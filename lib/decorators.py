from django.shortcuts import redirect

def forDjango(cls):
    """
    Enums values are callable in django template which causing issues, so use
    this decorator to fix this, so enum values will show as it is without call it.
    """

    cls.do_not_call_in_templates = True
    return cls

def anonymous_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
