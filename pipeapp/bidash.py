
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
    try:
      datamahasiswa = pd.read_csv(request.FILES['datamahasiswa'])
      dosen = pd.read_csv(request.FILES['datadosen'])
      
      d_tahunakademik = pd.DataFrame(columns=['acad_id', 'acad_year'])
      tahun = list(datamahasiswa['tahun'].unique())
      regextahun = list(map(lambda x: re.sub("20", "", str(x)), tahun))
      d_tahunakademik = pd.DataFrame({
          "acad_id": list(map(lambda x: f'{x}{str(int(x)+1)}', regextahun)),
          "acad_year": tahun
      })

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

      def keahlianNaming(peminatan):
        if peminatan == 'Enterprise Intelligent System Development' or peminatan == 'Enterprise Data Engineering':
          return 'CYBERNETICS'
        elif peminatan == 'Enterprise Resource Planning' or peminatan == 'System Architecture and Governance' or peminatan == 'Enterprise Infrastructure Management':
          return 'EINS'

      d_peminatan = pd.DataFrame({
          "peminatan_id": list(map(codeNaming, list(datamahasiswa['PEMINATAN'].unique()))),
          "peminatan_name": list(datamahasiswa['PEMINATAN'].unique()),
          "kelompok_keahlian": list(map(keahlianNaming, list(datamahasiswa['PEMINATAN'].unique())))
      })

      seleksi = datamahasiswa.groupby(['PEMINATAN']).size().reset_index(name='counts')
      seleksi.columns = ['peminatan', 'jumlah_mahasiswa']

      jumlahdosen = dosen.groupby(['Peminatan']).size().reset_index(name='counts')
      jumlahdosen.columns = ['peminatan', 'jumlah_dosen']
      jumlahdosen['jumlah_kuota'] = jumlahdosen['jumlah_dosen'] * 10

      seleksi = seleksi.merge(jumlahdosen, on='peminatan')
      f_seleksi = pd.DataFrame(columns=['peminatan_id', 'acad_id', 'jumlah_mahasiswa', 'jumlah_kuota', 'jumlah_dosen'])

      for year in list(datamahasiswa['tahun'].unique()):
        seleksi = datamahasiswa[datamahasiswa['tahun'] == year].groupby(['PEMINATAN']).size().reset_index(name='counts')
        seleksi.columns = ['peminatan', 'jumlah_mahasiswa']

        jumlahdosen = dosen[dosen['tahun'] == year].groupby(['Peminatan']).size().reset_index(name='counts')
        jumlahdosen.columns = ['peminatan', 'jumlah_dosen']
        jumlahdosen['jumlah_kuota'] = jumlahdosen['jumlah_dosen'] * 10

        seleksi = seleksi.merge(jumlahdosen, on='peminatan')

        outp = pd.DataFrame({
          "peminatan_id": list(map(codeNaming, list(seleksi['peminatan'].unique()))),
          "jumlah_mahasiswa": seleksi['jumlah_mahasiswa'],
          "jumlah_dosen": seleksi['jumlah_dosen'],
          "jumlah_kuota": seleksi['jumlah_kuota'],
        })
        year = re.sub("20", "", str(year))
        outp['acad_id'] = f'{year}{str(int(year)+1)}'

        f_seleksi = f_seleksi.append(outp)

      matkul = datamahasiswa.drop(['NIM', 'NAMA', 'PEMINATAN'], axis=1)
      nilailist = datamahasiswa.drop(['NIM', 'NAMA', 'PEMINATAN', 'tahun'], axis=1)

      def courseNaming(course):
        if course == 'OOP' :
          return 'Pemrograman Berorientasikan Objek'
        if course == 'RPB' :
          return 'Rekayasa Proses Bisnis'
        if course == 'RPL' :
          return 'Rekayasa Perangkat Lunak'
        if course == 'PI' :
          return 'Perancangan Interaksi'
        if course == 'APSI' :
          return 'Analisis dan Perancangan Interaksi'
        if course == 'WEB' :
          return 'Pengembangan Aplikasi Website'
        if course == 'Statistik' :
          return 'Statistika Industri'
        if course == 'Matdis' :
          return 'Matematika Diskrit'
        if course == 'Alpro' :
          return 'Algoritma dan Pemrograman'
        if course == 'Strukdat' :
          return 'Struktur Data'
        if course == 'SE' :
          return 'Sistem Enterprise'
        if course == 'PO' :
          return 'Perilaku Organisasi'
        if course == 'SCM' :
          return 'Manaajemen Rantai Pasok'
        if course == 'EA' :
          return 'Arsitektur Enterprise'
        if course == 'BASDAT' :
          return 'Sistem Basis Data'
        if course == 'MANJARKOM' :
          return 'Manahemen Jaringan Komputer'
        if course == 'SISOP' :
          return 'Sistem Operasi'
        if course == 'MSDM' :
          return 'Manajemen Sumber Daya Manusia'
        if course == 'DESJAR' :
          return 'Desain Jaringan'
        if course == 'KSI' :
          return 'Keamanan Sistem Informasi'

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

      for score in list(matkul.columns):
        if score != 'tahun':
          matkul[score] = list(map(nilaiMapping, list(matkul[score])))
      
      f_list = pd.DataFrame(columns=['course_id', 'acad_id', 'grade_A', 'grade_AB', 'grade_B', 'grade_BC', 'grade_C', 'grade_D', 'grade_E'])

      for year in list(matkul['tahun'].unique()):
        scorelist = matkul[matkul['tahun'] == year]
        scorelist = scorelist.drop(['tahun'], axis=1)
        for score in list(scorelist.columns):
          n = scorelist.groupby([score]).size().reset_index(name='counts')
          n['id'] = 'a'
          n = n.pivot(index='id', columns=score, values='counts')
          n['course_id'] = score
          year = re.sub("20", "", str(year))
          n['acad_id'] = f'{year}{str(int(year)+1)}'
          f_list = f_list.append(n)
      
      f_list = f_list.fillna(0)


      check_seleksi = pd.read_sql('SELECT * FROM "F_Seleksi"', con=engine)
      check_peminatan = pd.read_sql('SELECT * FROM "D_Peminatan"', con=engine)
      check_acad = pd.read_sql('SELECT * FROM "D_Acad_Year"', con=engine)
      check_course = pd.read_sql('SELECT * FROM "D_Course"', con=engine)
      check_score = pd.read_sql('SELECT * FROM "F_Nilai"', con=engine)

      in_seleksi = f_seleksi[(~f_seleksi.peminatan_id.isin(check_seleksi.peminatan_id)) & (~f_seleksi.acad_id.isin(check_seleksi.acad_id))]
      in_peminatan = d_peminatan[~d_peminatan.peminatan_id.isin(check_peminatan.peminatan_id)]
      in_acad = d_tahunakademik[~d_tahunakademik.acad_id.isin(check_acad.acad_id)]
      in_course = d_course[~d_course.course_id.isin(check_course.course_id)]
      in_nilai = f_list[(~f_list.acad_id.isin(check_score.acad_id)) & (~f_list.course_id.isin(check_score.course_id))]

      in_peminatan.to_sql('D_Peminatan', con=engine, index=False, if_exists="append", method='multi')
      in_acad.to_sql('D_Acad_Year', con=engine, index=False, if_exists="append", method='multi')
      in_course.to_sql('D_Course', con=engine, index=False, if_exists="append", method='multi')
      in_seleksi.to_sql('F_Seleksi', con=engine, index=False, if_exists="append", method='multi')
      in_nilai.to_sql('F_Nilai', con=engine, index=False, if_exists="append", method='multi')

      return render(request, 'bidata.html', {'user': user, "message": "Proses ETL berhasil dilakukan."})
    except Exception:
      return render(request, 'bidata.html', {'user': user, "error": "File tidak sesuai dengan ketentuan."})



