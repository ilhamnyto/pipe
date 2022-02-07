from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer


"""
Tukar peminatan
"""

class TukarPeminatan:

    def __init__(self, firstStudent, secondStudent):
        try:
            self.firstStudent = Profile.objects.get(username=firstStudent)
            self.secondStudent = Profile.objects.get(username=secondStudent)
        except:
            pass

    def switch(self, status):
        try:
            
            switched = TukarPeminatan(
                mahasiswa1 = self.firstStudent,
                mahasiswa2 = self.secondStudent,
                status = status
            )

            switched.save()
        except:
            pass