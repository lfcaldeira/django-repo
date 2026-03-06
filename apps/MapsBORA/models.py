from django.db import models

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
    description = models.CharField(max_length=400)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"{self.mapper_name} - {map_name}"

    class Meta:
        verbose_name_plural = "submissions"
        verbose_name = "submission"
        ordering = ['submitted_date']
    

