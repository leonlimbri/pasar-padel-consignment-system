def check_any_input_is_empty(input):
    if input is None: return True
    if isinstance(input, int) or isinstance(input, float):
        return False if input < 0 or input > 0 else True
    if len(input) > 1 and isinstance(input, list):
        return any([check_any_input_is_empty(inp) for inp in input])
    return True if input == "" or len(input) == 0 else False