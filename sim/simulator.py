# -*- coding: utf-8 -*-
from __future__ import division
import math
import random

from models.telemetry import TelemetryFrame

def _smoothstep(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


_PHASE_TARGETS = [
    (850, 0, 0, 14.7, 75.0),
    (3200, 60, 55, 14.2, 88.0),
    (6500, 130, 100, 12.8, 91.0),
    (1200, 30, 10, 15.2, 89.0),
]

_PHASE_NAMES = ["Idle", "Cruising", "Acceleration", "Deceleration"]
_PHASE_DURATION = 4.0


class Simulator:
    def __init__(self):
        self._t = 0.0
        self._coolant = 40.0
        self._last_phase = -1
        self.frame = TelemetryFrame()
        random.seed()

    @property
    def rpm(self):
        return self.frame.rpm

    @property
    def speed(self):
        return self.frame.speed

    @property
    def throttle(self):
        return self.frame.throttle

    @property
    def afr(self):
        return self.frame.afr

    @property
    def coolant(self):
        return self.frame.coolant

    @property
    def dtcs(self):
        return self.frame.dtcs

    @property
    def phase_name(self):
        return self.frame.phase_name

    def _phase_index(self):
        return int(self._t / _PHASE_DURATION) % 4

    def _lerp_phase_values(self):
        cycle_t = self._t % (4.0 * _PHASE_DURATION)
        seg = cycle_t / _PHASE_DURATION
        i0 = int(seg) % 4
        i1 = (i0 + 1) % 4
        ratio = _smoothstep(seg - math.floor(seg))

        start = _PHASE_TARGETS[i0]
        end = _PHASE_TARGETS[i1]
        rpm = start[0] + (end[0] - start[0]) * ratio
        speed = start[1] + (end[1] - start[1]) * ratio
        throttle = start[2] + (end[2] - start[2]) * ratio
        base_afr = start[3] + (end[3] - start[3]) * ratio
        coolant_target = start[4] + (end[4] - start[4]) * ratio
        return rpm, speed, throttle, base_afr, coolant_target

    def update(self, dt):
        if dt <= 0:
            dt = 1.0 / 30.0
        self._t += dt

        rpm, speed, throttle, base_afr, coolant_target = self._lerp_phase_values()
        phase_index = self._phase_index()
        phase_name = _PHASE_NAMES[phase_index]
        
        if phase_index != self._last_phase:
            from core.logger import logger
            if self._last_phase == -1:
                logger.log("connection", "Simulator initialized. Commencing runtime routines.")
            else:
                logger.log("info", "Engine shifting to {0} phase.".format(phase_name))
                if phase_index == 2:
                    logger.log("error", "Warning! Lean misfire detected (Simulated P0171/P0300).")
                elif self._last_phase == 2:
                    logger.log("connection", "Fault codes cleared. Normal operation resumed.")
            
            # Additional simulated log noise every phase switch
            logger.log("pid", "Requested [01 0C] - Engine RPM = {0:.0f}".format(rpm))
            logger.log("pid", "Requested [01 0D] - Vehicle Speed = {0:.0f}".format(speed))
            
            self._last_phase = phase_index

        throttle_factor = max(0.0, min(100.0, throttle)) / 100.0
        afr = base_afr - 1.2 * throttle_factor
        afr_noise = (random.random() - 0.5) * 0.12
        afr = max(10.0, min(20.0, afr + afr_noise))

        rpm += (random.random() - 0.5) * 25
        speed = max(0.0, speed + (random.random() - 0.5) * 0.8)
        throttle = max(0.0, min(100.0, throttle + (random.random() - 0.5) * 1.5))

        approach = coolant_target + 2.0 * math.sin(self._t * 0.15)
        rate = 0.35 + 0.15 * throttle_factor
        self._coolant += (approach - self._coolant) * rate * dt
        self._coolant = max(40.0, min(110.0, self._coolant))
        coolant = self._coolant + (random.random() - 0.5) * 0.4

        self.frame = TelemetryFrame(
            rpm=max(0.0, rpm),
            speed=speed,
            throttle=throttle,
            afr=afr,
            coolant=coolant,
            dtcs=["P0171", "P0300"] if phase_index == 2 else [],
            phase_name=phase_name,
        )
        
        # High-frequency random OBD-II chatter simulation
        if random.random() < 0.25:
            from core.logger import logger
            l_type = random.choice(["pid", "pid", "pid", "info", "warning"])
            if l_type == "pid":
                pids = ["01 0C", "01 0D", "01 04", "01 11", "01 05", "09 02", "01 1F", "01 2F"]
                req = random.choice(pids)
                fake_hex = "".join(random.choice("0123456789ABCDEF") for _ in range(random.choice([2, 4, 6])))
                logger.log("pid", "TX: {0}  RX: 41 {1} {2}".format(req.replace(" ", ""), req.split()[1], fake_hex))
            elif l_type == "info":
                msg = random.choice([
                    "Keep-alive packet sent (OK).",
                    "ELM327 buffer parsed.",
                    "Querying STFT/LTFT trims...",
                    "Checking timing advance."
                ])
                logger.log("info", msg)
            else:
                logger.log("warning", "High latency on CAN bus response.")

        return self.frame
