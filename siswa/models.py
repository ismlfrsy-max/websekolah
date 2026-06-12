from django.db import models

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    umur = models.IntegerField(null=True, blank=True)
    tgl_lahir = models.DateField(null=True, blank=True)
    status_hadir = models.BooleanField(default=False)
    nilai_akhir = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nama