def getdataoverall(request):
  seleksi = pd.read_sql('SELECT * FROM "F_Seleksi" INNER JOIN "D_Peminatan" ON "F_Seleksi".peminatan_id="D_Peminatan".peminatan_id INNER JOIN "D_Acad_Year" ON "F_Seleksi".acad_id="D_Acad_Year".acad_id', con=engine)
  seleksi = seleksi.loc[:,~seleksi.columns.duplicated()]
  resp = {}
  for year in list(seleksi['acad_year'].unique()):
    data = json.loads(seleksi[seleksi['acad_year'] == year].to_json(orient="records"))
    resp[year] = {}
    for peminatan in data:
      resp[year].update(
      { peminatan['peminatan_id']: 
                { 
                  "keahlian": peminatan['kelompok_keahlian'],
                  "mahasiswa": peminatan['jumlah_mahasiswa'],
                  "kuota": peminatan['jumlah_kuota'],
                  "dosen": peminatan['jumlah_dosen'],
                }
      }
      )

  return JsonResponse(resp, safe=False)

def getdatanilai(request):
  nilai = pd.read_sql('SELECT * FROM "F_Nilai" INNER JOIN "D_Acad_Year" ON "F_Nilai".acad_id = "D_Acad_Year".acad_id', con=engine)
  nilai = nilai.loc[:,~nilai.columns.duplicated()]
  resp = {}
  for year in list(nilai['acad_year'].unique()):
    data = json.loads(nilai[nilai['acad_year'] == year].to_json(orient="records"))
    overall = nilai[nilai['acad_year'] == year].drop(['course_id', 'acad_year', 'acad_id'], axis=1).sum(axis=0)
    resp[year] = []
    resp[year].append(
      {
        "matkulid": "All",
        "A": overall['grade_A'],
        "AB": overall['grade_AB'],
        "B": overall['grade_B'],
        "BC": overall['grade_BC'],
        "C": overall['grade_C'],
        "D": overall['grade_D'],
        "E": overall['grade_E'],
      }
    )
    for score in data:
      resp[year].append({
        "matkulid": score['course_id'],
        "A": score['grade_A'],
        "AB": score['grade_AB'],
        "B": score['grade_B'],
        "BC": score['grade_BC'],
        "C": score['grade_C'],
        "D": score['grade_D'],
        "E": score['grade_E'],
      })
    
    
  

  return JsonResponse(resp, safe=False)

  