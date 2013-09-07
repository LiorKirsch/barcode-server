from django.http import HttpResponse
from django.shortcuts import render_to_response
from forms import PhotoForm, BarcodeForm

from models import Product, ProductImage, Scanner, ScannedProducts
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
import json

import os
import tempfile
import urllib2
from subprocess import Popen, PIPE, STDOUT
import string, random

def addToPerson(request, machineID, personID):
    person = User.objects.get(uniqueId=personID)
    
    try:
        scanner = Scanner.objects.get(uniqueId=machineID)
        scanner.owner = person
        scanner.save()
    except Scanner.DoesNotExist:
        scanner = Scanner(owner=person, uniqueId=machineID )
        scanner.save()

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
        productObj, created = Product.objects.get_or_create(barcode = barcode, barcodeType=barcodeType)
        ScannedProducts.objects.create(product=productObj, owner=person)
        
        if imageFile is not None:
            productImage = ProductImage(product=productObj, image= imageFile)
            productImage.save()
        
        response = '%s : %s' % ( productObj.description, productObj.barcode)
        
    return response