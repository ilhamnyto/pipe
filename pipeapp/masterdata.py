from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Batch, Bobot, Dosen, Nilai, Peminatan, Keprof, Profile, Seleksi
import pandas as pd
from.dburl import engine

def deleteData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      bobot = Bobot.objects.get(id=1)
      Dosen.objects.get(id=request.POST['id']).delete()
      ede = Peminatan.objects.get(peminatancode='EDE')
      eisd = Peminatan.objects.get(peminatancode='EISD')
      eim = Peminatan.objects.get(peminatancode='EIM')
      erp = Peminatan.objects.get(peminatancode='ERP')
      sag = Peminatan.objects.get(peminatancode='SAG')

      ede.kuota = Dosen.objects.filter(peminatan='EDE').count() * bobot.kuotadosen
      eisd.kuota = Dosen.objects.filter(peminatan='EISD').count() * bobot.kuotadosen
      eim.kuota = Dosen.objects.filter(peminatan='EIM').count() * bobot.kuotadosen
      erp.kuota = Dosen.objects.filter(peminatan='ERP').count() * bobot.kuotadosen
      sag.kuota = Dosen.objects.filter(peminatan='SAG').count() * bobot.kuotadosen

      ede.save()
      eisd.save()
      eim.save()
      erp.save()
      sag.save()
      return redirect('datadosen')
    elif request.POST['data'] == 'NILAI':
      Nilai.objects.get(id=request.POST['id']).delete()
      return redirect('datamahasiswa')
    elif request.POST['data'] == 'PEMINATAN':
      peminatan = Peminatan.objects.get(peminatancode=request.POST['id'])
      peminatan.delete()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      Keprof.objects.get(id=request.POST['id']).delete()
      return redirect('datakeprof')


def insertData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      bobot = Bobot.objects.get(id=1)
      dosen = Dosen(name=request.POST['name'], kelompok=request.POST['kelompok'], peminatan=request.POST['peminatan'])
      dosen.save()
      jumlah = Dosen.objects.filter(peminatan=request.POST['peminatan']).count() * bobot.kuotadosen
      peminatan = Peminatan.objects.get(peminatancode=request.POST['peminatan'])
      peminatan.kuota = jumlah
      peminatan.save()
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
      peminatan = Peminatan(peminatancode=request.POST['kodepeminatan'], peminatanname=request.POST['namapeminatan'], kelompokkeahlian=request.POST['kelompokkeahlian'])
      peminatan.save()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      keprof = Keprof(nim=request.POST['nim'], name=request.POST['name'], keprof=request.POST['keprofesian'], kategori=request.POST['kategori'])
      keprof.save()
      return redirect('datakeprof')

def updateData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      bobot = Bobot.objects.get(id=1)
      dosen = Dosen.objects.get(id=request.POST['id'])
      dosen.name = request.POST['name']
      dosen.kelompok = request.POST['kelompok']
      dosen.peminatan = request.POST['peminatan']
      dosen.save()
      
      ede = Peminatan.objects.get(peminatancode='EDE')
      eisd = Peminatan.objects.get(peminatancode='EISD')
      eim = Peminatan.objects.get(peminatancode='EIM')
      erp = Peminatan.objects.get(peminatancode='ERP')
      sag = Peminatan.objects.get(peminatancode='SAG')

      ede.kuota = Dosen.objects.filter(peminatan='EDE').count() * bobot.kuotadosen
      eisd.kuota = Dosen.objects.filter(peminatan='EISD').count() * bobot.kuotadosen
      eim.kuota = Dosen.objects.filter(peminatan='EIM').count() * bobot.kuotadosen
      erp.kuota = Dosen.objects.filter(peminatan='ERP').count() * bobot.kuotadosen
      sag.kuota = Dosen.objects.filter(peminatan='SAG').count() * bobot.kuotadosen

      ede.save()
      eisd.save()
      eim.save()
      erp.save()
      sag.save()
      
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
      peminatan.save()
      return redirect('datapeminatan')
    elif request.POST['data'] == 'KEPROF':
      keprof = Keprof.objects.get(id=request.POST['id'])
      keprof.nim = request.POST['nim']
      keprof.name = request.POST['name']
      keprof.keprof = request.POST['keprofesian']
      keprof.kategori = request.POST['kategori']
      keprof.save()
      return redirect('datakeprof')

def importData(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      try:
        bobot = Bobot.objects.get(id=1)
        dosen = pd.read_excel(request.FILES['file'])
        dosen.columns = map(str.lower, dosen.columns)
        dosen.to_sql('pipeapp_dosen', con=engine, index=False, if_exists="append", method='multi')

        ede = Peminatan.objects.get(peminatancode='EDE')
        eisd = Peminatan.objects.get(peminatancode='EISD')
        eim = Peminatan.objects.get(peminatancode='EIM')
        erp = Peminatan.objects.get(peminatancode='ERP')
        sag = Peminatan.objects.get(peminatancode='SAG')

        ede.kuota = Dosen.objects.filter(peminatan='EDE').count() * bobot.kuotadosen
        eisd.kuota = Dosen.objects.filter(peminatan='EISD').count() * bobot.kuotadosen
        eim.kuota = Dosen.objects.filter(peminatan='EIM').count() * bobot.kuotadosen
        erp.kuota = Dosen.objects.filter(peminatan='ERP').count() * bobot.kuotadosen
        sag.kuota = Dosen.objects.filter(peminatan='SAG').count() * bobot.kuotadosen

        ede.save()
        eisd.save()
        eim.save()
        erp.save()
        sag.save()
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
      try:
        peminatan = pd.read_excel(request.FILES['file'])
        peminatan.columns = map(str.lower, peminatan.columns)
        peminatan.to_sql('pipeapp_peminatan', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datapeminatan')
      except Exception:
        return render(request, 'tambahpeminatan.html', {'user': user, "error" : "File tidak sesuai."})

    elif request.POST['data'] == 'KEPROF':
      try:
        keprof = pd.read_excel(request.FILES['file'])
        keprof.columns = map(str.lower, keprof.columns)
        keprof.to_sql('pipeapp_keprof', con=engine, index=False, if_exists="append", method='multi')
        return redirect('datakeprof')
      except Exception:
        return render(request, 'tambahkeprof.html', {'user': user, "error" : "File tidak sesuai."})


def truncateData(request):
  if request.method == 'POST':
    if request.POST['data'] == 'DOSEN':
      Dosen.objects.all().delete()

      ede = Peminatan.objects.get(peminatancode='EDE')
      eisd = Peminatan.objects.get(peminatancode='EISD')
      eim = Peminatan.objects.get(peminatancode='EIM')
      erp = Peminatan.objects.get(peminatancode='ERP')
      sag = Peminatan.objects.get(peminatancode='SAG')

      ede.kuota = 0
      eisd.kuota = 0
      eim.kuota = 0
      erp.kuota = 0
      sag.kuota = 0

      ede.save()
      eisd.save()
      eim.save()
      erp.save()
      sag.save()
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

def exportMahasiswa(request):
  user = Profile.objects.get(username=request.session['user_login'])
  results = pd.DataFrame.from_records(Profile.objects.filter(Q(role='MAHASISWA') & Q(peminatan=user.peminatan)).values('numberid', 'fullname'))
  results.columns = ['NIM', 'Nama']
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=peminatan.csv'
  results.to_csv(path_or_buf=response,sep=',',float_format='%.2f', index=False, decimal=".")
  return response