from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Profile, Peminatan, StatusServer
import requests as req

def login(request):
  profile = Profile.objects.filter(username=request.POST['username'])
  statuslogin = StatusServer.objects.get(name='Login') 
  if request.method == 'POST':
      data = {
      "username": request.POST['username'],
      "password": request.POST['password']
      }
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

      login = req.post('https://gateway.telkomuniversity.ac.id/issueauth', data=data, headers=headers)

      token = login.json()

      if 'token' in token and statuslogin.isAvailable:
        if profile:
          request.session['user_login'] = request.POST['username']
          return redirect('home')
        else:
          bearertoken = {
            "Authorization": "Bearer {tokens}".format(tokens = token['token']),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
          }
          getprofile = req.get('https://gateway.telkomuniversity.ac.id/issueprofile', headers=bearertoken)
          getposisi = req.get('https://gateway.telkomuniversity.ac.id/issuerole', headers=bearertoken)

          profile = getprofile.json()
          posisi = getposisi.json()
          
          if posisi and posisi[0]['role'] == 'MAHASISWA':
            users = Profile(
              numberid= profile['numberid'],
              username=request.POST['username'],
              fullname= profile['fullname'],
              studyprogram= profile['studyprogram'],
              faculty= profile['faculty'],
              schoolyear= profile['schoolyear'],
              studentclass= profile['studentclass'],
              lecturerguardian= profile['lecturerguardian'],
              photo= profile['photo'],
              role= posisi[0]['role']
            )

            request.session['user_login'] = request.POST['username']
            users.save()
          else:
            users = Profile(
              numberid= profile['numberid'],
              username=request.POST['username'],
              fullname= profile['fullname'],
              role='DOSEN'
            )

            request.session['user_login'] = request.POST['username']
            users.save()

          return redirect('home')
      elif 'token' in token and profile and profile[0].role == 'ADMIN':
        request.session['user_login'] = request.POST['username']
        return redirect('home')
      elif not statuslogin.isAvailable:
        return render(request, 'index.html', {"error": "Server belum dibuka oleh admin."})
      else: 
        return render(request, 'index.html', {"error": "Wrong username or password."})

  else:
    return JsonResponse({"error": {
      "status": "403",
      "message": "method is not allowed"
    }})
    

def logout(request):
  try:
    del request.session['user_login']
  except KeyError:
    pass
  return redirect('index')