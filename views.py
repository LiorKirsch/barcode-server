from django.http import HttpResponse
from django.shortcuts import render
from forms import PhotoForm, BarcodeForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import Product, ProductImage, Scanner, ScannedProducts
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers

import os
import tempfile
import urllib2
from subprocess import Popen, PIPE, STDOUT
import string, random

def addToPerson(request, personID):
    person = User.objects.get(username=personID)
    machineID = request.GET['machineID']
    try:
        scanner = Scanner.objects.get(uniqueId=machineID)
        scanner.owner = person
        scanner.save()
    except Scanner.DoesNotExist:
        scanner = Scanner(owner=person, uniqueId=machineID )
        scanner.save()

    response_data = {'status': 'success','response': 'added %s to user %s' % (machineID, personID) }
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt    
def uploadImage(request):
        
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            machineID = urllib2.unquote( request.POST['machineID'] )
            scanner = Scanner.objects.get(uniqueId=machineID)
            person =  scanner.owner
            
            imageFile = request.FILES['image']
            code      =  getBarCodeFromImage(imageFile)
            
            if code == '':
                response = 'barcode not found'
                status = 'error'
            else:
                imageFile.name = getTmpFileName()
                response = updateRecords(code, person, imageFile)
                status = 'success'
        else:
            response = 'form is not valid'
            status = 'error'
    
    response_data = {'status': status,'response': response}
    
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    

@csrf_exempt    
def uploadBarcode(request):
        
    if request.method == 'POST':
        form = BarcodeForm(request.POST, request.FILES)
        
        if form.is_valid():
            machineID = urllib2.unquote( request.POST['machineID'] )
            barcode = urllib2.unquote( request.POST['barcode'] )
            scanner = Scanner.objects.get(uniqueId=machineID)
            person =  scanner.owner
                
            response = updateRecords(barcode, person)
            status = 'success'
        else:
            response = 'form is not valid'
            status = 'error'
    
    response_data = {'status': status,'response': response}
    
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
def getTmpFileName():
    N = 8
    tmpImageFile = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
    return '%s.jpeg' % tmpImageFile

def getBarCodeFromImage(f):



    p = Popen(['/usr/bin/zbarimg', 'JPEG:-'], stdout=PIPE, stdin= PIPE)
    code = p.communicate( f.read() )[0]
    code = code.rstrip()

#    tmpImageFile = tempfile.NamedTemporaryFile(suffix='.jpeg', dir='/tmp')
#    tmpImageFileName = os.path.basename(tmpImageFile.name)
#    f.name = tmpImageFileName    
#    with open(tmpImageFile.name ,'w') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)
#    zbarimgCommand = '/usr/bin/zbarimg %s' % tmpImageFile.name
#    p = os.popen(zbarimgCommand, 'r')
#    code = p.readline()
    
    return code 

def updateRecords(code, person, imageFile = None):    
    if code == '':
        response = 'no bar code detected'
    else:
        barcodeType = code.split(':')[0]
        barcode = code.split(':')[1].rstrip()
        barcode = int(barcode)
        productObj, created = Product.objects.get_or_create(barcode = barcode, barcodeType=barcodeType, addedBy=person)
        ScannedProducts.objects.create(product=productObj, owner=person)
        
        if imageFile is not None:
            productImage = ProductImage(product=productObj, image= imageFile)
            productImage.save()
        
        response = '%s : %s' % ( productObj.description, productObj.barcode)
        
    return response

@login_required
def addProductDetails(request, productBarCode):
    person = request.user
    description = request.GET['description']
    expiresInDays = float(request.GET['expiresInDays'])
        
    productObj = Product.objects.get(barcode = productBarCode)

    productObj.addedBy = person
    productObj.description = description
    productObj.expiresInDays = expiresInDays
    productObj.save()
    
    response_data = {'status': 'success','response': productObj.natural_key()}
    
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    
@login_required
def getRecords(request):
    
    person = request.user
    scannedProducts = ScannedProducts.objects.filter(owner=person) #.order_by('product__description')

#    groupedItems = groupByProduct(scannedProducts)
    serliazedData = serializers.serialize("json", scannedProducts ,indent=2, use_natural_keys=True)
    return HttpResponse(serliazedData, mimetype="application/json")
#    return HttpResponse(json.dumps(productDetails), mimetype="application/json")

def groupByProduct(input):
    output = []
    lastItem = None
    lastItemCounter = 0
    groupItem = []
    for iter in xrange(len(input)):
        currentItem = input[iter]
        if (lastItem is None) or ( currentItem.product == lastItem.product  ) and  iter < len(input) -1 :
            lastItemCounter = lastItemCounter + 1
            groupItem.append(currentItem.addingDate)
        else:
            output.append({'counter': lastItemCounter, 'item': lastItem ,'dates':groupItem})
            groupItem = []
            lastItemCounter = 0
            
        lastItem = currentItem
        
    return output
            
        
def base(request):
    
    return render(request, 'barcodeServer/index.html' , {"foo": "bar"},
        content_type="application/xhtml+xml")   