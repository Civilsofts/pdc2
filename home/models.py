from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email ünvanı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Abunə tarixi")
    
    class Meta:
        verbose_name = "Abunəçi"
        verbose_name_plural = "Abunəçilər"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
