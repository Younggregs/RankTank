from django.contrib import admin

# Register your models here.
from .models import Account, Contest


admin.site.register(Account)
admin.site.register(Contest)
