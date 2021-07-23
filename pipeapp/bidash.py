
from django.shortcuts import redirect
import pandas as pd
import re
from django.http import JsonResponse
from .dburl import engine


def uploadfile(request):
  if request.method == "POST":
    try:
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

      jumlahdosen = dosen.groupby(['Peminatan']).size().reset_index(name='counts')
      jumlahdosen.columns = ['peminatan_name', 'jumlah_dosen']

      d_peminatan = pd.DataFrame({
          "peminatan_id": list(map(codeNaming, list(datamahasiswa['peminatan'].unique()))),
          "peminatan_name": list(datamahasiswa['peminatan'].unique())
      })

      d_peminatan = d_peminatan.merge(jumlahdosen, on='peminatan_name', how='left')

      d_peminatan['kuota'] = list(map(lambda x: x * 10, list(d_peminatan['jumlah_dosen'])))

      d_pilihan = pd.DataFrame({
          "pilihan_id": ['P1', 'P2'],
          "keterangan": ['Pilihan 1', 'Pilihan 2']
      })

      d_hasil = pd.DataFrame({
          "hasil_id": ['LP1', 'LP2', 'NB'],
          "keterangan": ['Lolos Pilihan Pertama', 'Lolos Pilihan Kedua', 'Tidak Lolos Keduanya']
      })

      def hasilNaming(pilihan1, pilihan2, hasil):
        if pilihan1 == hasil:
          return 'LP1'
        elif pilihan2 == hasil:
          return 'LP2'
        else:
          return 'NB'

      dd = datamahasiswa.filter(['nim', 'peminatan', 'peminatan_1', 'peminatan_2'])
      dd.columns = ['student_id', 'peminatan_id', 'peminatan_1', 'peminatan_2']

      dd['peminatan_id'] = list(map(codeNaming, list(dd['peminatan_id'])))
      dd['peminatan_1'] = list(map(codeNaming, list(dd['peminatan_1'])))
      dd['peminatan_2'] = list(map(codeNaming, list(dd['peminatan_2'])))

      dd['hasil_id'] = list(map(hasilNaming, list(dd['peminatan_1']), list(dd['peminatan_2']), list(dd['peminatan_id']) ))

      data1 = pd.DataFrame(columns=['student_id', 'acad_id', 'peminatan_id', 'pilihan_id', 'hasil_id', 'score'])
      data2 = pd.DataFrame(columns=['student_id', 'acad_id', 'peminatan_id', 'pilihan_id', 'hasil_id', 'score'])

      data1 = data1.append(dd)
      data2 = data2.append(dd)

      data1['acad_id'] = f'{acadid}{str(int(acadid)+1)}'
      data2['acad_id'] = f'{acadid}{str(int(acadid)+1)}'

      data1['pilihan_id'] = 'P1'
      data2['pilihan_id'] = 'P2'

      for ind in list(data1[data1['peminatan_1'] == 'EISD'].index):
        data1.loc[ind, 'score'] = datamahasiswa.iloc[ind]['oop'] + datamahasiswa.iloc[ind]['apsi'] + datamahasiswa.iloc[ind]['alpro'] + datamahasiswa.iloc[ind]['web']

      for ind in list(data1[data1['peminatan_1'] == 'EDE'].index):
        data1.loc[ind, 'score'] = datamahasiswa.iloc[ind]['rpb'] + datamahasiswa.iloc[ind]['basdat']

      for ind in list(data1[data1['peminatan_1'] == 'SAG'].index):
        data1.loc[ind, 'score'] = datamahasiswa.iloc[ind]['rpb'] + datamahasiswa.iloc[ind]['ea'] + datamahasiswa.iloc[ind]['apsi']

      for ind in list(data1[data1['peminatan_1'] == 'ERP'].index):
        data1.loc[ind, 'score'] = datamahasiswa.iloc[ind]['se'] + datamahasiswa.iloc[ind]['scm'] + datamahasiswa.iloc[ind]['manprosi']

      for ind in list(data1[data1['peminatan_1'] == 'EIM'].index):
        data1.loc[ind, 'score'] = datamahasiswa.iloc[ind]['desjar'] + datamahasiswa.iloc[ind]['manjarkom'] + datamahasiswa.iloc[ind]['sisop']

      for ind in list(data2[data2['peminatan_2'] == 'EISD'].index):
        data2.loc[ind, 'score'] = datamahasiswa.iloc[ind]['oop'] + datamahasiswa.iloc[ind]['apsi'] + datamahasiswa.iloc[ind]['alpro'] + datamahasiswa.iloc[ind]['web']

      for ind in list(data2[data2['peminatan_2'] == 'EDE'].index):
        data2.loc[ind, 'score'] = datamahasiswa.iloc[ind]['rpb'] + datamahasiswa.iloc[ind]['basdat']

      for ind in list(data2[data2['peminatan_2'] == 'SAG'].index):
        data2.loc[ind, 'score'] = datamahasiswa.iloc[ind]['rpb'] + datamahasiswa.iloc[ind]['ea'] + datamahasiswa.iloc[ind]['apsi']

      for ind in list(data2[data2['peminatan_2'] == 'ERP'].index):
        data2.loc[ind, 'score'] = datamahasiswa.iloc[ind]['se'] + datamahasiswa.iloc[ind]['scm'] + datamahasiswa.iloc[ind]['manprosi']

      for ind in list(data2[data2['peminatan_2'] == 'EIM'].index):
        data2.loc[ind, 'score'] = datamahasiswa.iloc[ind]['desjar'] + datamahasiswa.iloc[ind]['manjarkom'] + datamahasiswa.iloc[ind]['sisop']

      data1 = data1.drop(['peminatan_id', 'peminatan_2'], axis=1)
      data1.columns = ['student_id', 'acad_id', 'pilihan_id', 'hasil_id', 'score', 'peminatan_id']
      data2 = data2.drop(['peminatan_id', 'peminatan_1'], axis=1)
      data2.columns = ['student_id', 'acad_id', 'pilihan_id', 'hasil_id', 'score', 'peminatan_id']

      f_pendaftaran = data1.append(data2)

      check_pendaftaran = pd.read_sql('SELECT * FROM "F_Pendaftaran_Peminatan"', con=engine)
      check_mahasiswa = pd.read_sql('SELECT * FROM "D_Student"', con=engine)
      check_peminatan = pd.read_sql('SELECT * FROM "D_Peminatan"', con=engine)
      check_pilihan = pd.read_sql('SELECT * FROM "D_Pilihan"', con=engine)
      check_hasil = pd.read_sql('SELECT * FROM "D_Hasil"', con=engine)
      check_acad = pd.read_sql('SELECT * FROM "D_Acad_Year"', con=engine)

      in_pendaftaran = f_pendaftaran[(~f_pendaftaran.student_id.isin(check_pendaftaran.student_id)) & (~f_pendaftaran.pilihan_id.isin(check_pendaftaran.pilihan_id))]
      in_mahasiswa = d_mahasiswa[~d_mahasiswa.student_id.isin(check_mahasiswa.student_id)]
      in_peminatan = d_peminatan[~d_peminatan.peminatan_id.isin(check_peminatan.peminatan_id)]
      in_pilihan = d_pilihan[~d_pilihan.pilihan_id.isin(check_pilihan.pilihan_id)]
      in_hasil = d_hasil[~d_hasil.hasil_id.isin(check_hasil.hasil_id)]
      in_acad = d_tahunakademik[~d_tahunakademik.acad_id.isin(check_acad.acad_id)]

      in_mahasiswa.to_sql('D_Student', con=engine, index=False, if_exists="append", method='multi')
      in_peminatan.to_sql('D_Peminatan', con=engine, index=False, if_exists="append", method='multi')
      in_pilihan.to_sql('D_Pilihan', con=engine, index=False, if_exists="append", method='multi')
      in_hasil.to_sql('D_Hasil', con=engine, index=False, if_exists="append", method='multi')
      in_acad.to_sql('D_Acad_Year', con=engine, index=False, if_exists="append", method='multi')
      in_pendaftaran.to_sql('F_Pendaftaran_Peminatan', con=engine, index=False, if_exists="append", method='multi')


      return redirect('bidata')
    except Exception:
      return JsonResponse({"message": "File tidak sesuai dengan ketentuan."})


