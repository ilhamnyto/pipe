from django.db.models.expressions import  F
from pipeapp.models import Batch, Dosen, Keprof, Nilai, Peminatan, Profile, Seleksi, StatusServer, TukarPeminatan
from django.shortcuts import render
from .decorator import login_required, is_authenticated, role_required, daftarlist, diterimalist, rasiolist
from django.db.models import Q, Count
import pandas as pd
from .dburl import engine

# Create your views here.

@is_authenticated()
def index(request):
  return render(request, 'index.html')

@login_required()
def home(request):
  user = Profile.objects.get(username=request.session['user_login'])
  login = StatusServer.objects.get(name='Login') 
  
  if user.role == 'DOSEN' or user.role == 'DOSEN PEMBINA':
    mahasiswa = Profile.objects.filter(Q(role='MAHASISWA') & Q(peminatan=user.peminatan)).count()
    dosen = Dosen.objects.filter(peminatan=user.peminatan).count()
    return render(request, 'home.html', {'user': user, "login": login, "mahasiswa": mahasiswa, "dosen": dosen})
  elif user.role == 'ADMIN':
    mahasiswa = Profile.objects.filter(role='MAHASISWA').count()
    dosen = Dosen.objects.count()
    peminatan = Peminatan.objects.count()
    return render(request, 'home.html', {'user': user, "login": login,"mahasiswa": mahasiswa, "dosen": dosen, "peminatan": peminatan})
  else:
    return render(request, 'home.html', {'user': user})

# mahasiswa

@login_required()
@role_required(allowed_roles=['MAHASISWA'])
def daftar(request):
  user = Profile.objects.get(username=request.session['user_login'])
  peminatan = Peminatan.objects.all()
  batch = Batch.objects.last()
  seleksistatus = Seleksi.objects.filter(studentid=user)
  serverstatus = StatusServer.objects.get(name='Batch Pendaftaran')
  return render(request, 'daftar.html', {'user': user, 'peminatan': peminatan, 'batch': batch, 'seleksistatus': seleksistatus, "serverstatus": serverstatus})

# admin

