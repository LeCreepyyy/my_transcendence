from django.db import models

class p_img(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.desc