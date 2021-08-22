from django.db import models
from django.db.models.deletion import CASCADE
from decimal import Decimal



PEMINATAN_CHOICES = [
  ("EDE", "EDE"),
  ("EISD", "EISD"),
  ("ERP", "ERP"),
  ("SAG", "SAG"),
  ("EIM", "EIM"),
]

KELOMPOK_CHOICES = [
  ("CYBERNETICS", "CYBERNETICS"),
  ("EIS", "EIS"),
]

PENGAJUAN_CHOICES = [
  ("Pengajuan I", "Pengajuan I"),
  ("Pengajuan II", "Pengajuan II"),
  ("Disetujui", "Disetujui"),
  ("Ditolak I", "Ditolak I"),
  ("Ditolak II", "Ditolak II"),
]

ROLE_CHOICES = [
  ("MAHASISWA", "MAHASISWA"),
  ("DOSEN PEMBINA", "DOSEN PEMBINA"),
  ("ADMIN", "ADMIN"),
]

MATKUL_CHOICES = [
  ("RPB", "RPB"),
  ("PROBSTAT", "PROBSTAT"),
  ("BASDAT", "BASDAT"),
  ("DWBI", "DWBI"),
  ("OOP", "OOP"),
  ("APSI", "APSI"),
  ("ALPRO", "ALPRO"),
  ("WEB", "WEB"),
  ("EA", "EA"),
  ("MANLAY", "MANLAY"),
  ("SE", "SE"),
  ("SCM", "SCM"),
  ("AKUNTANSI", "AKUNTANSI"),
  ("MANPROSI", "MANPROSI"),
  ("DESJAR", "DESJAR"),
  ("MANJARKOM", "MANJARKOM"),
  ("SISOP", "SISOP"),
  ("KSI", "KSI"),
]

KEPROF_CHOICES = [
  ("DASPRO", "DASPRO"),
  ("SISJAR", "SISJAR"),
  ("SAG", "SAG"),
  ("ERP", "ERP"),
  ("EIM", "EIM"),
]

KEPROF_KATEGORI = [
  ("KORDAS", "KORDAS"),
  ("ASISTEN", "ASISTEN"),
  ("ANGGOTA", "ANGGOTA"),
]

# PIPE APP

class Peminatan(models.Model):
  peminatancode = models.CharField(max_length=255, choices=PEMINATAN_CHOICES, primary_key=True)
  peminatanname = models.CharField(max_length=255)
  kelompokkeahlian = models.CharField(max_length=255, choices=KELOMPOK_CHOICES, null=True, blank=True)
  prasyarat1 = models.CharField(max_length=255, choices=MATKUL_CHOICES, blank=True, null=True)
  prasyarat2 = models.CharField(max_length=255, choices=MATKUL_CHOICES, blank=True, null=True)
  prasyarat3 = models.CharField(max_length=255, choices=MATKUL_CHOICES, blank=True, null=True)
  prasyarat4 = models.CharField(max_length=255, choices=MATKUL_CHOICES, blank=True, null=True)
  kuota = models.IntegerField(blank=True, null=True, default=0)
  sisakuota = models.IntegerField(blank=True, null=True, default=0)

  def __str__(self):
   return f'{self.peminatancode} - {self.peminatanname}'

class Profile(models.Model):
  numberid = models.CharField(max_length=255, null=True)
  username = models.CharField(max_length=255)
  role = models.CharField(max_length=255, null=True, choices=ROLE_CHOICES)
  fullname = models.CharField(max_length=255, null=True)
  photo = models.CharField(max_length=255, null=True, blank=True)
  schoolyear = models.IntegerField(null=True, blank=True)
  studentclass = models.CharField(max_length=255, null=True, blank=True)
  lecturerguardian = models.CharField(max_length=255, null=True, blank=True)
  studyprogram = models.CharField(max_length=255, null=True, blank=True)
  faculty = models.CharField(max_length=255, null=True, blank=True)
  peminatan = models.ForeignKey('Peminatan', null=True, on_delete=models.SET_NULL, blank=True, related_name='user_peminatan')

  def __str__(self):
   return f'{self.numberid} - {self.fullname}'

class Dosen(models.Model):
  name = models.CharField(max_length=255, null=True)
  kelompok = models.CharField(max_length=255,choices=KELOMPOK_CHOICES ,null=True, blank=True)
  peminatan = models.CharField(max_length=255,choices=PEMINATAN_CHOICES ,null=True, blank=True)

  def __str__(self):
   return f'{self.name} - {self.peminatan}'

class Keprof(models.Model):
  nim = models.CharField(max_length=255, null=True)
  name = models.CharField(max_length=255, null=True)
  keprof = models.CharField(max_length=255, choices=KEPROF_CHOICES, blank=True)
  kategori = models.CharField(max_length=255, choices=KEPROF_KATEGORI, blank=True)

  def __str__(self):
   return f'{self.nim} - {self.name}'
  

class Nilai(models.Model):
  nim = models.CharField(max_length=255, blank=True, null=True)
  name = models.CharField(max_length=255, blank=True, null=True)
  rpb = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  probstat = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  basdat = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  dwbi = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  oop = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  apsi = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  alpro = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  web = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  ea = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  manlay = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  se = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  scm = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  akuntansi = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  manprosi = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  desjar = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  manjarkom = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  sisop = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)
  ksi = models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True, default=0)

  def __str__(self):
   return f'{self.nim} - {self.name}'

class Batch(models.Model):
  batchnum = models.CharField(max_length=255, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
   return f'Batch - {self.batchnum}'

class Seleksi(models.Model):
  studentid = models.ForeignKey('Profile', on_delete=CASCADE, related_name='seleksi_student')
  pilihan1 = models.ForeignKey('Peminatan', on_delete=models.SET_NULL, null=True, blank=True, related_name='pilihansatu')
  pilihan2 = models.ForeignKey('Peminatan', on_delete=models.SET_NULL, null=True, blank=True, related_name='pilihandua')
  score1 = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal(0.0), null=True)
  score2 = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal(0.0), null=True)
  batch = models.ForeignKey('Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='batchnumber')
  result = models.ForeignKey('Peminatan', on_delete=models.SET_NULL, null=True, blank=True, related_name='result_peminatan')

  def __str__(self):
   return f'{self.studentid.numberid} - {self.studentid.fullname}'

class StatusServer(models.Model):
  name = models.CharField(max_length=100)
  isAvailable = models.BooleanField(default=True)

  def __str__(self):
   return self.name

class TukarPeminatan(models.Model):
  mahasiswa1 = models.ForeignKey('Profile', on_delete=CASCADE, related_name='mahasiswasatu')
  mahasiswa2 = models.ForeignKey('Profile', on_delete=CASCADE, related_name='mahasiswadua')
  status = models.CharField(max_length=255, null=True, choices=PENGAJUAN_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
   return self.mahasiswa1.numberid

class Bobot(models.Model):
  kordas = models.IntegerField(blank=True, null=True, default=0)
  asisten = models.IntegerField(blank=True, null=True, default=0)
  anggota = models.IntegerField(blank=True, null=True, default=0)
  pilihan1 = models.IntegerField(blank=True, null=True, default=0)



  
  




