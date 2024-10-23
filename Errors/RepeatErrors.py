class RepeatErrors(Exception):
    """It is worth calling when repeating
    the call to the decorator function did not lead to anything and there is still an error"""