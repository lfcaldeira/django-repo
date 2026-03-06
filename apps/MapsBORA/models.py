from django.db import models

class Submissao(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Submissões"
        ordering = ['creation_date']

