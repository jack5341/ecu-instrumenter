from __future__ import annotations

from config import settings as C


def afr_zone_color(afr: float) -> tuple[int, int, int]:
    zone_count = len(C.AFR_ZONES)
    for index, (lo, hi, color) in enumerate(C.AFR_ZONES):
        is_last = index == zone_count - 1
        if is_last and lo <= afr <= hi:
            return color
        if not is_last and lo <= afr < hi:
            return color
    return C.WHITE


def rpm_arc_color(rpm: float) -> tuple[int, int, int]:
    if rpm >= C.RPM_DANGER:
        return C.RED
    if rpm >= C.RPM_WARN:
        return C.ORANGE
    return C.CYAN
