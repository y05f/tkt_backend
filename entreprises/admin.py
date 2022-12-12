from django.contrib import admin
from .models import Entreprise, Result


class ResultInline(admin.TabularInline):
    model = Result


class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [
        ResultInline,
    ]
    list_display = (
        "name",
        "siren",
        "sector",
    )


class ResultAdmin(admin.ModelAdmin):

    list_display = ("entreprise", "year", "ca", "margin", "ebitda", "loss")


admin.site.register(Entreprise, EntrepriseAdmin)
admin.site.register(Result, ResultAdmin)