def getdatapeminatan(request):

  return JsonResponse({
    "eisd": {
      "mahasiswa": 123,
      "dosen": 12,
      "kuota": 120,
      "bimbingan": f'{123/12:.1f}'
    },
    "ede": {
      "mahasiswa": 67,
      "dosen": 9,
      "kuota": 90,
      "bimbingan": f'{67/9:.1f}'
    },
    "erp": {
      "mahasiswa": 39,
      "dosen": 5,
      "kuota": 50,
      "bimbingan": f'{39/5:.1f}'
    },
    "sag": {
      "mahasiswa": 95,
      "dosen": 15,
      "kuota": 150,
      "bimbingan": f'{95/15:.1f}'
    },
    "eim": {
      "mahasiswa": 43,
      "dosen": 6,
      "kuota": 60,
      "bimbingan": f'{43/6:.1f}'
    },
  })

def getdataoverall(request):

  return JsonResponse({
    "eisd": {
      "mahasiswa": 123,
      "dosen": 12,
      "kuota": 120,
      "bimbingan": f'{123/12:.1f}'
    },
    "ede": {
      "mahasiswa": 67,
      "dosen": 9,
      "kuota": 90,
      "bimbingan": f'{67/9:.1f}'
    },
    "erp": {
      "mahasiswa": 39,
      "dosen": 5,
      "kuota": 50,
      "bimbingan": f'{39/5:.1f}'
    },
    "sag": {
      "mahasiswa": 95,
      "dosen": 15,
      "kuota": 150,
      "bimbingan": f'{95/15:.1f}'
    },
    "eim": {
      "mahasiswa": 43,
      "dosen": 6,
      "kuota": 60,
      "bimbingan": f'{43/6:.1f}'
    },
  })

