from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from user_auth.models import farmer,Inventory,consumer,Comment,retailer,Product
from mongoengine import *
import base64
import random
from PIL import Image
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.Farmers
from django.core.files.uploadedfile import InMemoryUploadedFile,UploadedFile
from gridfs import GridFS

from datetime import datetime

def index(request):
    content = {'status':1}
    return render(request,'vendor/index.html',content)


def history(request):
    content = {'status':1}
    return render(request,'vendor/index.html',content)

def add_new(request):
    mail = request.session['username']
    ret = retailer.objects(email=mail).get()
    already = 0
    if request.method == 'POST':
        product_id = random.randint(0,1000000)
        cat_id = request.POST.get('cat')
        name = request.POST.get('name')
        qty = request.POST.get('qty')
        img = request.FILES["img"]
        cost = request.POST.get('cost')
        desc = request.POST.get('desc')
        qty = int(qty)
        cost = int(cost)
        w = name[0]
        if w.isupper():
            pass
        else:
            w = w.upper()
        name = w+name[1:]

        pro = Product(product_id = product_id,cat_id = cat_id,name = name,description=desc,photo = img,stock=qty,cost=cost)
        #inv.photo.put(img, content_type = 'image/jpeg')
        #inv.save()
        ret.products.append(pro)
        ret.save()

        return prod_profile(request)
    content = {'status':1}
    return render(request, 'vendor/add_new.html', content)


def add(request,pid):
    mail = request.session['username']
    ret = retailer.objects(email=mail).get()
    for i in ret.products:
        if i.product_id == pid:
            break

    if request.method == 'POST':
        cost = request.POST.get('cost')
        qty = request.POST.get('qty')
        cost = int(cost)
        qty = int(qty)
        i.stock = i.stock + qty
        i.cost = cost
        ret.save()
        
        return prod_profile(request)
    content = {'status':1,'prod':i}
    return render(request,'vendor/add.html',content)
    
    
def subtract(request,pid):
    mail = request.session['username']
    print(mail)
    ret = retailer.objects(email=mail).get()
    if request.method == 'POST':
        for i in ret.products:
            if i.product_id == pid:
                qty = request.POST.get('qty')
                cost = request.POST.get('cost')

                i.qty = i.qty - qty
                i.cost = cost
                ret.save()
                break
    


def prod_profile(request):
    mail = request.session['username']
    ret = retailer.objects(email=mail).get()
    ilist = []
    for i in ret.products:
        lmg = i["photo"].grid_id
        col = db.images.chunks.find({"files_id":lmg})
        my_string = base64.b64encode(col[0]["data"])
        l = my_string.decode('utf-8')
        ilist.append(l)
    
    map = zip(ret.products,ilist)
    content = {'prods':ret.products,'map':map,'status':1}
    return render(request,'vendor/inv.html',content)
