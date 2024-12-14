from django.db import models


#model for my cover letter
class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')

