from django.contrib import admin
from .models import CarMake, CarModel 


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1
# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
class CarMakAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakAdmin)
admin.site.register(CarModel)