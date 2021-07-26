
import json
from pipeapp.models import Profile
from django.shortcuts import redirect, render
import pandas as pd
import re
from django.http import JsonResponse
from .dburl import engine


def uploadfile(request):
  user = Profile.objects.get(username=request.session['user_login'])
  if request.method == "POST":
    # try:
      datamahasiswa = pd.read_csv(request.FILES['datamahasiswa'])
      dosen = pd.read_csv(request.FILES['datadosen'])
      d_mahasiswa = datamahasiswa.filter(['nim', 'nama', 'kelas'])
      d_mahasiswa.columns = ['student_id', 'student_name', 'kelas']

      d_tahunakademik = pd.DataFrame(columns=['acad_id', 'acad_year'])
      angkatan = str(request.POST['angkatan'])
      acadid = re.sub("20", "", angkatan)
      d_tahunakademik = d_tahunakademik.append({"acad_id": f'{acadid}{str(int(acadid)+1)}' , "acad_year": angkatan}, ignore_index=True)

      def codeNaming(peminatan):
        if peminatan == 'Enterprise Intelligent System Development':
          return 'EISD'
        elif peminatan == 'Enterprise Data Engineering':
          return 'EDE'
        elif peminatan == 'Enterprise Resource Planning':
          return 'ERP'
        elif peminatan == 'System Architecture and Governance':
          return 'SAG'
        elif peminatan == 'Enterprise Infrastructure Management':
          return 'EIM'

      d_peminatan = pd.DataFrame({
          "peminatan_id": list(map(codeNaming, list(datamahasiswa['peminatan'].unique()))),
          "peminatan_name": list(datamahasiswa['peminatan'].unique())
      })

      d_keahlian = pd.DataFrame({
          "keahlian_id": ['CYBERNETICS', 'EIS'],
          "keahlian_name": ['CYBERNETICS', 'ENTERPRISE AND INDUSTRIAL SYSTEM']
      })

      def keahlianNaming(peminatan):
        if peminatan == 'Enterprise Intelligent System Development' or peminatan == 'Enterprise Data Engineering':
          return 'CYBERNETICS'
        elif peminatan == 'Enterprise Resource Planning' or peminatan == 'System Architecture and Governance' or peminatan == 'Enterprise Infrastructure Management':
          return 'EIS'

      seleksi = datamahasiswa.groupby(['peminatan']).size().reset_index(name='counts')
      seleksi.columns = ['peminatan', 'jumlah_mahasiswa']
      jumlahdosen = dosen.groupby(['Peminatan']).size().reset_index(name='counts')
      jumlahdosen.columns = ['peminatan', 'jumlah_dosen']
      jumlahdosen['jumlah_kuota'] = jumlahdosen['jumlah_dosen'] * 10

      seleksi = seleksi.merge(jumlahdosen, on='peminatan')
      f_seleksi = pd.DataFrame({
          "peminatan_id": list(map(codeNaming, list(seleksi['peminatan'].unique()))),
          "keahlian_id": list(map(keahlianNaming, list(seleksi['peminatan'].unique()))),
          "jumlah_mahasiswa": seleksi['jumlah_mahasiswa'],
          "jumlah_dosen": seleksi['jumlah_dosen'],
          "jumlah_kuota": seleksi['jumlah_kuota'],
      })
      f_seleksi['acad_id'] = f'{acadid}{str(int(acadid)+1)}' 

      nilailist = datamahasiswa.drop(['nim', 'nama', 'peminatan', 'peminatan_1', 'peminatan_2', 'kelas'], axis=1)

      def courseNaming(course):
        if course == 'oop' :
          return 'Pemrograman Berorientasikan Objek'
        if course == 'rpb' :
          return 'Rekayasa Proses Bisnis'
        if course == 'pi' :
          return 'Perancangan Interaksi'
        if course == 'apsi' :
          return 'Analisis dan Perancangan Interaksi'
        if course == 'web' :
          return 'Pengembangan Aplikasi Website'
        if course == 'statistik' :
          return 'Statistika Industri'
        if course == 'matdis' :
          return 'Matematika Diskrit'
        if course == 'alpro' :
          return 'Algoritma Pemrograman'
        if course == 'strukdat' :
          return 'Struktur Data'
        if course == 'se' :
          return 'Sistem Enterprise'
        if course == 'po' :
          return 'Perilaku Organisasi'
        if course == 'scm' :
          return 'Manaajemen Rantai Pasok'
        if course == 'ea' :
          return 'Arsitektur Enterprise'
        if course == 'basdat' :
          return 'Sistem Basis Data'
        if course == 'manjarkom' :
          return 'Manahemen Jaringan Komputer'
        if course == 'sisop' :
          return 'Sistem Operasi'
        if course == 'msdm' :
          return 'Manajemen Sumber Daya Manusia'
        if course == 'desjar' :
          return 'Desain Jaringan'
        if course == 'manprosi' :
          return 'Manajemen Proyek Sistem Informasi'
      
      d_course = pd.DataFrame({
          'course_id': list(nilailist.columns),
          'course_name': list(map(courseNaming, list(nilailist.columns)))
      })

      def nilaiMapping(nilai):
        if nilai == 0:
          return 'grade_E'
        if nilai == 1:
          return 'grade_D'
        if nilai == 2:
          return 'grade_C'
        if nilai == 2.5:
          return 'grade_BC'
        if nilai == 3:
          return 'grade_B'
        if nilai == 3.5:
          return 'grade_AB'
        if nilai == 4:
          return 'grade_A'
      
      for score in list(nilailist.columns):
        nilailist[score] = list(map(nilaiMapping, list(nilailist[score])))
      f_list = pd.DataFrame(columns=['course_id', 'acad_id', 'grade_A', 'grade_AB', 'grade_B', 'grade_BC', 'grade_C', 'grade_D', 'grade_E'])


      for score in list(nilailist.columns):
        n = nilailist.groupby([score]).size().reset_index(name='counts')
        n['id'] = 'a'
        n = n.pivot(index='id', columns=score, values='counts')
        n['course_id'] = score
        n['acad_id'] = f'{acadid}{str(int(acadid)+1)}'
        f_list = f_list.append(n)

      f_list = f_list.fillna(0)

      check_seleksi = pd.read_sql('SELECT * FROM "F_Seleksi"', con=engine)
      check_peminatan = pd.read_sql('SELECT * FROM "D_Peminatan"', con=engine)
      check_keahlian = pd.read_sql('SELECT * FROM "D_Keahlian"', con=engine)
      check_acad = pd.read_sql('SELECT * FROM "D_Acad_Year"', con=engine)
      check_course = pd.read_sql('SELECT * FROM "D_Course"', con=engine)
      check_score = pd.read_sql('SELECT * FROM "F_Nilai"', con=engine)

      in_seleksi = f_seleksi[(~f_seleksi.peminatan_id.isin(check_seleksi.peminatan_id)) & (~f_seleksi.keahlian_id.isin(check_seleksi.keahlian_id))]
      in_peminatan = d_peminatan[~d_peminatan.peminatan_id.isin(check_peminatan.peminatan_id)]
      in_keahlian = d_keahlian[~d_keahlian.keahlian_id.isin(check_keahlian.keahlian_id)]
      in_acad = d_tahunakademik[~d_tahunakademik.acad_id.isin(check_acad.acad_id)]
      in_course = d_course[~d_course.course_id.isin(check_course.course_id)]
      in_nilai = f_list[(~f_list.acad_id.isin(check_score.acad_id)) & (~f_list.course_id.isin(check_score.course_id))]

      in_keahlian.to_sql('D_Keahlian', con=engine, index=False, if_exists="append", method='multi')
      in_peminatan.to_sql('D_Peminatan', con=engine, index=False, if_exists="append", method='multi')
      in_acad.to_sql('D_Acad_Year', con=engine, index=False, if_exists="append", method='multi')
      in_course.to_sql('D_Course', con=engine, index=False, if_exists="append", method='multi')
      in_seleksi.to_sql('F_Seleksi', con=engine, index=False, if_exists="append", method='multi')
      in_nilai.to_sql('F_Nilai', con=engine, index=False, if_exists="append", method='multi')

      return redirect('bidata')
    # except Exception:
    #   return render(request, 'bidata.html', {'user': user, "message": "File tidak sesuai dengan ketentuan."})


