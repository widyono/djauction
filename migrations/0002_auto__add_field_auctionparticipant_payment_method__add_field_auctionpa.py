# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AuctionParticipant.payment_method'
        db.add_column(u'djauction_auctionparticipant', 'payment_method',
                      self.gf('django.db.models.fields.CharField')(default='none', max_length=10),
                      keep_default=False)

        # Adding field 'AuctionParticipant.payment_notes'
        db.add_column(u'djauction_auctionparticipant', 'payment_notes',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AuctionParticipant.payment_method'
        db.delete_column(u'djauction_auctionparticipant', 'payment_method')

        # Deleting field 'AuctionParticipant.payment_notes'
        db.delete_column(u'djauction_auctionparticipant', 'payment_notes')


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
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '10'}),
            'payment_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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