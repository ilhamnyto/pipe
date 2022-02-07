from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer


"""
Server
"""

class Server:

    def __init__(self, name):
        try:
            self.status = StatusServer.objects.get(name=name)
        except:
            pass

    def enable(self):
        try:
            self.status.isAvailable = True
            self.status.save()
        except:
            pass

    def disable(self):
        try:
            self.status.isAvailable = False
            self.status.save()
        except:
            pass