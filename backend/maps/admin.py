from django.contrib import admin
from .models import Building, Facility, Menu, Tag, Restaurant

admin.site.register(Building)
admin.site.register(Facility)
admin.site.register(Menu)
admin.site.register(Restaurant)

