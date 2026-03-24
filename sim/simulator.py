from __future__ import annotations

import math
import random

from models.telemetry import TelemetryFrame


def _smoothstep(value: float) -> float:
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
    def __init__(self) -> None:
        self._t = 0.0
        self._coolant = 40.0
        self.frame = TelemetryFrame()
        random.seed()

    @property
    def rpm(self) -> float:
        return self.frame.rpm

    @property
    def speed(self) -> float:
        return self.frame.speed

    @property
    def throttle(self) -> float:
        return self.frame.throttle

    @property
    def afr(self) -> float:
        return self.frame.afr

    @property
    def coolant(self) -> float:
        return self.frame.coolant

    @property
    def dtcs(self) -> list[str]:
        return self.frame.dtcs

    @property
    def phase_name(self) -> str:
        return self.frame.phase_name

    def _phase_index(self) -> int:
        return int(self._t / _PHASE_DURATION) % 4

    def _lerp_phase_values(self) -> tuple[float, float, float, float, float]:
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

    def update(self, dt: float) -> TelemetryFrame:
        if dt <= 0:
            dt = 1.0 / 30.0
        self._t += dt

        rpm, speed, throttle, base_afr, coolant_target = self._lerp_phase_values()
        phase_index = self._phase_index()
        phase_name = _PHASE_NAMES[phase_index]

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
        return self.frame
