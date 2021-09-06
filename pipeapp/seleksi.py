from django.db.models.expressions import F
from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count

def daftarpeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  eins = ['SAG', 'ERP', 'EIM']
  cybernetics = ['EISD', 'EDE']
  
  if request.method == 'POST':
    if 'reset' in request.POST:
      seleksi = Seleksi.objects.get(studentid__username=request.session['user_login'])
      seleksi.delete()
      return redirect('daftar')
    elif request.POST['pilihan1'] == request.POST['pilihan2']:
      peminatan = Peminatan.objects.all()
      batch = Batch.objects.last()
      seleksistatus = Seleksi.objects.filter(studentid=user.numberid)
      serverstatus = StatusServer.objects.get(name='Batch Pendaftaran')
      return render(request, 'daftar.html', {'user': user, 'peminatan': peminatan, 'batch': batch, 'seleksistatus': seleksistatus, "serverstatus": serverstatus, 'error': "Pilihan 1 dan pilihan 2 tidak boleh sama."})
    elif (request.POST['pilihan1'] in eins and request.POST['pilihan2'] in eins) or (request.POST['pilihan1'] in cybernetics and request.POST['pilihan2'] in cybernetics):
      peminatan = Peminatan.objects.all()
      batch = Batch.objects.last()
      seleksistatus = Seleksi.objects.filter(studentid=user.numberid)
      serverstatus = StatusServer.objects.get(name='Batch Pendaftaran')
      return render(request, 'daftar.html', {'user': user, 'peminatan': peminatan, 'batch': batch, 'seleksistatus': seleksistatus, "serverstatus": serverstatus, 'error': "Pilihan 1 dan pilihan 2 tidak boleh dari kelompok keahlian yang sama."})
    else:
      batch = Batch.objects.get(id=request.POST['batch'])
      pilihan1 = Peminatan.objects.get(peminatancode=request.POST['pilihan1'])
      pilihan2 = Peminatan.objects.get(peminatancode=request.POST['pilihan2'])
      seleksi = Seleksi(studentid=user, pilihan1=pilihan1, pilihan2=pilihan2, batch=batch)
      seleksi.save()

      return redirect('daftar')

  else:
    return JsonResponse({"error": {
      "status": "403",
      "message": "method is not allowed"
    }})

def pengajuantukar(request):
  if 'reset' in request.POST:
    mahasiswa1 = Profile.objects.get(username=request.session['user_login'])
    TukarPeminatan.objects.get(Q(mahasiswa1=mahasiswa1) or Q(mahasiswa2=mahasiswa1)).delete()
    return redirect('tukar')
  else:
    mahasiswa1 = Profile.objects.get(username=request.session['user_login'])
    mahasiswa2 = Profile.objects.filter(fullname=request.POST['mahasiswadua'])
    if mahasiswa2 and mahasiswa2[0].peminatan:
      tukar = TukarPeminatan(
        mahasiswa1=mahasiswa1,
        mahasiswa2=mahasiswa2[0],
        status="Pengajuan I"
      )
      tukar.save()

    return redirect('tukar')

def pindahpeminatan(request):
  if request.method == 'POST':
    user = Profile.objects.get(username=request.session['user_login'])
    mahasiswa = Profile.objects.get(numberid=request.POST['mahasiswa'])
    mahasiswa.peminatan = user.peminatan
    mahasiswa.save()

    return redirect('pindah')

def pengajuankedosen(request):
  tukar = TukarPeminatan.objects.get(id=request.POST['tukarid'])
  if request.method == 'POST':
    if request.POST['status'] == 'Pengajuan I' and request.POST['decision'] == 'approve':
      tukar.status = 'Pengajuan II'
      tukar.save()
      return redirect('tukar')
    elif request.POST['status'] == 'Pengajuan I' and request.POST['decision'] == 'decline':
      tukar.status = 'Ditolak I'
      tukar.save()
      return redirect('tukar')
    elif request.POST['status'] == 'Pengajuan II' and request.POST['decision'] == 'approve':
      tukar.status = 'Disetujui'
      mahasiswa1 = Profile.objects.get(username=tukar.mahasiswa1.username)
      mahasiswa2 = Profile.objects.get(username=tukar.mahasiswa2.username)
      peminatan = mahasiswa1.peminatan
      mahasiswa1.peminatan = mahasiswa2.peminatan
      mahasiswa2.peminatan = peminatan
      mahasiswa1.save()
      mahasiswa2.save()
      tukar.save()
      return redirect('tukar')
    elif request.POST['status'] == 'Pengajuan II' and request.POST['decision'] == 'decline':
      tukar.status = 'Ditolak II'
      tukar.save()
      return redirect('tukar')
    return redirect('tukar')

