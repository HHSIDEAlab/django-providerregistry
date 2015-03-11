from django.contrib import admin
from models import NameAlias


class NameAliasAdmin(admin.ModelAdmin):
    search_fields = ("name", "alias")
    list_display = ("name", "alias")


admin.site.register(NameAlias, NameAliasAdmin)
