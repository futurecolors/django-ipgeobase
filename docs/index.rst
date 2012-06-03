django-ipgeobase
================

This app is no longer maintained, see https://github.com/futurecolors/django-geoip

django-ipgeobase - определение города, региона и страны по IP в Django

В качестве базы для геолокации используется ежедневно обновляемая http://ipgeobase.ru/
База содержит данные для России и Украины

Внимание: тестировалось только под Django 1.3

Установка
---------

Проделываем в командной строке ::

  $ git clone git://github.com/futurecolors/django-ipgeobase.git
  $ cd django-ipgeobase
  $ python setup.py install


Потом следует добавить 'django_ipgeobase' в INSTALLED_APPS и выполнить ::

  $ python manage.py syncdb


Либо, если вы используете south::

  $ python manage.py migrate django-ipgeobase


Использование
-------------

Для получения объекта ipgeobase (для определения региона) ::

  from django_ipgeobase.models import IPGeoBase

  ip = "212.49.98.48"

  ipgeobases = IPGeoBase.objects.by_ip(ip)
  if ipgeobases.exists():
      ipgeobase = ipgeobases[0]
      print ipgeobase.city # Населенный пункт (Екатеринбург)
      print ipgeobase.region # Регион (Свердловская область)
      print ipgeobase.country # Страна (Россия)


Обновления базы
~~~~~~~~~~~~~~~

Чтобы обновить базу ipgeobase:

  $ python manage.py ipgeobase_update
