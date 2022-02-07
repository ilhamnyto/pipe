from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer


"""
Pindah peminatan
"""

class PindahPeminatan:

    def __init__(self, lecturer, student):
        try:
            self.lecturer = Profile.objects.get(username=lecturer)
            self.student = Profile.objects.get(username=student)
        except:
            pass

    def shift(self):
        try:
            
            self.student.peminatan = self.lecturer.peminatan
            self.student.save()

        except:
            pass