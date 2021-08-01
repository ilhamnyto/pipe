from django.urls import path
from . import views
from . import api
from . import auth
from . import seleksi
from . import bidash
from . import masterdata
from . import prediksi

urlpatterns = [
  # Views
  path('login', views.index, name="index"),
  path('', views.home, name="home"),
      # mahasiswa
  path('daftar-peminatan', views.daftar, name="daftar"),
      # mahasiswa dan dosen
  path('pindah-peminatan', views.pindah, name="pindah"),
      # admin
  path('data-mahasiswa', views.datamahasiswa, name='datamahasiswa'),
  path('data-dosen', views.datadosen, name='datadosen'),
  path('data-keprof', views.datakeprof, name='datakeprof'),
  path('data-peminatan', views.datapeminatan, name='datapeminatan'),
  path('data-peminatan/add', views.tambahpeminatan, name='tambahpeminatan'),
  path('data-keprof/add', views.tambahkeprof, name='tambahkeprof'),
  path('data-mahasiswa/add', views.tambahmahasiswa, name='tambahmahasiswa'),
  path('data-dosen/add', views.tambahdosen, name='tambahdosen'),
  path('data-peminatan/edit/<str:peminatancode>', views.editpeminatan, name='editpeminatan'),
  path('data-keprof/edit/<int:id>', views.editkeprof, name='editkeprof'),
  path('data-mahasiswa/edit/<int:id>', views.editmahasiswa, name='editmahasiswa'),
  path('data-dosen/edit/<int:id>', views.editdosen, name='editdosen'),
  path('seleksi-peminatan', views.seleksipeminatan, name='seleksipeminatan'),
  path('hasil-seleksi', views.hasilseleksi, name='hasilseleksi'),
  path('hasil-seleksi/<int:id>', views.seleksiresult, name='seleksiresult'),
  path('penghitungan-nilai', views.penghitungannilai, name='penghitungannilai'),
  path('penghitungan-nilai/<int:id>', views.hitungnilai, name='hitungnilai'),
      # admin dan dosen
  path('bi-dashboard', views.bidashboard, name='bidashboard'),
  path('bi-dashboard/data', views.bidata, name='bidata'),
  path('bi-dashboard/nilai', views.binilai, name='binilai'),

  # API
  path('api/auth/login', auth.login, name='login'),
  path('api/auth/logout', auth.logout, name='logout'),
  path('api/daftar-peminatan', seleksi.daftarpeminatan, name='api-daftar-peminatan'),
  path('api/pindah-peminatan', seleksi.pengajuanpindah, name='api-pengajuan-pindah'),
  path('api/pengajuan-pindah', seleksi.pengajuankedosen, name='api-pengajuan-pindah-dosen'),
  path('api/login-status', api.loginstatus, name='api-login-status'),
  path('api/batch-status', seleksi.statusbatch, name='api-batch-status'),
  path('api/batch-create', seleksi.createbatch, name='api-create-batch'),
  path('api/plotting', seleksi.plotting, name='api-plotting'),
  path('api/upload-data', bidash.uploadfile, name='api-uploadfile'),
  path('api/delete-data', masterdata.deleteData, name='api-deletedata'),
  path('api/insert-data', masterdata.insertData, name='api-insertdata'),
  path('api/truncate-data', masterdata.truncateData, name='api-truncatedata'),
  path('api/update-data', masterdata.updateData, name='api-updatedata'),
  path('api/import-data', masterdata.importData, name='api-importdata'),
  path('api/bi/overall', bidash.getdataoverall, name='api-bi-overall'),
  path('api/bi/datanilai', bidash.getdatanilai, name='api-bi-nilai'),

    #   TA
    path('prediksi/kelulusan', prediksi.prediksikelulusan, name="prediksikelulusan"),
    path('prediksi/peminatan', prediksi.prediksipeminatan, name="prediksipeminatan"),
]