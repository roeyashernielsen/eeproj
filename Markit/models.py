from django.db import models


class System(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=False)

class Stock(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    symbol = models.CharField(max_length=256, null=False, blank=False)
    file = models.FileField(default="tmp",upload_to='files/%Y/%m/%d')
    print("t")