def statusbatch(request):
  status = StatusServer.objects.get(name='Batch Pendaftaran')
  if request.method == 'POST':
    if request.POST['status'] == 'enable':
      status.isAvailable = True
      status.save()
      return redirect('seleksipeminatan')
    else:
      status.isAvailable = False
      status.save()
      return redirect('seleksipeminatan')
  return redirect('seleksipeminatan')

def createbatch(request):
  if request.method == 'POST':
    newbatch = Batch(batchnum=request.POST['batchnum'])
    newbatch.save()
    status = StatusServer.objects.get(name='Batch Pendaftaran')
    status.isAvailable = False
    status.save() 
    return redirect('seleksipeminatan')
  return redirect('seleksipeminatan')

def plotting(request, id):
  if request.method == 'POST':
    bobot = Bobot.objects.get(id=1)
    batch = Batch.objects.get(id=id)
    print(batch)
    ede = Seleksi.objects.filter(pilihan1='EDE', result__isnull=True, batch=batch).order_by('-score1')
    eisd = Seleksi.objects.filter(pilihan1='EISD', result__isnull=True, batch=batch).order_by('-score1')
    sag = Seleksi.objects.filter(pilihan1='SAG', result__isnull=True, batch=batch).order_by('-score1')
    eim = Seleksi.objects.filter(pilihan1='EIM', result__isnull=True, batch=batch).order_by('-score1')
    erp = Seleksi.objects.filter(pilihan1='ERP', result__isnull=True, batch=batch).order_by('-score1')

    edekuota = Peminatan.objects.get(peminatancode='EDE')
    eisdkuota = Peminatan.objects.get(peminatancode='EISD')
    eimkuota = Peminatan.objects.get(peminatancode='EIM')
    erpkuota = Peminatan.objects.get(peminatancode='ERP')
    sagkuota = Peminatan.objects.get(peminatancode='SAG')

    edekuota.sisakuota = Dosen.objects.filter(peminatan='EDE').count() * bobot.kuotadosen - Seleksi.objects.filter(result__peminatancode='EDE').count()
    eisdkuota.sisakuota = Dosen.objects.filter(peminatan='EISD').count() * bobot.kuotadosen - Seleksi.objects.filter(result__peminatancode='EISD').count()
    eimkuota.sisakuota = Dosen.objects.filter(peminatan='EIM').count() * bobot.kuotadosen - Seleksi.objects.filter(result__peminatancode='EIM').count()
    erpkuota.sisakuota = Dosen.objects.filter(peminatan='ERP').count() * bobot.kuotadosen - Seleksi.objects.filter(result__peminatancode='ERP').count()
    sagkuota.sisakuota = Dosen.objects.filter(peminatan='SAG').count() * bobot.kuotadosen - Seleksi.objects.filter(result__peminatancode='SAG').count()

    edekuota.save()
    eisdkuota.save()
    eimkuota.save()
    erpkuota.save()
    sagkuota.save()

    for s in sag:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan1.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan1.peminatancode)
        data.result = s.pilihan1
        mahasiswa.peminatan = s.pilihan1
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()

    for s in ede:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan1.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan1.peminatancode)
        data.result = s.pilihan1
        mahasiswa.peminatan = s.pilihan1
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()

    for s in eisd:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan1.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan1.peminatancode)
        data.result = s.pilihan1
        mahasiswa.peminatan = s.pilihan1
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()

    for s in eim:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan1.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan1.peminatancode)
        data.result = s.pilihan1
        mahasiswa.peminatan = s.pilihan1
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()

    for s in erp:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan1.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan1.peminatancode)
        data.result = s.pilihan1
        mahasiswa.peminatan = s.pilihan1
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()

    pilihan2 = Seleksi.objects.filter(result__isnull=True, batch=batch)
    for s in pilihan2:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif s.pilihan2.sisakuota <= 0:
        pass
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        mahasiswa = Profile.objects.get(numberid=s.studentid.numberid)
        peminatan = Peminatan.objects.get(peminatancode=s.pilihan2.peminatancode)
        data.result = s.pilihan2
        mahasiswa.peminatan = s.pilihan2
        peminatan.sisakuota -= 1
        peminatan.save()
        data.save()
        mahasiswa.save()


    return redirect('penghitungannilai')

