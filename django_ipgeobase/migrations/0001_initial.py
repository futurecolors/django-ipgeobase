# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IPGeoBase_Country'
        db.create_table('django_ipgeobase_ipgeobase_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_ipgeobase', ['IPGeoBase_Country'])

        # Adding model 'IPGeoBase_Region'
        db.create_table('django_ipgeobase_ipgeobase_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_ipgeobase', ['IPGeoBase_Region'])

        # Adding model 'IPGeoBase_City'
        db.create_table('django_ipgeobase_ipgeobase_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_Country'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_Region'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_ipgeobase', ['IPGeoBase_City'])

        # Adding model 'IPGeoBase'
        db.create_table('django_ipgeobase_ipgeobase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_ip', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_City'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_Region'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_ipgeobase.IPGeoBase_Country'])),
            ('ip_block', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('django_ipgeobase', ['IPGeoBase'])


    def backwards(self, orm):
        
        # Deleting model 'IPGeoBase_Country'
        db.delete_table('django_ipgeobase_ipgeobase_country')

        # Deleting model 'IPGeoBase_Region'
        db.delete_table('django_ipgeobase_ipgeobase_region')

        # Deleting model 'IPGeoBase_City'
        db.delete_table('django_ipgeobase_ipgeobase_city')

        # Deleting model 'IPGeoBase'
        db.delete_table('django_ipgeobase_ipgeobase')


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
            'Meta': {'object_name': 'IPGeoBase_City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Region']"})
        },
        'django_ipgeobase.ipgeobase_country': {
            'Meta': {'object_name': 'IPGeoBase_Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'django_ipgeobase.ipgeobase_region': {
            'Meta': {'object_name': 'IPGeoBase_Region'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_ipgeobase.IPGeoBase_Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['django_ipgeobase']
