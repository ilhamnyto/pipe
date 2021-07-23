from pipeapp.models import StatusServer
from django.shortcuts import redirect



def loginstatus(request):
  status = StatusServer.objects.get(name='Login')
  if request.method == 'POST':
    if request.POST['status'] == 'enable':
      status.isAvailable = True
      status.save()
      return redirect('home')
    else:
      status.isAvailable = False
      status.save()
      return redirect('home')
  return redirect('home')

