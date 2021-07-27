from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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

def role_required(allowed_roles=[]):
  def decorator(view_func):
    def wrap(request, *args, **kwargs):
      if request.session['role'] in allowed_roles:
        return view_func(request, *args, **kwargs)
      else:
        raise PermissionDenied
    return wrap
  return decorator


def diterimalist(peminatan):
  cybernatics = peminatan[(peminatan['result_id'] == 'EISD') | (peminatan['result_id'] == 'EDE')]
  eis = peminatan[(peminatan['result_id'] == 'SAG') | (peminatan['result_id'] == 'ERP') | (peminatan['result_id'] == 'EIM')]
  return [cybernatics['counts'].sum(), eis['counts'].sum()]

def daftarlist(peminatan):
  cybernatics = peminatan[(peminatan['pilihan'] == 'EISD') | (peminatan['pilihan'] == 'EDE')]
  eis = peminatan[(peminatan['pilihan'] == 'SAG') | (peminatan['pilihan'] == 'ERP') | (peminatan['pilihan'] == 'EIM')]
  return [cybernatics['counts'].sum(), eis['counts'].sum()]

def rasiolist(pendaftar, diterima):
  p_cybernatics = pendaftar[(pendaftar['pilihan'] == 'EISD') | (pendaftar['pilihan'] == 'EDE')]
  p_eis = pendaftar[(pendaftar['pilihan'] == 'SAG') | (pendaftar['pilihan'] == 'ERP') | (pendaftar['pilihan'] == 'EIM')]

  d_cybernatics = diterima[(diterima['result_id'] == 'EISD') | (diterima['result_id'] == 'EDE')]
  d_eis = diterima[(diterima['result_id'] == 'SAG') | (diterima['result_id'] == 'ERP') | (diterima['result_id'] == 'EIM')]

  return [ f"{d_cybernatics['counts'].sum() / p_cybernatics['counts'].sum() * 100:.1f}%", f"{d_eis['counts'].sum() / p_eis['counts'].sum() * 100:.1f}%"]