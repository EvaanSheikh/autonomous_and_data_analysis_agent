def calculate_percentage_change(
    old_value: float,
    new_value: float,
) -> dict:
    """
    Calculate the percentage change from an old value to a new value.

    Formula:
        ((new_value - old_value) / old_value) * 100

    Returns:
        Structured percentage-change result.
    """
    if not isinstance(old_value, (int, float)):
        raise TypeError("old_value must be numerical.")

    if not isinstance(new_value, (int, float)):
        raise TypeError("new_value must be numerical.")

    if old_value == 0:
        raise ValueError(
            "Percentage change cannot be calculated when old_value is zero."
        )

    absolute_change = new_value - old_value
    percentage_change = (absolute_change / old_value) * 100

    if percentage_change > 0:
        direction = "increase"
    elif percentage_change < 0:
        direction = "decrease"
    else:
        direction = "no_change"

    return {
        "operation": "calculate_percentage_change",
        "parameters": {
            "old_value": old_value,
            "new_value": new_value,
        },
        "absolute_change": float(absolute_change),
        "percentage_change": float(percentage_change),
        "direction": direction,
    }