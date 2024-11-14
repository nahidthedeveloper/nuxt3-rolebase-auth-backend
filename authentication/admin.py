from django.contrib import admin
from authentication.models import Account
from django.contrib.auth.models import Permission

admin.site.register(Account)
admin.site.register(Permission)
