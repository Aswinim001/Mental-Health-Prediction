from django.contrib import admin

from mentalhealthapp.models import Bookings, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Bookings)