
def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