def getdatapeminatan(request):
  seleksi = pd.read_sql('SELECT * FROM "F_Seleksi"', con=engine)
  seleksilist = json.loads(seleksi.to_json(orient="records"))
  resp = {}
  for sl in seleksilist:
    resp[sl['peminatan_id']] = {
      "mahasiswa": sl['jumlah_mahasiswa'],
      "dosen": sl['jumlah_dosen'],
      "kuota": sl['jumlah_kuota'],
      "bimbingan": f"{sl['jumlah_mahasiswa'] / sl['jumlah_dosen']:.1f}"
    }
  return JsonResponse(resp, safe=False)

def getdataoverall(request):
  seleksi = pd.read_sql('SELECT * FROM "F_Seleksi"', con=engine)
  keahlian = seleksi.filter(['keahlian_id', 'jumlah_dosen']).groupby(['keahlian_id']).sum().reset_index()
  seleksilist = json.loads(seleksi.to_json(orient="records"))
  keahlianlist = json.loads(keahlian.to_json(orient="records"))
  print(keahlian)
  dosenpeminatan = {}
  dosenkeahlian = {}
  kuotamahasiswa = {}
    
  for dosen in seleksilist:
    dosenpeminatan[dosen['peminatan_id']] = dosen['jumlah_dosen']
    kuotamahasiswa[dosen['peminatan_id']] = {
      "mahasiswa": dosen['jumlah_mahasiswa'],
      "kuota": dosen['jumlah_kuota']
    }

  for dosen in keahlianlist:
    dosenkeahlian[dosen['keahlian_id']] = dosen['jumlah_dosen']

  
  return JsonResponse({"dosenpeminatan" : dosenpeminatan,"dosenkeahlian" : dosenkeahlian,  "kuotamahasiswa": kuotamahasiswa}, safe=False)

def getdatanilai(request):
  nilai = pd.read_sql('SELECT * FROM "F_Nilai"', con=engine)
  nilailist = json.loads(nilai.to_json(orient="records"))
  overall = nilai.drop(['course_id', 'acad_id'], axis=1).sum(axis=0)
  resp = {}
  for score in nilailist:
    resp[score['course_id']] = {
      "A": score['grade_A'],
      "AB": score['grade_AB'],
      "B": score['grade_B'],
      "BC": score['grade_BC'],
      "C": score['grade_C'],
      "D": score['grade_D'],
      "E": score['grade_E'],
    }
    
    resp['all'] = {
        "A": int(overall['grade_A']),
      "AB": int(overall['grade_AB']),
      "B": int(overall['grade_B']),
      "BC": int(overall['grade_BC']),
      "C": int(overall['grade_C']),
      "D": int(overall['grade_D']),
      "E": int(overall['grade_E']),
    }

  return JsonResponse(resp, safe=False)

  