from django.db import models
from django.apps import apps


class Website(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Sitio Web'
        verbose_name_plural = 'Sitios Web'


class Property(models.Model):
    post = models.OneToOneField('progress.Posts', on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100, verbose_name='Nombre')
    property_price = models.CharField(max_length=100, verbose_name='Precio')
    property_address = models.CharField(max_length=200, verbose_name='Dirección')
    property_url = models.URLField(verbose_name='URL Detalle')

    def website_name(self):
        return self.post.website.site_name

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name = 'Espacio en Renta'
        verbose_name_plural = 'Espacios en Renta'
