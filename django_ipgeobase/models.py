#encoding:utf8
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_ipgeobase.managers import IPGeoBaseManager


class IPGeoBase_Country(models.Model):
    code = models.CharField(_(u'код страны'), max_length=2, primary_key=True)
    name = models.CharField(_(u'название страны'), max_length=255, unique=True)

    def __unicode__(self):
        return u"[%s] %s" % (self.code, self.name)

    class Meta:
        verbose_name = _(u"страна")
        verbose_name_plural = _(u"страны")


class IPGeoBase_Region(models.Model):
    country = models.ForeignKey(IPGeoBase_Country, verbose_name=_(u'страна'), null=True)
    name = models.CharField(_(u"название региона"), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"регион")
        verbose_name_plural = _(u"регионы")
        unique_together = (('country', 'name'), )


class IPGeoBase_City(models.Model):
    country = models.ForeignKey(IPGeoBase_Country, verbose_name=_(u'страна'))
    region = models.ForeignKey(IPGeoBase_Region, verbose_name=_(u'регион'))
    name = models.CharField(_(u"название города"), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"город")
        verbose_name_plural = _(u"города")
        unique_together = (('country', 'region', 'name'), )


class IPGeoBase(models.Model):
    """Таблица перечень блоков ip-адресов с координатами"""
    start_ip = models.BigIntegerField(
        u'Начальный IP-адрес блока, преобразованный в число',
        help_text=u"""IP-адрес иммет вид a.b.c.d, где a-d числа в диапазоне 0-255. Преобразование в число происходит по формуле 256³*a+256²*b+256*c+d""",
        db_index=True)

    end_ip = models.BigIntegerField(
        u'Конечный IP-адрес блока, преобразованный в число',
        db_index=True)

    country = models.ForeignKey(IPGeoBase_Country)
    region = models.ForeignKey(IPGeoBase_Region)
    city = models.ForeignKey(IPGeoBase_City)

    ip_block = models.CharField(
        _(u'Блок IP-адресов'),
        help_text=_(u"""Данное поле состоит из начального и конечного адресов блока, отделенных друг от друга пробелом, тире и пробелом"""),
        max_length=64)

    def __unicode__(self):
        return "[%s] %s" % (self.country_id, self.ip_block)

    objects = IPGeoBaseManager()

    class Meta:
        verbose_name = _(u"Блок IP")
        verbose_name_plural = _(u"Блоки IP")