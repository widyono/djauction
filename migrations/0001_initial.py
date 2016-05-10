# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Auction'
        db.create_table(u'djauction_auction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'djauction', ['Auction'])

        # Adding model 'AuctionUser'
        db.create_table(u'djauction_auctionuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'djauction', ['AuctionUser'])

        # Adding model 'AuctionParticipant'
        db.create_table(u'djauction_auctionparticipant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.Auction'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.AuctionUser'])),
            ('paddle', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'djauction', ['AuctionParticipant'])

        # Adding model 'AuctionEvent'
        db.create_table(u'djauction_auctionevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.Auction'])),
        ))
        db.send_create_signal(u'djauction', ['AuctionEvent'])

        # Adding model 'AuctionItem'
        db.create_table(u'djauction_auctionitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('item_number', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('valid_winners', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.Auction'])),
            ('auction_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.AuctionEvent'])),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.AuctionUser'])),
            ('starting_bid', self.gf('django.db.models.fields.FloatField')()),
            ('conditions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('time_and_location', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'djauction', ['AuctionItem'])

        # Adding model 'AuctionBid'
        db.create_table(u'djauction_auctionbid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.Auction'])),
            ('bidder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.AuctionParticipant'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djauction.AuctionItem'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'djauction', ['AuctionBid'])


    def backwards(self, orm):
        # Deleting model 'Auction'
        db.delete_table(u'djauction_auction')

        # Deleting model 'AuctionUser'
        db.delete_table(u'djauction_auctionuser')

        # Deleting model 'AuctionParticipant'
        db.delete_table(u'djauction_auctionparticipant')

        # Deleting model 'AuctionEvent'
        db.delete_table(u'djauction_auctionevent')

        # Deleting model 'AuctionItem'
        db.delete_table(u'djauction_auctionitem')

        # Deleting model 'AuctionBid'
        db.delete_table(u'djauction_auctionbid')


    models = {
        u'djauction.auction': {
            'Meta': {'object_name': 'Auction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djauction.auctionbid': {
            'Meta': {'object_name': 'AuctionBid'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.Auction']"}),
            'bidder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.AuctionParticipant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.AuctionItem']"})
        },
        u'djauction.auctionevent': {
            'Meta': {'object_name': 'AuctionEvent'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.Auction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'djauction.auctionitem': {
            'Meta': {'object_name': 'AuctionItem'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.Auction']"}),
            'auction_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.AuctionEvent']"}),
            'conditions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.AuctionUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'item_number': ('django.db.models.fields.IntegerField', [], {}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'starting_bid': ('django.db.models.fields.FloatField', [], {}),
            'time_and_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'valid_winners': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'djauction.auctionparticipant': {
            'Meta': {'object_name': 'AuctionParticipant'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.Auction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paddle': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djauction.AuctionUser']"})
        },
        u'djauction.auctionuser': {
            'Meta': {'object_name': 'AuctionUser'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['djauction']