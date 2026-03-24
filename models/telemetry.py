# -*- coding: utf-8 -*-
class TelemetryFrame:
    def __init__(self, rpm=850.0, speed=0.0, throttle=0.0, afr=14.7, coolant=40.0, dtcs=None, phase_name="Idle"):
        self.rpm = rpm
        self.speed = speed
        self.throttle = throttle
        self.afr = afr
        self.coolant = coolant
        self.dtcs = dtcs if dtcs is not None else []
        self.phase_name = phase_name
