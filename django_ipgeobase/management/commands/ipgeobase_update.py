#encoding:utf8
from django.core.management.base import NoArgsCommand, CommandError
from django.db import connection, transaction
from django_ipgeobase import conf
from zipfile import ZipFile
import urllib2
from django_ipgeobase import models
from hashlib import md5
from os import path
import datetime

DELETE_SQL = \
"""
DELETE FROM django_ipgeobase_ipgeobase
"""

INSERT_SQL = \
"""
INSERT INTO django_ipgeobase_ipgeobase
(start_ip, end_ip, ip_block, country_id, city_id, region_id)
VALUES (%s, %s, %s, %s, %s, %s)
"""

COUNTRIES = {'RU': u'Россия',
             'UA': u'Украина'}

class Command(NoArgsCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._cache_existing_geo_objects()

    def handle_noargs(self, *args, **options):
        print 'Starting IP Geobase update...'
        ip_blocks, self.city_mapping = self._process_cidr()
        self._process_city_data()
        self._renew_ipblocks(ip_blocks)

    def _cache_existing_geo_objects(self):
        self.countries = {}
        self.cities = {}
        self.regions = {}

        for country in models.IPGeoBase_Country.objects.all():
            self.countries[country.code] = country.code
        for region in models.IPGeoBase_Region.objects.all():
            self.regions[(region.country_id, region.name.lower())] = region.id
        for city in models.IPGeoBase_City.objects.all():
            self.cities[int(city.id)] = int(city.id)

    def _process_cidr(self):
        ''' Обработка данных по блокам ip-адресов (файл cidr_optim.txt) '''
        cidr_data = self._get_entries_from_zipfile(conf.IPGEOBASE_CIDR_INFO)
        ip_blocks = []
        city_mapping = {'country':{}, 'region':{}}
        for line in cidr_data:
            row = dict(zip(conf.IPGEOBASE_CIDR_INFO['fields'], line.split("\t")))
            if row['city_id'].isdigit():
                self._add_country_if_not_exists(row['country_id'])
                city_mapping['country'][row['city_id']] = row['country_id']
                ip_blocks.append(line.split("\t"))
        return ip_blocks, city_mapping

    def _process_city_data(self):
        ''' Обработка данных по географии (файл cities.txt) '''
        city_data = self._get_entries_from_zipfile(conf.IPGEOBASE_CITIES_INFO)
        for line in city_data:
            row = dict(zip(conf.IPGEOBASE_CITIES_INFO['fields'], line.split("\t")))
            if row['city_id'] in self.city_mapping['country']:
                country_id = self.city_mapping['country'][row['city_id']]
            else:
                continue
            self._add_region_if_not_exists(country_id = country_id,
                                           region_name = row['region_name'])
            region_id = self._get_region_id(country_id, row['region_name'])
            self.city_mapping['region'][row['city_id']] = region_id
            self._add_city_if_not_exists(city_id = row['city_id'],
                                         city_name = row['city_name'],
                                         region_id = region_id,
                                         country_id = country_id)

    def _get_region_id(self, country_id, region_name):
        key = (country_id, region_name.lower())
        return self.regions[key]

    def _get_entries_from_zipfile(self, config):
        """ Получаем содержимое конкретного файла из архива в виде списка строк """
        zip_file = self._get_remote_file_contents(config['url'])
        content = self._get_unzipped_content(zip_file, config['filename'])
        return [line.strip() for line in content.decode(config['encoding']).split("\n")
                 if line.strip()]

    def _add_country_if_not_exists(self, country_id):
        if country_id not in self.countries:
            country = models.IPGeoBase_Country.objects.create(code=country_id,
                                                              name=COUNTRIES.get(country_id, country_id))
            self.countries[country.code] = country.code
            return country

    def _add_region_if_not_exists(self, country_id, region_name):
        region_key = (country_id, region_name.lower())
        if region_key not in self.regions:
            region = models.IPGeoBase_Region.objects.create(country_id=country_id, name=region_name)
            self.regions[region_key] = region.id
            return region

    def _add_city_if_not_exists(self, city_id, city_name, region_id, country_id):
        if int(city_id) not in self.cities:
            city = models.IPGeoBase_City.objects.create(id=city_id, name=city_name,
                                                        region_id=region_id,
                                                        country_id=country_id)
            self.cities[city_id] = city.id
            return city_id

    @transaction.commit_manually
    def _renew_ipblocks(self, ipblocks):
        """ Заменяем данные по блокам адресов в БД на новые """
        print 'Updating CIDR...'
        try:
            cursor = connection.cursor()
            cursor.execute(DELETE_SQL)
            for row in ipblocks:
                row.append(self.city_mapping['region'][row[4]])
            cursor.executemany(INSERT_SQL, ipblocks)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            print e
            print 'Geo data not updated'

    def _get_remote_file_contents(self, url):

        def get_local_name(url):
            now = datetime.datetime.now()
            md5_url_hash = md5(url+now.strftime('%Y-%m-%d')).hexdigest()
            return u'/tmp/{0}.zip'.format(md5_url_hash)

        def download_file(url, local_name):
            print 'Downloading {0}'.format(url)
            remote_file = urllib2.urlopen(url)
            output = open(local_name, 'wb')
            output.write(remote_file.read())
            output.close()

        local_name = get_local_name(url)
        if not path.exists(local_name):
            download_file(url, local_name)
        return open(local_name, 'rb')


    def _get_unzipped_content(self, zip_file, extract_file):
        """ Получаем содержимое конкретного файла из архива в виде строки """
        zip = ZipFile(zip_file)
        try:
            content = zip.read(extract_file)
        except KeyError:
            raise CommandError("File %s not found in archive".format(extract_file))
        zip.close()
        print 'Unzipped {0} successfully!'.format(zip_file.name)
        return content