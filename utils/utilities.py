"""utils/utilities.py
General-purpose helper functions used across the app.
"""


def check_any_input_is_empty(input):
    """Recursively check whether any value in `input` is considered empty.

    Rules:
    - None            → empty
    - int / float 0   → empty  (non-zero numbers are valid)
    - empty string    → empty
    - empty list      → empty
    - list with items → recurse into each element

    Returns True if any value is empty, False otherwise.
    """
    if input is None:
        return True

    if isinstance(input, (int, float)):
        # 0 is treated as "empty" (no value entered); other numbers are fine
        return input == 0

    if isinstance(input, list) and len(input) > 1:
        return any(check_any_input_is_empty(item) for item in input)

    return input == "" or len(input) == 0
