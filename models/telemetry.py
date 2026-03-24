from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TelemetryFrame:
    rpm: float = 850.0
    speed: float = 0.0
    throttle: float = 0.0
    afr: float = 14.7
    coolant: float = 40.0
    dtcs: list[str] = field(default_factory=list)
    phase_name: str = "Idle"
