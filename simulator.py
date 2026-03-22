# -*- coding: utf-8 -*-
from __future__ import division
"""
Demo ECU simulator — no hardware, no network.
"""

import math
import random


def _smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


# (rpm, speed_kmh, throttle_pct, base_afr, coolant_target_C)
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
        self.rpm = 850.0
        self.speed = 0.0
        self.throttle = 0.0
        self.afr = 14.7
        self.coolant = 40.0
        self.dtcs = []
        self.phase_name = "Idle"
        random.seed()

    def _phase_index(self):
        return int(self._t / _PHASE_DURATION) % 4

    def _lerp_phase_values(self):
        """Interpolate between consecutive phase targets over each 4s segment."""
        cycle_t = self._t % (4.0 * _PHASE_DURATION)
        seg = cycle_t / _PHASE_DURATION
        i0 = int(seg) % 4
        i1 = (i0 + 1) % 4
        u = _smoothstep(seg - math.floor(seg))

        a = _PHASE_TARGETS[i0]
        b = _PHASE_TARGETS[i1]
        rpm = a[0] + (b[0] - a[0]) * u
        speed = a[1] + (b[1] - a[1]) * u
        throttle = a[2] + (b[2] - a[2]) * u
        base_afr = a[3] + (b[3] - a[3]) * u
        cool_tgt = a[4] + (b[4] - a[4]) * u
        return rpm, speed, throttle, base_afr, cool_tgt

    def update(self, dt):
        if dt <= 0:
            dt = 1.0 / 30.0
        self._t += dt

        rpm, speed, throttle, base_afr, cool_tgt = self._lerp_phase_values()
        phase_i = self._phase_index()
        self.phase_name = _PHASE_NAMES[phase_i]

        # Richer mixture with more throttle (lower AFR), on top of phase lerp
        throttle_f = max(0.0, min(100.0, throttle)) / 100.0
        afr = base_afr - 1.2 * throttle_f
        noise = (random.random() - 0.5) * 0.12
        afr = max(10.0, min(20.0, afr + noise))

        rpm += (random.random() - 0.5) * 25
        speed = max(0.0, speed + (random.random() - 0.5) * 0.8)
        throttle = max(0.0, min(100.0, throttle + (random.random() - 0.5) * 1.5))

        # Coolant warms slowly toward target (~90°C steady state)
        approach = cool_tgt + 2.0 * math.sin(self._t * 0.15)
        rate = 0.35 + 0.15 * throttle_f
        self._coolant += (approach - self._coolant) * rate * dt
        self._coolant = max(40.0, min(110.0, self._coolant))
        coolant = self._coolant + (random.random() - 0.5) * 0.4

        self.rpm = max(0.0, rpm)
        self.speed = speed
        self.throttle = throttle
        self.afr = afr
        self.coolant = coolant

        if phase_i == 2:
            self.dtcs = ["P0171", "P0300"]
        else:
            self.dtcs = []
