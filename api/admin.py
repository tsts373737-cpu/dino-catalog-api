from django.contrib import admin
from .models import Period, Diet, Dinosaur


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_mya', 'end_mya']
    search_fields = ['name']


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(Dinosaur)
class DinosaurAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'length_m', 'weight_t', 'period', 'diet']
    list_filter = ['period', 'diet']
    search_fields = ['name', 'description']