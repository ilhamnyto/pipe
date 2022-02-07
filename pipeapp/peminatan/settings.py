from .models import Batch, Bobot, Dosen, Keprof, Nilai, Seleksi, Peminatan, Profile, TukarPeminatan, StatusServer

"""
Settings for peminatan.
"""

class Setting:

    def __init__(self):
        try:
            self.ede = Peminatan.objects.get(peminatancode='EDE')
            self.eisd = Peminatan.objects.get(peminatancode='EISD')
            self.sag = Peminatan.objects.get(peminatancode='SAG')
            self.eim = Peminatan.objects.get(peminatancode='EIM')
            self.erp = Peminatan.objects.get(peminatancode='ERP')
            self.bobot = Bobot.objects.get(id=1)
        except:
            pass

    def setEDEPrasyarat(self, first, second, third, fourth):
        try:
            self.ede.prasyarat1 = first
            self.ede.prasyarat2 = second
            self.ede.prasyarat3 = third
            self.ede.prasyarat4 = fourth
            self.ede.save()
        except:
            pass

    
    def setEISDPrasyarat(self, first, second, third, fourth):
        try:
            self.eisd.prasyarat1 = first
            self.eisd.prasyarat2 = second
            self.eisd.prasyarat3 = third
            self.eisd.prasyarat4 = fourth
            self.eisd.save()
        except:
            pass

    
    def setSAGPrasyarat(self, first, second, third, fourth):
        try:
            self.sag.prasyarat1 = first
            self.sag.prasyarat2 = second
            self.sag.prasyarat3 = third
            self.sag.prasyarat4 = fourth
            self.sag.save()
        except:
            pass

    
    def setEIMPrasyarat(self, first, second, third, fourth):
        try:
            self.eim.prasyarat1 = first
            self.eim.prasyarat2 = second
            self.eim.prasyarat3 = third
            self.eim.prasyarat4 = fourth
            self.eim.save()
        except:
            pass


    def setERPPrasyarat(self, first, second, third, fourth):
        try:
            self.erp.prasyarat1 = first
            self.erp.prasyarat2 = second
            self.erp.prasyarat3 = third
            self.erp.prasyarat4 = fourth
            self.erp.save()
        except:
            pass

    def setBobot(self, firstOption, kordas, assiten, anggota):
        try:
            self.bobot.pilihan1 = firstOption
            self.bobot.kordas = kordas
            self.bobot.asisten = assiten
            self.bobot.anggota = anggota
        except:
            pass

    def setKuota(self, bobot):
        try:
            self.bobot.kuotadosen = bobot
        except:
            pass

    

    