#encoding:utf8
from django.core.management.base import NoArgsCommand, CommandError
from django.db import connection, transaction
from django_ipgeobase import conf
from zipfile import ZipFile
from urllib import urlopen
from cStringIO import StringIO
from django.core.mail import mail_admins
from django_ipgeobase import models


DELETE_SQL = \
"""
DELETE FROM django_ipgeobase_ipgeobase
"""

INSERT_SQL = \
"""
INSERT INTO django_ipgeobase_ipgeobase
(ip_block, "start_ip", "end_ip", city, region, district, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

ERROR_SUBJECT = u"Error of command ipgeobase_update"
send_message = conf.IPGEOBASE_SEND_MESSAGE_FOR_ERRORS

def get_url(url):
    from hashlib import md5
    from os import path
    h = md5()
    h.update(url)
    fn = '/tmp/%s.txt' % h.hexdigest()
    if path.exists(fn):
        return open(fn, 'rb')
    else:
        content = urlopen(url).read()
        f = open(fn, 'wb')
        f.write(content)
        f.close()
        return StringIO(content)


class Command(NoArgsCommand):

    def get_row(self, row, query_info):
        record = {}
        record.update(query_info.get('defaults', {}))
        for i, field_name in enumerate(query_info['fields']):
            if field_name is not None:
                val = row[i].strip()
                if val:
                    record[field_name] = val
        record['country'] = record['country'].upper()
        return record

    def get_contents(self, query_info):
        buff = get_url(query_info['url'])
        if query_info['format'] == 'zip':
            zip_file = ZipFile(buff)
            try:
                content = zip_file.read(query_info['zip_filename'])
            except KeyError:
                raise CommandError("File %s in archive not found" % query_info['zip_filename'])
            zip_file.close()
        else:
            content = buff.read()
        buff.close()
        return content

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.countries = {}
        self.cities = {}
        self.regions = {}

        for c in models.IPGeoBase_Country.objects.all():
            self.countries[c.code.upper()] = c.code

        for c in models.IPGeoBase_Region.objects.all():
            self.regions[(c.country_id, c.name.lower())] = c.id

        for c in models.IPGeoBase_City.objects.all():
            self.cities[(c.country_id, c.region_id, c.name.lower())] = c.id

    def preprocess_row(self, row):
        row['country'] = row['country'].upper()
        if row['country'] not in self.countries:
            country = models.IPGeoBase_Country.objects.create(code=row['country'], name=row['country'])
            self.countries[country.code] = country.code
            print "created country", country.name
        row['country'] = self.countries[row['country']]

        region = row['region'].lower()
        region_key = (row['country'], region)
        if region_key not in self.regions:
            region = models.IPGeoBase_Region.objects.create(country_id=row['country'], name=row['region'])
            self.regions[region_key] = region.id
            print "created city", row['region']
        row['region'] = self.regions[region_key]

        city_key = (row['country'], row['region'], row['city'].lower())
        if city_key not in self.cities:
            city = models.IPGeoBase_City.objects.create(country_id=row['country'], region_id=row['region'], name=row['city'])
            self.cities[city_key] = city.id
            print "created city", row['city']
        row['city'] = self.cities[city_key]
        return row

    @transaction.commit_on_success
    def handle_noargs(self, *args, **options):
        database = []
        print "Init done"
        for query_info in conf.IPGEOBASE_COUNTRY_INFO:
            content = self.get_contents(query_info)
            for line in content.decode(query_info['coding']).split("\n"):
                line = line.strip()
                if not line:
                    continue

                row = self.get_row(line.split("\t"), query_info)
                row = self.preprocess_row(row)
                database.append(
                    (row['start_ip'], row['end_ip'], row['city'], row['region'], row['country'], row['ip_block']),
                )
        try:
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE django_ipgeobase_ipgeobase")
            print cursor.executemany("""
            INSERT INTO django_ipgeobase_ipgeobase
            (start_ip, end_ip, city_id, region_id, country_id, ip_block)
            VALUES (%s, %s, %s, %s, %s, %s )
            """, database)
            transaction.commit()
        except Exception, e:
            transaction.rollback()
            message = "The data not updated:", e
            if send_message:
                mail_admins(subject=ERROR_SUBJECT, message=message)
            raise CommandError(message)
