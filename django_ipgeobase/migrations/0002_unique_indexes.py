# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'IPGeoBase_Region', fields ['country', 'name']
        db.create_unique('django_ipgeobase_ipgeobase_region', ['country_id', 'name'])

        # Adding unique constraint on 'IPGeoBase_Country', fields ['name']
        db.create_unique('django_ipgeobase_ipgeobase_country', ['name'])

        # Adding unique constraint on 'IPGeoBase_City', fields ['country', 'region', 'name']
        db.create_unique('django_ipgeobase_ipgeobase_city', ['country_id', 'region_id', 'name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'IPGeoBase_City', fields ['country', 'region', 'name']
        db.delete_unique('django_ipgeobase_ipgeobase_city', ['country_id', 'region_id', 'name'])

        # Removing unique constraint on 'IPGeoBase_Country', fields ['name']
        db.delete_unique('django_ipgeobase_ipgeobase_country', ['name'])

        # Removing unique constraint on 'IPGeoBase_Region', fields ['country', 'name']
        db.delete_unique('django_ipgeobase_ipgeobase_region', ['country_id', 'name'])


    models = {
        'django_ipgeobase.ipgeobase': {
            'Meta': {'object_name': 'IPGeoBase'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Country']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_block': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Region']"}),
            'start_ip': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        'django_ipgeobase.ipgeobase_city': {
            'Meta': {'unique_together': "(('country', 'region', 'name'),)", 'object_name': 'IPGeoBase_City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Region']"})
        },
        'django_ipgeobase.ipgeobase_country': {
            'Meta': {'object_name': 'IPGeoBase_Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'django_ipgeobase.ipgeobase_region': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'IPGeoBase_Region'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['django_ipgeobase']
