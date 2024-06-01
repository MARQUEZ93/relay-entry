from django.shortcuts import redirect

def anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'

    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_to)
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function
