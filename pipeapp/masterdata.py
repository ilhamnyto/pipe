from django.shortcuts import redirect, render
from .models import Dosen, Nilai, Peminatan, Keprof, Profile
import pandas as pd
from.dburl import engine

def deleteData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      Dosen.objects.get(id=request.POST['id']).delete()
      return redirect('datadosen')
    elif request.POST['data'] == 'NILAI':
      Nilai.objects.get(id=request.POST['id']).delete()
      return redirect('datamahasiswa')
    elif request.POST['data'] == 'PEMINATAN':
      Nilai.objects.get(id=request.POST['id']).delete()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      Nilai.objects.get(id=request.POST['id']).delete()
      return redirect('datakeprof')


def insertData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      dosen = Dosen(name=request.POST['name'], kelompok=request.POST['kelompok'], peminatan=request.POST['peminatan'])
      dosen.save()
      return redirect('datadosen')
    elif request.POST['data'] == 'NILAI':
      nilai = Nilai(
        nim=request.POST['nim'],
        name=request.POST['name'],
        rpb=request.POST['rpb'],
        probstat=request.POST['probstat'],
        basdat=request.POST['basdat'],
        dwbi=request.POST['dwbi'],
        oop=request.POST['oop'],
        apsi=request.POST['apsi'],
        alpro=request.POST['alpro'],
        web=request.POST['web'],
        ea=request.POST['ea'],
        manlay=request.POST['manlay'],
        se=request.POST['se'],
        scm=request.POST['scm'],
        akuntansi=request.POST['akuntansi'],
        manprosi=request.POST['manprosi'],
        desjar=request.POST['desjar'],
        manjarkom=request.POST['manjarkom'],
        sisop=request.POST['sisop'],
        ksi=request.POST['ksi'],
      )
      nilai.save()
      return redirect('datamahasiswa')
    elif request.POST['data'] == 'PEMINATAN':


      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':


      return redirect('datakeprof')

def updateData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      dosen = Dosen.objects.get(id=request.POST['id'])
      dosen.name = request.POST['name']
      dosen.kelompok = request.POST['kelompok']
      dosen.peminatan = request.POST['peminatan']
      dosen.save()
      return redirect('datadosen')
    elif request.POST['data'] == 'NILAI':
      nilai = Nilai.objects.get(id=request.POST['id'])
      nilai.nim = request.POST['nim']
      nilai.name = request.POST['name']
      nilai.rpb = request.POST['rpb']
      nilai.probstat = request.POST['probstat']
      nilai.basdat = request.POST['basdat']
      nilai.dwbi = request.POST['dwbi']
      nilai.oop = request.POST['oop']
      nilai.apsi = request.POST['apsi']
      nilai.alpro = request.POST['alpro']
      nilai.web = request.POST['web']
      nilai.ea = request.POST['ea']
      nilai.manlay = request.POST['manlay']
      nilai.se = request.POST['se']
      nilai.scm = request.POST['scm']
      nilai.akuntansi = request.POST['akuntansi']
      nilai.manprosi = request.POST['manprosi']
      nilai.desjar = request.POST['desjar']
      nilai.manjarkom = request.POST['manjarkom']
      nilai.sisop = request.POST['sisop']
      nilai.ksi = request.POST['ksi']
      nilai.save()
      return redirect('datamahasiswa')
    elif request.POST['data'] == 'PEMINATAN':


      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':


      return redirect('datakeprof')

def importData(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      # try:
        dosen = pd.read_excel(request.FILES['file'])
        dosen.columns = map(str.lower, dosen.columns)
        Dosen.objects.all().delete()
        dosen.to_sql('pipeapp_dosen', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datadosen')
      # except Exception:
      #   return render(request, 'tambahdosen.html', {'user': user, "error"})
    elif request.POST['data'] == 'NILAI':
      # try:
        nilai = pd.read_excel(request.FILES['file'])
        nilai.columns = map(str.lower, nilai.columns)
        Nilai.objects.all().delete()
        nilai.to_sql('pipeapp_nilai', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datamahasiswa')
      # except Exception:
      #   print('error')
      #   return redirect('datamahasiswa')

    elif request.POST['data'] == 'PEMINATAN':


      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':


      return redirect('datakeprof')

def truncateData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      Dosen.objects.all().delete()
      return redirect('datadosen')
    elif request.POST['data'] == 'NILAI':
      Nilai.objects.all().delete()
      return redirect('datamahasiswa')
    elif request.POST['data'] == 'PEMINATAN':
      Peminatan.objects.all().delete()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      Keprof.objects.all().delete()
      return redirect('datakeprof')
