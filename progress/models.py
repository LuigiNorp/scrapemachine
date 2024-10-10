from django.utils import timezone
from django.db import models
from django.apps import apps


class Posts(models.Model):
    website = models.ForeignKey('scraper.Website', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
