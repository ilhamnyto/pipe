from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer


"""
Batch peminatan
"""

class BatchPeminatan:

    def __init__(self, batch):
        try:
            self.batch = Batch(batchnum=batch)
        except:
            pass

    def create(self):
        try:
            self.batch.save()
        except:
            pass

    def getLatestBatch(self):
        pass