@login_required()
@role_required(allowed_roles=['ADMIN'])
def datadosen(request):
  user = Profile.objects.get(username=request.session['user_login'])
  dosenlist = Dosen.objects.all()
  return render(request, 'datadosen.html', {'user': user, "dosenlist": dosenlist})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def datakeprof(request):
  user = Profile.objects.get(username=request.session['user_login'])
  keproflist = Keprof.objects.all()
  return render(request, 'datakeprof.html', {'user': user, "keproflist": keproflist})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def datamahasiswa(request):
  user = Profile.objects.get(username=request.session['user_login'])
  nilailist = Nilai.objects.all()
  return render(request, 'datamahasiswa.html', {'user': user, "nilailist": nilailist})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def datapeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  peminatanlist = Peminatan.objects.all()
  return render(request, 'datapeminatan.html', {'user': user, "peminatanlist": peminatanlist})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def tambahdosen(request):
  user = Profile.objects.get(username=request.session['user_login'])
  return render(request, 'tambahdosen.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def tambahkeprof(request):
  user = Profile.objects.get(username=request.session['user_login'])
  return render(request, 'tambahkeprof.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def tambahmahasiswa(request):
  user = Profile.objects.get(username=request.session['user_login'])
  return render(request, 'tambahmahasiswa.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def tambahpeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  return render(request, 'tambahpeminatan.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def editdosen(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  dosen = Dosen.objects.filter(id=id)
  if dosen:
    return render(request, 'tambahdosen.html', {'user': user, "dosen": dosen[0]})
  else:  
    return render(request, 'tambahdosen.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def editkeprof(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  keprof = Keprof.objects.filter(id=id)
  if keprof:
    return render(request, 'tambahkeprof.html', {'user': user, "keprof": keprof[0]})
  else:  
    return render(request, 'tambahkeprof.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def editmahasiswa(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  nilai = Nilai.objects.filter(id=id)
  if nilai:
    return render(request, 'tambahmahasiswa.html', {'user': user, "nilai": nilai[0]})
  else:  
    return render(request, 'tambahmahasiswa.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def editpeminatan(request, peminatancode):
  user = Profile.objects.get(username=request.session['user_login'])
  peminatan = Peminatan.objects.filter(peminatancode=id)
  if peminatan:
    return render(request, 'tambahpeminatan.html', {'user': user, "peminatan": peminatan[0]})
  else:  
   return render(request, 'tambahpeminatan.html', {'user': user})
  

@login_required()
@role_required(allowed_roles=['ADMIN'])
def seleksipeminatan(request):
  user = Profile.objects.get(username=request.session['user_login'])
  batchstatus = StatusServer.objects.get(name='Batch Pendaftaran')
  latestbatch = Batch.objects.last()
  batchdata = Seleksi.objects.values('batch__batchnum').annotate(mahasiswa=Count('studentid')).order_by()
  print(batchdata)
  return render(
    request, 'seleksipeminatan.html', {'user': user, "batchstatus": batchstatus, 
    "latestbatch": latestbatch.batchnum, "minbatch": (latestbatch.batchnum + 1),
    "batchdata": batchdata
    })

@login_required()
@role_required(allowed_roles=['ADMIN'])
def hasilseleksi(request):
  user = Profile.objects.get(username=request.session['user_login'])
  seleksiresult = pd.read_sql('SELECT * FROM "pipeapp_seleksi"', con=engine)
  pilihan1 = seleksiresult.groupby(['pilihan1_id']).size().reset_index(name='counts')
  pilihan1.columns = ['pilihan', 'counts']
  pilihan2 = seleksiresult.groupby(['pilihan2_id']).size().reset_index(name='counts')
  pilihan2.columns = ['pilihan', 'counts']
  pendaftar = pd.concat([pilihan1, pilihan2]).groupby(['pilihan']).sum().reset_index()
  persen1 = seleksiresult.groupby(['pilihan1_id']).size().reset_index(name='counts')['counts'] / len(seleksiresult) * 100
  persen2 = seleksiresult.groupby(['pilihan2_id']).size().reset_index(name='counts')['counts'] / len(seleksiresult) * 100
  diterima = seleksiresult.groupby(['result_id']).size().reset_index(name='counts')

  peminatan = pd.DataFrame({
    "Peminatan": diterima['result_id'],
    "Jumlah Pendaftar": pendaftar['counts'],
    "Jumlah Pilihan 1": pilihan1['counts'],
    "Jumlah Pilihan 2": pilihan2['counts'],
    "Pilihan 1": persen1.map('{}%'.format),
    "Pilihan 2": persen2.map('{}%'.format),
  })
  peminatan.index += 1 
  peminatan['No.'] = list(peminatan.index)
  peminatan = peminatan[['No.', 'Peminatan', 'Jumlah Pendaftar', 'Jumlah Pilihan 1', 'Jumlah Pilihan 2', 'Pilihan 1', 'Pilihan 2']]

  
  keahlian = pd.DataFrame({
    "Kelompok Keahlian": ['Cybernatics', 'EIS'],
    "Jumlah Peminat": daftarlist(pendaftar),
    "Jumlah Diterima": diterimalist(diterima),
    "Rasio": rasiolist(pendaftar, diterima)
  })
  result = Seleksi.objects.all()

  return render(request, 'hasilseleksi.html', {'user': user, "result": result, 
  "peminatan": peminatan.to_html(index=False, justify='left', classes='table borderless', table_id='tablepeminatan', border=0),
  "keahlian": keahlian.to_html(index=False, justify='left', classes='table borderless', table_id='tablekk', border=0)
  })

@login_required()
@role_required(allowed_roles=['ADMIN'])
def penghitungannilai(request):
  latestbatch = Batch.objects.last()
  user = Profile.objects.get(username=request.session['user_login'])
  seleksi = Profile.objects.filter(role='MAHASISWA', seleksi_student__batch=latestbatch).values('numberid', 'fullname', 'seleksi_student__pilihan1__peminatanname', 'seleksi_student__pilihan1__kuota', 'seleksi_student__pilihan2__peminatanname', 'seleksi_student__pilihan2__kuota')
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
        data.score1 = nilai[0]['nilai'] + 1
      else:
        data.score1 = 0
      
      if keprof and keprof[0].keprof == 'DASPRO':
        data.score1 += 2

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Resource Planning':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(erp.prasyarat1.lower()) + F(erp.prasyarat2.lower()) + F(erp.prasyarat3.lower()) + F(erp.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + 1
      else:
        data.score1 = 0

      if keprof and keprof[0].keprof == 'ERP':
        data.score1 += 2

    elif s['seleksi_student__pilihan1__peminatanname'] == 'System Architecture and Governance':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(sag.prasyarat1.lower()) + F(sag.prasyarat2.lower()) + F(sag.prasyarat3.lower()) + F(sag.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + 1
      else:
        data.score1 = 0

      if keprof and keprof[0].keprof == 'SAG':
        data.score1 += 2

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Intelligent System Development':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eisd.prasyarat1.lower()) + F(eisd.prasyarat2.lower()) + F(eisd.prasyarat3.lower()) + F(eisd.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + 1
      else:
        data.score1 = 0

      if keprof and keprof[0].keprof == 'EISD':
        data.score1 += 2

    elif s['seleksi_student__pilihan1__peminatanname'] == 'Enterprise Infrastructure Management':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eim.prasyarat1.lower()) + F(eim.prasyarat2.lower()) + F(eim.prasyarat3.lower()) + F(eim.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score1 = nilai[0]['nilai'] + 1
      else:
        data.score1 = 0

      if keprof and keprof[0].keprof == 'SISJAR':
        data.score1 += 2

    if s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Data Engineering':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(ede.prasyarat1.lower()) + F(ede.prasyarat2.lower()) + F(ede.prasyarat3.lower()) + F(ede.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      if keprof and keprof[0].keprof == 'DASPRO':
        data.score2 += 2

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Resource Planning':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(erp.prasyarat1.lower()) + F(erp.prasyarat2.lower()) + F(erp.prasyarat3.lower()) + F(erp.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      if keprof and keprof[0].keprof == 'ERP':
        data.score2 += 2

    elif s['seleksi_student__pilihan2__peminatanname'] == 'System Architecture and Governance':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(sag.prasyarat1.lower()) + F(sag.prasyarat2.lower()) + F(sag.prasyarat3.lower()) + F(sag.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      if keprof and keprof[0].keprof == 'SAG':
        data.score2 += 2

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Intelligent System Development':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eisd.prasyarat1.lower()) + F(eisd.prasyarat2.lower()) + F(eisd.prasyarat3.lower()) + F(eisd.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      if keprof and keprof[0].keprof == 'EISD':
        data.score2 += 2

    elif s['seleksi_student__pilihan2__peminatanname'] == 'Enterprise Infrastructure Management':
      nilai = Nilai.objects.filter(Q(nim=s['numberid'])).annotate(nilai=F(eim.prasyarat1.lower()) + F(eim.prasyarat2.lower()) + F(eim.prasyarat3.lower()) + F(eim.prasyarat4.lower())).values('nilai')
      if nilai and nilai[0]:
        data.score2 = nilai[0]['nilai']
      else:
        data.score2 = 0

      if keprof and keprof[0].keprof == 'EIM':
        data.score2 += 2

    data.save()

  fulldata = Profile.objects.filter(role='MAHASISWA', seleksi_student__batch=latestbatch).values('numberid', 'fullname', 'seleksi_student__pilihan1__peminatanname', 'seleksi_student__score1', 'seleksi_student__pilihan2__peminatanname', 'seleksi_student__score2', 'seleksi_student__result').order_by('-seleksi_student__score1')
  
  return render(request, 'penghitungannilai.html', {'user': user, "latestbatch": latestbatch, "seleksi": fulldata})


# mahasiswa dan dosen

@login_required()
@role_required(allowed_roles=['MAHASISWA', 'DOSEN'])
def pindah(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if user.role == 'MAHASISWA':
    tukar = TukarPeminatan.objects.filter(Q(mahasiswa1=user) or Q(mahasiswa2=user))
    users = Profile.objects.filter(role='MAHASISWA').exclude(Q(username=user.username) and Q(peminatan=user.peminatan))
    userdata = {}
    for u in list(users):
      if u.peminatan:
        userdata["{0} - {1}".format(u.fullname, u.peminatan.peminatanname)] = u.fullname
      else:
        userdata["{0} - {1}".format(u.fullname, 'Belum ada peminatan')] = u.fullname

    
    return render(request, 'pindah.html', {"user": user, "userdata": userdata, "tukar": tukar})
  else:
    tukaran = TukarPeminatan.objects.filter(Q(mahasiswa1__peminatan=user.peminatan) | (Q(mahasiswa2__peminatan=user.peminatan) and ~Q(status="Pengajuan I"))).order_by('-created_at')
    print(tukaran)
    return render(request, 'pindah.html', {"user": user, "tukaran": tukaran})
# dosen dan admin

@login_required()
@role_required(allowed_roles=['DOSEN', 'DOSEN PEMBINA', 'ADMIN'])
def bidashboard(request):
  user = Profile.objects.get(username=request.session['user_login'])
  return render(request, 'bidashboard.html', {'user': user})

@login_required()
@role_required(allowed_roles=['DOSEN', 'DOSEN PEMBINA', 'ADMIN'])
def bidata(request):
  user = Profile.objects.get(username=request.session['user_login'])

  return render(request, 'bidata.html', {'user': user})

@login_required()
@role_required(allowed_roles=['DOSEN', 'DOSEN PEMBINA', 'ADMIN'])
def binilai(request):
  user = Profile.objects.get(username=request.session['user_login'])

  return render(request, 'binilai.html', {'user': user})

