from django.contrib import admin

from app.models import Profile,Balance,Entry

admin.site.register(Profile)

admin.site.register(Balance)
admin.site.register(Entry)