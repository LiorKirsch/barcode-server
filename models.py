from django.db import models
from datetime import datetime    
from django.contrib.auth.models import User
from django.conf import settings

class Product(models.Model):
    description = models.CharField(max_length=1000, blank=True)
    barcode     = models.IntegerField()
    barcodeType = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '%d:%s' % (self.barcode ,self.description)
    
    def natural_key(self):
        return { 'description':self.description,  'barcode':self.barcode,  'barcode_type':self.barcodeType}
    
   

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image       = models.ImageField(upload_to = settings.IMAGES_FOLDER)

    def __unicode__(self):
        return '%s - %s' % (self.product ,self.image )

class ScannedProducts(models.Model):
    addingDate = models.DateTimeField(default=datetime.now, blank=True)
    product = models.ForeignKey(Product)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return '%s - %s (%s)' % (self.product ,self.owner.username , self.addingDate)
    
    def natural_key(self):
        return { 'addingDate':self.addingDate, 'product':self.product.natural_key() }
    

class Scanner(models.Model):
    owner = models.ForeignKey(User)
    uniqueId = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.uniqueId ,self.owner.username)
