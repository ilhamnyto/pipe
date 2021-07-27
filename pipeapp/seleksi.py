from .models import Batch, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count

def daftarpeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if request.method == 'POST':
    if request.POST['pilihan1'] == request.POST['pilihan2']:
      peminatan = Peminatan.objects.all()
      batch = Batch.objects.last()
      seleksistatus = Seleksi.objects.filter(studentid=user.numberid)
      serverstatus = StatusServer.objects.get(name='Batch Pendaftaran')
      return render(request, 'daftar.html', {'user': user, 'peminatan': peminatan, 'batch': batch, 'seleksistatus': seleksistatus, "serverstatus": serverstatus, 'error': True})
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

def pengajuanpindah(request):
  if 'reset' in request.POST:
    mahasiswa1 = Profile.objects.get(username=request.session['user_login'])
    TukarPeminatan.objects.get(Q(mahasiswa1=mahasiswa1) or Q(mahasiswa2=mahasiswa1)).delete()
    return redirect('pindah')
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

    return redirect('pindah')

def pengajuankedosen(request):
  tukar = TukarPeminatan.objects.get(id=request.POST['tukarid'])
  if request.method == 'POST':
    if request.POST['status'] == 'Pengajuan I' and request.POST['decision'] == 'approve':
      tukar.status = 'Pengajuan II'
      tukar.save()
      return redirect('pindah')
    elif request.POST['status'] == 'Pengajuan I' and request.POST['decision'] == 'decline':
      tukar.status = 'Ditolak I'
      tukar.save()
      return redirect('pindah')
    elif request.POST['status'] == 'Pengajuan II' and request.POST['decision'] == 'approve':
      tukar.status = 'Disetujui'
      tukar.save()
      return redirect('pindah')
    elif request.POST['status'] == 'Pengajuan II' and request.POST['decision'] == 'decline':
      tukar.status = 'Ditolak II'
      tukar.save()
      return redirect('pindah')
    return redirect('pindah')

def statusbatch(request):
  status = StatusServer.objects.get(name='Batch Pendaftaran')
  if request.method == 'POST':
    if request.POST['status'] == 'enable':
      print(request.POST['status'])
      status.isAvailable = True
      status.save()
      return redirect('seleksipeminatan')
    else:
      print(request.POST['status'])
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

def plotting(request):
  if request.method == 'POST':
    seleksi = Seleksi.objects.all().order_by('-score1')
    for s in seleksi:
      if s.score1 <= 0.0 and s.score2 <= 0.0 :
        pass
      elif list(seleksi).index(s) + 1 > s.pilihan1.kuota:
        data = Seleksi.objects.get(studentid=s.studentid)
        data.result = s.pilihan2
        data.save()
      else:
        data = Seleksi.objects.get(studentid=s.studentid)
        data.result = s.pilihan1
        data.save()

    return redirect('penghitungannilai')