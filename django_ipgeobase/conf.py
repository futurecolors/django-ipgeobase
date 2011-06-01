#encoding: utf-8

IPGEOBASE_CITIES_INFO = {
        'url': 'http://ipgeobase.ru/files/db/Main/geo_files.zip',
        'filename': 'cities.txt',
        'encoding': 'windows-1251',
        'fields': ['city_id', 'city_name', 'region_name', 'district', 'lat', 'lng'],
    }

IPGEOBASE_CIDR_INFO = {
        'url': 'http://ipgeobase.ru/files/db/Main/geo_files.zip',
        'filename': 'cidr_optim.txt',
        'encoding': 'windows-1251',
        'fields': ['start_ip', 'end_ip', 'ip_block', 'country_id', 'city_id'],
    }
