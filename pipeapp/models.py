from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField


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
  ("DOSEN", "DOSEN"),
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
  peminatan = models.ForeignKey('Peminatan', null=True, on_delete=CASCADE, blank=True, related_name='user_peminatan')

class Dosen(models.Model):
  name = models.CharField(max_length=255, null=True)
  kelompok = models.CharField(max_length=255,choices=KELOMPOK_CHOICES ,null=True, blank=True)
  peminatan = models.CharField(max_length=255,choices=PEMINATAN_CHOICES ,null=True, blank=True)

class Keprof(models.Model):
  nim = models.CharField(max_length=255, null=True)
  name = models.CharField(max_length=255, null=True)
  keprof = models.CharField(max_length=255, choices=KEPROF_CHOICES, blank=True)

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

class Batch(models.Model):
  batchnum = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

class Seleksi(models.Model):
  studentid = models.ForeignKey('Profile', on_delete=CASCADE, related_name='seleksi_student')
  pilihan1 = models.ForeignKey('Peminatan', on_delete=CASCADE, related_name='pilihansatu')
  pilihan2 = models.ForeignKey('Peminatan', on_delete=CASCADE, related_name='pilihandua')
  score1 = models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)
  score2 = models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)
  batch = models.ForeignKey('Batch', on_delete=CASCADE, null=True, related_name='batchnumber')
  result = models.ForeignKey('Peminatan', on_delete=CASCADE, null=True, blank=True)

class StatusServer(models.Model):
  name = models.CharField(max_length=100)
  isAvailable = models.BooleanField(default=True)

class TukarPeminatan(models.Model):
  mahasiswa1 = models.ForeignKey('Profile', on_delete=CASCADE, related_name='mahasiswasatu')
  mahasiswa2 = models.ForeignKey('Profile', on_delete=CASCADE, related_name='mahasiswadua')
  status = models.CharField(max_length=255, null=True, choices=PENGAJUAN_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)


  
  




