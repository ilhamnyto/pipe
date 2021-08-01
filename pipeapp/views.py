from pipeapp.seleksi import hitung
from pipeapp.models import Batch, Dosen, Keprof, Nilai, Peminatan, Profile, Seleksi, StatusServer, TukarPeminatan
from django.shortcuts import redirect, render
from .decorator import login_required, is_authenticated, role_required
from django.db.models import Q, Count


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
  peminatan = Peminatan.objects.filter(peminatancode=peminatancode)
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

  return render(
    request, 'seleksipeminatan.html', {'user': user, "batchstatus": batchstatus, 
    "latestbatch": latestbatch.batchnum,
    "batchdata": batchdata
    })

@login_required()
@role_required(allowed_roles=['ADMIN'])
def hasilseleksi(request):
  latestbatch = Batch.objects.last()
  return redirect(f'/hasil-seleksi/{latestbatch.id}')


@login_required()
@role_required(allowed_roles=['ADMIN'])
def seleksiresult(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  latestbatch = Batch.objects.filter(id=id)
  if latestbatch:

    result = Seleksi.objects.filter(batch=latestbatch[0])
    batch = Batch.objects.all().exclude(id=latestbatch[0].id)
    peminatan = Seleksi.objects.filter(batch=latestbatch[0]).select_related('result').values('result').annotate(count=Count('studentid')).values('result', 'count', 'result__kuota').order_by()
    print(peminatan)
    return render(request, 'hasilseleksi.html', {'user': user, "result": result, 'allbatch': batch, 'latest': latestbatch[0], "peminatan":peminatan})
  else:
    return render(request, 'hasilseleksi.html', {'user': user})

@login_required()
@role_required(allowed_roles=['ADMIN'])
def penghitungannilai(request):
  latestbatch = Batch.objects.last()
  return redirect(f'/penghitungan-nilai/{latestbatch.id}')

@login_required()
@role_required(allowed_roles=['ADMIN'])
def hitungnilai(request, id):
  user = Profile.objects.get(username=request.session['user_login'])
  latestbatch = Batch.objects.filter(id=id)
  if latestbatch:
    batch = Batch.objects.all().exclude(id=latestbatch[0].id)
    fulldata = hitung(request, latestbatch[0])
    return render(request, 'penghitungannilai.html', {'user': user, "seleksi": fulldata, 'allbatch': batch, 'latest': latestbatch[0]})
  else:
    return render(request, 'penghitungannilai.html', {'user': user})

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

