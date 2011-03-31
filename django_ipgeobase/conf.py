#encoding: utf-8
from django.conf import settings

#Путь до файла block_coord.db
IPGEOBASE_SOURCE_URLS = getattr(settings, 'IPGEOBASE_SOURCE_URL', 'http://ipgeobase.ru/files/db/Map_db/block_coord.zip')
IPGEOBASE_FILENAME = getattr(settings, 'IPGEOBASE_FILENAME', "block_coord.db")
IPGEOBASE_CODING = getattr(settings, 'IPGEOBASE_CODING', 'windows-1251')
IPGEOBASE_SEND_MESSAGE_FOR_ERRORS = getattr(settings, 'IPGEOBASE_SEND_MESSAGE_FOR_ERRORS', True)

IPGEOBASE_USE_MULTICOUNTRY = True
IPGEOBASE_COUNTRY_INFO = [
    {
        'url': 'http://ipgeobase.ru/files/db/Main/db_files.zip',
        'format': 'zip',
        'zip_filename': 'cidr_ru_block.txt',
        'fields': ['start_ip', 'end_ip', 'ip_block', None, 'city', 'region', None, ],
        'coding': 'windows-1251',
        'defaults':{
            'country': 'ru',
            }
        },
    {
        'url': 'http://ipgeobase.ru/files/db/Main/ua_inetnums.txt',
        'format': 'text',
        'fields': ['ip_block', 'start_ip', 'end_ip', 'city', 'region'],
        'coding': 'windows-1251',
        'defaults': {
            'country':'ua',
            }
        }
    ]