def hitung(request, latestbatch):
  bobot = Bobot.objects.get(id=1)
  seleksi = Profile.objects.filter(role='MAHASISWA', seleksi_student__batch=latestbatch, peminatan__isnull=True).values('numberid', 'fullname', 'seleksi_student__pilihan1__peminatanname', 'seleksi_student__pilihan1__kuota', 'seleksi_student__pilihan2__peminatanname', 'seleksi_student__pilihan2__kuota')
  ede = Peminatan.objects.get(peminatancode='EDE')
  eisd = Peminatan.objects.get(peminatancode='EISD')
  sag = Peminatan.objects.get(peminatancode='SAG')
  eim = Peminatan.objects.get(peminatancode='EIM')
  erp = Peminatan.objects.get(peminatancode='ERP')


  for s in seleksi:
    data = Seleksi.objects.get(studentid__numberid=s['numberid'])
    keprof = Keprof.objects.filter(nim=s['numberid'])
    if s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Data Engineering':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(ede.prasyarat1.lower()) + F(ede.prasyarat2.lower()) + F(ede.prasyarat3.lower()) + F(ede.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + bobot.pilihan1
      else:
        data.score1 = bobot.pilihan1
      
      if keprof and keprof[0].keprof == 'EDE' and keprof[0].kategori == 'ASISTEN':
        data.score1 += bobot.asisten
      elif keprof and keprof[0].keprof == 'EDE' and keprof[0].kategori == 'KORDAS':
        data.score1 += bobot.kordas
      elif keprof and keprof[0].keprof == 'EDE' and keprof[0].kategori == 'ANGGOTA':
        data.score1 += bobot.anggota

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Resource Planning':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(erp.prasyarat1.lower()) + F(erp.prasyarat2.lower()) + F(erp.prasyarat3.lower()) + F(erp.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + bobot.pilihan1
      else:
        data.score1 = bobot.pilihan1

      if keprof and keprof[0].keprof == 'ESS' and keprof[0].kategori == 'ASISTEN':
        data.score1 += bobot.asisten
      elif keprof and keprof[0].keprof == 'ESS' and keprof[0].kategori == 'KORDAS':
        data.score1 += bobot.kordas
      elif keprof and keprof[0].keprof == 'ESS' and keprof[0].kategori == 'ANGGOTA':
        data.score1 += bobot.anggota

    elif s['seleksi_student__pilihan1__peminatanname'] == 'System Architecture and Governance':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(sag.prasyarat1.lower()) + F(sag.prasyarat2.lower()) + F(sag.prasyarat3.lower()) + F(sag.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + bobot.pilihan1
      else:
        data.score1 = bobot.pilihan1
      if keprof and keprof[0].keprof == 'SAG' and keprof[0].kategori == 'ASISTEN':
        data.score1 += bobot.asisten
      elif keprof and keprof[0].keprof == 'SAG' and keprof[0].kategori == 'KORDAS':
        data.score1 += bobot.kordas
      elif keprof and keprof[0].keprof == 'SAG' and keprof[0].kategori == 'ANGGOTA':
        data.score1 += bobot.anggota

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Intelligent System Development':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eisd.prasyarat1.lower()) + F(eisd.prasyarat2.lower()) + F(eisd.prasyarat3.lower()) + F(eisd.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + bobot.pilihan1
      else:
        data.score1 = bobot.pilihan1

      if keprof and keprof[0].keprof == 'EISD' and keprof[0].kategori == 'ASISTEN':
        data.score1 += bobot.asisten
      elif keprof and keprof[0].keprof == 'EISD' and keprof[0].kategori == 'KORDAS':
        data.score1 += bobot.kordas
      elif keprof and keprof[0].keprof == 'EISD' and keprof[0].kategori == 'ANGGOTA':
        data.score1 += bobot.anggota

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Infrastructure Management':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eim.prasyarat1.lower()) + F(eim.prasyarat2.lower()) + F(eim.prasyarat3.lower()) + F(eim.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + bobot.pilihan1
      else:
        data.score1 = 0

      if keprof and keprof[0].keprof == 'EIM' and keprof[0].kategori == 'ASISTEN':
        data.score1 += bobot.asisten
      elif keprof and keprof[0].keprof == 'EIM' and keprof[0].kategori == 'KORDAS':
        data.score1 += bobot.kordas
      elif keprof and keprof[0].keprof == 'EIM' and keprof[0].kategori == 'ANGGOTA':
        data.score1 += bobot.anggota

    if s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Data Engineering':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(ede.prasyarat1.lower()) + F(ede.prasyarat2.lower()) + F(ede.prasyarat3.lower()) + F(ede.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Resource Planning':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(erp.prasyarat1.lower()) + F(erp.prasyarat2.lower()) + F(erp.prasyarat3.lower()) + F(erp.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

     

    elif s['seleksi_student__pilihan2__peminatanname'] == 'System Architecture and Governance':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(sag.prasyarat1.lower()) + F(sag.prasyarat2.lower()) + F(sag.prasyarat3.lower()) + F(sag.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0
      
      

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Intelligent System Development':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eisd.prasyarat1.lower()) + F(eisd.prasyarat2.lower()) + F(eisd.prasyarat3.lower()) + F(eisd.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

     

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Infrastructure Management':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eim.prasyarat1.lower()) + F(eim.prasyarat2.lower()) + F(eim.prasyarat3.lower()) + F(eim.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0


    data.save()

  fulldata = Profile.objects.filter(role='MAHASISWA', seleksi_student__batch=latestbatch, peminatan__isnull=True).values('numberid', 'fullname', 'seleksi_student__pilihan1__peminatanname', 'seleksi_student__score1', 'seleksi_student__pilihan2__peminatanname', 'seleksi_student__score2', 'seleksi_student__result').order_by('-seleksi_student__score1')

  return fulldata

def pengaturanapi(request):
  if request.method == 'POST':
    ede = Peminatan.objects.get(peminatancode='EDE')
    eisd = Peminatan.objects.get(peminatancode='EISD')
    sag = Peminatan.objects.get(peminatancode='SAG')
    eim = Peminatan.objects.get(peminatancode='EIM')
    erp = Peminatan.objects.get(peminatancode='ERP')
    bobot = Bobot.objects.get(id=1)

    ede.prasyarat1 = request.POST['EDE1']
    ede.prasyarat2 = request.POST['EDE2']
    ede.prasyarat3 = request.POST['EDE3']
    ede.prasyarat4 = request.POST['EDE4']

    eisd.prasyarat1 = request.POST['EISD1']
    eisd.prasyarat2 = request.POST['EISD2']
    eisd.prasyarat3 = request.POST['EISD3']
    eisd.prasyarat4 = request.POST['EISD4']

    sag.prasyarat1 = request.POST['SAG1']
    sag.prasyarat2 = request.POST['SAG2']
    sag.prasyarat3 = request.POST['SAG3']
    sag.prasyarat4 = request.POST['SAG4']

    eim.prasyarat1 = request.POST['EIM1']
    eim.prasyarat2 = request.POST['EIM2']
    eim.prasyarat3 = request.POST['EIM3']
    eim.prasyarat4 = request.POST['EIM4']

    erp.prasyarat1 = request.POST['ERP1']
    erp.prasyarat2 = request.POST['ERP2']
    erp.prasyarat3 = request.POST['ERP3']
    erp.prasyarat4 = request.POST['ERP4']

    bobot.pilihan1 = request.POST['pilihan1']
    bobot.kordas = request.POST['kordas']
    bobot.asisten = request.POST['asisten']
    bobot.anggota = request.POST['anggota']
    bobot.kuotadosen = request.POST['kuotadosen']


    sag.kuota = Dosen.objects.filter(peminatan='SAG').count() * int(request.POST['kuotadosen'])
    ede.kuota = Dosen.objects.filter(peminatan='EDE').count() * int(request.POST['kuotadosen'])
    eisd.kuota = Dosen.objects.filter(peminatan='EISD').count() * int(request.POST['kuotadosen'])
    eim.kuota = Dosen.objects.filter(peminatan='EIM').count() * int(request.POST['kuotadosen'])
    erp.kuota = Dosen.objects.filter(peminatan='ERP').count() * int(request.POST['kuotadosen'])

    ede.save()
    eisd.save()
    sag.save()
    eim.save()
    erp.save()
    bobot.save()
    return redirect('pengaturan')