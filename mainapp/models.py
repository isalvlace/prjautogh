from django.db import models

class XYZKCLIENT(models.Model):
    XYZKCODCLI = models.AutoField(primary_key=True)
    XYZKCLIENTE = models.CharField(max_length=255)
    XYZKTELCOB = models.CharField(max_length=20, blank=True, null=True)
    XYZKTELENT = models.CharField(max_length=20, blank=True, null=True)
    XYZKEMAIL = models.EmailField(max_length=255, blank=True, null=True)
    XYZKCODBARRA = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'XYZKCLIENT'

    def __str__(self):
        return f"Cliente {self.XYZKCODCLI} - {self.XYZKCLIENTE}"

class XYZKNFSAID(models.Model):
    XYZKNUMTRANSVENDA = models.AutoField(primary_key=True)
    XYZKCODCLI = models.ForeignKey(XYZKCLIENT, on_delete=models.DO_NOTHING, db_column='XYZKCODCLI')
    XYZKDTFECHA = models.DateField(blank=True, null=True)
    XYZKESPECIE = models.CharField(max_length=50, blank=True, null=True)
    XYZKNUMNOTA = models.CharField(max_length=50, blank=True, null=True)
    XYZKVLTOTAL = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    XYZKDTENTREGA = models.DateField(blank=True, null=True)
    XYZKNUMPED = models.IntegerField(blank=True, null=True)
    XYZKCLIENTE = models.CharField(max_length=255, blank=True, null=True)
    XYZKDTFAT = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'XYZKNFSAID'

    def __str__(self):
        return f"Venda {self.XYZKNUMTRANSVENDA} - {self.XYZKESPECIE}"

class XYZKPREST(models.Model):
    XYZKNUMTRANSVENDA = models.AutoField(primary_key=True)
    XYZKCODCLI = models.ForeignKey(XYZKCLIENT, on_delete=models.DO_NOTHING, db_column='XYZKCODCLI')
    XYZKDUPLIC = models.IntegerField(blank=True, null=True)
    XYZKVALOR = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    XYZKDTVENC = models.DateField(blank=True, null=True)
    XYZKDTPAG = models.DateField(blank=True, null=True)
    XYZKDTFECHA = models.DateField(blank=True, null=True)
    XYZKCODBARRA = models.CharField(max_length=255, blank=True, null=True)
    XYZKNUMPED = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'XYZKPREST'

    def __str__(self):
        return f"Transação {self.XYZKNUMTRANSVENDA} - Valor: {self.XYZKVALOR}"
