from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer


"""
    Seleksi peminatan
"""

class SeleksiPeminatan:
    def __init__(self, username):
        try:
            self.student = Profile.objects.get(username=username)
        except:
            pass

    def register(self, batch, firstOption, secondOption):
        try:
            
            batch = Batch.objects.get(id=batch)
            firstOption = Peminatan.objects.get(peminatancode=firstOption)
            secondOption = Peminatan.objects.get(peminatancode=secondOption)

            seleksi = Seleksi(studentid=self.student, pilihan1=firstOption, pilihan2=secondOption, batch=batch)
            seleksi.save()

        except:
            pass