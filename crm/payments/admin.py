from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Payment)

admin.site.register(models.EMI)

admin.site.register(models.Transactions)
