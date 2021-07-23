from django.shortcuts import redirect

def login_required():
  def decorator(view_func):
    def wrap(request, *args, **kwargs):
      if "user_login" in request.session:
        return view_func(request, *args, **kwargs)
      else:
        return redirect('index')
    return wrap
  return decorator

def is_authenticated():
  def decorator(view_func):
    def wrap(request, *args, **kwargs):
      if "user_login" in request.session:
        return redirect('home')
      else:
        return view_func(request, *args, **kwargs)
    return wrap
  return decorator