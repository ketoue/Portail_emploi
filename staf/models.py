from django.db import models
from users.models import User

#model to the company
class Staf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    est_date = models.PositiveBigIntegerField(null=True, blank=True)
    ville = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=150, null=True, blank=True)


    def __str__(self):
        return self.name
