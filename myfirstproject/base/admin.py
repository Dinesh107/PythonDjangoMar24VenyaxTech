from django.contrib import admin

# Register your models here.

from .models import Space, Heading, Communicate

admin.site.register(Space)
admin.site.register(Heading)
admin.site.register(Communicate)
