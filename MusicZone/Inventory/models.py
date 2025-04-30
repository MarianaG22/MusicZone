from django.db import models

# Create your models here.
class Type(models.Model):
    type = models.CharField(max_length=100, verbose_name="Tipo")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

class Mark(models.Model):
    mark = models.CharField(max_length=100, verbose_name="Marca")

    def __str__(self):
        return self.mark

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

class Instrument(models.Model):
    instrument = models.CharField(max_length=100, verbose_name="Instrumento")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Tipo")
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name="Marca")
    price = models.IntegerField(verbose_name="Precio")
    stock = models.IntegerField(verbose_name="Stock")

    def __str__(self):
        return self.instrument

    class Meta:
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"