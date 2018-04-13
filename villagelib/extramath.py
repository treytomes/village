
def is_in_range(value, inclusive_min, exclusive_max):
    return (inclusive_min <= value) and (value < exclusive_max)

def clamp(value, inclusive_min, inclusive_max):
    if value < inclusive_min:
        value = inclusive_min
    elif value > inclusive_max:
        value = inclusive_max
    return value
