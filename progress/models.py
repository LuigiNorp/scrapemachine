from django.db import models
from django.apps import apps


class Posts(models.Model):
    website = models.ForeignKey('scraper.Website', on_delete=models.CASCADE)
    website_page = models.IntegerField(verbose_name='Página')
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
