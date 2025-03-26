def forDjango(cls):
    """
    Enums values are callable in django template which causing issues, so use
    this decorator to fix this, so enum values will show as it is without call it.
    """

    cls.do_not_call_in_templates = True
    return cls
