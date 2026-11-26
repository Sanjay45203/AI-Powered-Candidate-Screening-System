def calculate_time_savings(manual_hours_per_1000: float, automated_hours_for_1000: float) -> dict:
    if manual_hours_per_1000 <= 0:
        raise ValueError("Manual hours must be positive.")
    reduction = (manual_hours_per_1000 - automated_hours_for_1000) / manual_hours_per_1000 * 100
    return {
        "manual_hours_per_1000": round(manual_hours_per_1000, 3),
        "automated_hours_per_1000": round(automated_hours_for_1000, 3),
        "time_reduction_percent": round(max(0, reduction), 3)
    }
