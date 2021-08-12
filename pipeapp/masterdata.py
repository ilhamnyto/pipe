from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Batch, Dosen, Nilai, Peminatan, Keprof, Profile, Seleksi
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
      peminatan = Peminatan.objects.get(peminatancode=request.POST['id'])
      print(peminatan)
      print(peminatan.peminatancode)
      peminatan.delete()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      Keprof.objects.get(id=request.POST['id']).delete()
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
      peminatan = Peminatan(peminatancode=request.POST['kodepeminatan'], peminatanname=request.POST['namapeminatan'], kelompokkeahlian=request.POST['kelompokkeahlian'], kuota=request.POST['kuota'])
      peminatan.save()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      keprof = Keprof(nim=request.POST['nim'], name=request.POST['name'], keprof=request.POST['keprofesian'])
      keprof.save()
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
      peminatan = Peminatan.objects.get(peminatancode=request.POST['id'])
      peminatan.peminatanname = request.POST['namapeminatan']
      peminatan.kelompokkeahlian=request.POST['kelompokkeahlian']
      peminatan.kuota=request.POST['kuota']
      peminatan.save()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      keprof = Keprof.objects.get(id=request.POST['id'])
      keprof.nim = request.POST['nim']
      keprof.name = request.POST['name']
      keprof.keprof = request.POST['keprofesian']
      keprof.save()
      return redirect('datakeprof')

def importData(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      try:
        dosen = pd.read_excel(request.FILES['file'])
        dosen.columns = map(str.lower, dosen.columns)
        dosen.to_sql('pipeapp_dosen', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datadosen')
      except Exception:
        return render(request, 'tambahdosen.html', {'user': user, "error" : "File tidak sesuai."})
    elif request.POST['data'] == 'NILAI':
      try:
        nilai = pd.read_excel(request.FILES['file'])
        nilai.columns = map(str.lower, nilai.columns)
        nilai.to_sql('pipeapp_nilai', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datamahasiswa')
      except Exception:
        return render(request, 'tambahnilai.html', {'user': user, "error" : "File tidak sesuai"})

    elif request.POST['data'] == 'PEMINATAN':
       
        return render(request, 'tambahpeminatan.html', {'user': user, "error" : "File tidak sesuai."})

    elif request.POST['data'] == 'KEPROF':
        
        return render(request, 'tambahkeprof.html', {'user': user, "error" : "File tidak sesuai."})


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

def exportData(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  latestbatch = Batch.objects.filter(id=id)
  if latestbatch:
    results = pd.DataFrame.from_records(Seleksi.objects.filter(batch=latestbatch[0]).values('studentid__numberid', 'studentid__fullname', 'pilihan1_id', 'pilihan2_id', 'score1', 'score2', 'result_id'))
    results.columns = ['NIM', 'Nama', 'Pilihan 1', 'Pilihan 2', 'Skor Pilihan 1', 'Skor Pilihan 2', 'Peminatan']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=seleksi.csv'
    results.to_csv(path_or_buf=response,sep=',',float_format='%.2f', index=False, decimal=".")
    return response
  else:
    return redirect('hasilseleksi')