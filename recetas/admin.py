from django.contrib import admin
from .models import Receta, RecetaOjo


class RecetaOjoInline(admin.TabularInline):
    model = RecetaOjo
    extra = 2


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    inlines = [RecetaOjoInline]