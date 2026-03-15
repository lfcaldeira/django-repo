from django.db import models
import random, string

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('completed', 'Completed')
    ]
    mapper_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    map_name = models.CharField(max_length=300)
    map_url = models.URLField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=400)
    request_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')
    token = models.CharField(max_length=10,null=True, blank=True)
    gpx_file = models.FileField(upload_to='gpx_files/', null=True, blank=True, help_text='Optional: Send the course\'s .gpx')

    def __str__(self):
        return f"{self.mapper_name} - {self.map_name}"

    @property
    def is_repeated(self):
        return Submission.objects.filter(map_url=self.map_url, status='completed').exclude(id=self.id).exists()
    
    class Meta:
        verbose_name_plural = "submissions"
        verbose_name = "submission"
        ordering = ['request_date']