def getdatanilai(request):

  return JsonResponse({
    "all": {
      "A": 300,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 4,
      "E": 20
    },
    "oop": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 42,
      "E": 5
    },
    "rpb": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 41,
      "E": 5
    },
    "pi": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 120,
      "D": 4,
      "E": 5
    },
    "apsi": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 120,
      "D": 4,
      "E": 5
    },
    "web": {
      "A": 10,
      "AB": 42,
      "B": 410,
      "BC": 10,
      "C": 10,
      "D": 4,
      "E": 5
    },
    "statistik": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 42,
      "E": 5
    },
    "matdis": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 110,
      "D": 4,
      "E": 5
    },
    "alpro": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 42,
      "E": 5
    },
    "strukdat": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 110,
      "D": 4,
      "E": 5
    },
    "se": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 110,
      "D": 4,
      "E": 5
    },
    "po": {
      "A": 10,
      "AB": 42,
      "B": 420,
      "BC": 10,
      "C": 10,
      "D": 4,
      "E": 5
    },
    "scm": {
      "A": 10,
      "AB": 42,
      "B": 401,
      "BC": 10,
      "C": 10,
      "D": 4,
      "E": 5
    },
    "ea": {
      "A": 10,
      "AB": 422,
      "B": 40,
      "BC": 10,
      "C": 10,
      "D": 4,
      "E": 5
    },
    "basdat": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 110,
      "D": 4,
      "E": 5
    },
    "manjarkom": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 120,
      "D": 4,
      "E": 5
    },
    "sisop": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 110,
      "D": 4,
      "E": 5
    },
    "msdm": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 10,
      "C": 103,
      "D": 4,
      "E": 5
    },
    "desjar": {
      "A": 10,
      "AB": 42,
      "B": 410,
      "BC": 10,
      "C": 10,
      "D": 42,
      "E": 5
    },
    "manprosi": {
      "A": 10,
      "AB": 42,
      "B": 40,
      "BC": 101,
      "C": 102,
      "D": 42,
      "E": 55
    },
  })

  