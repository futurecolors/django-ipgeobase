# -*- coding: utf-8 -*-
from django.contrib import admin
from django_ipgeobase import models


class IPGeoBase_CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    readonly_fields = ('code', )

admin.site.register(models.IPGeoBase_Country, IPGeoBase_CountryAdmin)


class IPGeoBase_RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'name')
    list_filter = ('country',)
    ordering = ('name', )

admin.site.register(models.IPGeoBase_Region, IPGeoBase_RegionAdmin)


class IPGeoBase_CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'region', 'name')
    list_filter = ('country', 'region')
    pass

admin.site.register(models.IPGeoBase_City, IPGeoBase_CityAdmin)


class IPGeoBaseAdmin(admin.ModelAdmin):
    list_display = ('ip_block',)
    list_select_related = False

    # def queryset(self,request):
    #     a = self.model.objects.all().select_related('country', 'region')
    #     return a
admin.site.register(models.IPGeoBase, IPGeoBaseAdmin)
