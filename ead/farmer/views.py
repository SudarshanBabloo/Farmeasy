from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from user_auth.models import farmer,Inventory,consumer,Comment,retailer
from mongoengine import *
import base64
from PIL import Image
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.Farmers
from django.core.files.uploadedfile import InMemoryUploadedFile,UploadedFile
from gridfs import GridFS

from datetime import datetime

#db = client.test_database
def index(request):
    return render(request,'farmer/index.html')

def edit(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    if request.method == 'POST':
        empty=''
        first_name=request.POST['f_name']
        last_name=request.POST['l_name']
        phone_no=request.POST['phone_no']
        address=request.POST['address']
        farm.f_name = first_name
        farm.l_name = last_name
        farm.phone_no = phone_no
        farm.address = address
        farm.save()
        message = "Your profile has been edited"
        #messages.info(request, 'Your password has been changed successfully!')
        content = {'p':farm,'messages':message,'no':0,'status':2}
        return render(request, 'farmer/profile.html',content)
    content = {'p':farm,'no':1,'status':2}
    return render(request, 'farmer/profile.html',content)

def viewreview(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    content = {'reviews':farm.reviews,'status':2}
    return render(request,'farmer/view_reviews.html',content)

def reviewtext(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    #cons = consumer.objects(email = mail).get()
    name = farm.name
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        date = datetime.now()
        print(content,rating)
        comment = Comment(content=content,rating=rating,name = name,date=date)
        farm.reviews.append(comment)
        farm.save()   
        return viewreview(request)

    return render(request, 'farmer/writereview.html')


def getrequests(request):
    get_request = requests.objects.filter(farmer_id = farmer.id , status = 0)
    paginator = paginator(get_request,8)
    page = request.GET.get('page')
    # ?page=2
    posts = paginator.get_page(page)
    content = {'posts':posts}
    return render(request,'farmer/get_request.html',content)


def invview(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    ilist = []
    for i in farm.stock:
        lmg = i["photo"].grid_id
        col = db.images.chunks.find({"files_id":lmg})
        my_string = base64.b64encode(col[0]["data"])
        l = my_string.decode('utf-8')
        ilist.append(l)
    print(l)
    map = zip(farm.stock,ilist)
    content = {'stocks':farm.stock,'status':2,'map':map}
    return render(request,'farmer/inv.html',content)

def add(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    already = 0
    if request.method == 'POST':
        crop = request.POST.get('crop')
        qty = request.POST.get('qty')
        img = request.FILES["img"]
        
        # bmg =InMemoryUploadedFile(img)
        # print(bmg)
        # with open(bmg, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())
        
        # print(encoded_string)

        qty = int(qty)
        w = crop[0]
        if w.isupper():
            w = w.lower()
        else:
            w = w.upper()
        worp = w+crop[1:]
        for i in farm.stock:
            if i.crop == crop or i.crop == worp:
                already = 1
                i.qty = qty + i.qty
                farm.save()
        
        if already == 0:
            inv = Inventory(crop = crop,qty=qty,photo = img)
            #inv.photo.put(img, content_type = 'image/jpeg')
            #inv.save()
            farm.stock.append(inv)
            farm.save()

        return invview(request)
    content = {'status':2}
    return render(request, 'farmer/add.html', content)

def subtract(request,farmer,crop,qty):
    farmer = farmer.objects(farmer_id=100).get()
    
    for i in farmer.stock:
            if i.crop == crop:
                i.qty = i.qty - qty
                farmer.save()
        


def history(request):
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    content = {'posts':history,'status':2}
    return render(request,'farmer/historydone.html',content)

def currentview(request):
    history = history.objects.filter(farmer_id = farmer.id,status = 1)
    content = {'posts':history}
    return render(request,'farmer/history.html',content)

def profileview(request):
    if request.method == 'POST':
        name=request.POST['name']
        address=request.POST['address']
        phone_no=request.POST['phone']
        email=request.POST['email']
        farmer_id=request.POST['id']
        saveform = Farmer(farmer_id = farmer_id,name=name,address=address,phone_no=phone_no,email=email)
        saveform.save()
        return HttpResponse('Done')
    else:
        return render(request,'farmer/test.html')

def store_home(request):
    content = {'status':2}
    return render(request,'farmer/store.html',content)


def cat_page(request,cid):
    ret_mail = "abc@kartk5.com"
    ret = retailer.objects(email=ret_mail).get()
    prod = []
    prod_image = []
    for i in ret.products:
        if i.cat_id == cid:
            prod.append(i)
            lmg = i["photo"].grid_id
            col = db.images.chunks.find({"files_id":lmg})
            my_string = base64.b64encode(col[0]["data"])
            l = my_string.decode('utf-8')
            prod_image.append(l)
    map = zip(prod,prod_image) 
    content = {'product':prod,'map':map,'status':2,'cid':cid}
    return render(request,'farmer/cat.html',content)

def cat_page_by_price(request,cid):
    ret_mail = "abc@kartk5.com"
    ret = retailer.objects(email=ret_mail).get()
    prod_image = []
    prod = []
    for i in ret.products:
        if i.cat_id == cid:
            prod.append(i)
            lmg = i["photo"].grid_id
            col = db.images.chunks.find({"files_id":lmg})
            my_string = base64.b64encode(col[0]["data"])
            l = my_string.decode('utf-8')
            prod_image.append(l)

    map = list(zip(prod,prod_image))
    map.sort(key=lambda x:x[0].cost)
    
    
    content = {'product':prod,'map':map,'status':2,'cid':cid}
    return render(request,'farmer/cat.html',content)

def cat_page_by_rating(request,cid):
    ret_mail = "abc@kartk5.com"
    ret = retailer.objects(email=ret_mail).get()
    prod_image = []
    prod = []
    for i in ret.products:
        if i.cat_id == cid:
            prod.append(i)
            lmg = i["photo"].grid_id
            col = db.images.chunks.find({"files_id":lmg})
            my_string = base64.b64encode(col[0]["data"])
            l = my_string.decode('utf-8')
            prod_image.append(l)
    
    
    map = list(zip(prod,prod_image))
    map.sort(key=lambda x:x[0].cost)
    content = {'product':prod,'map':map,'status':2,'cid':cid}
    return render(request,'farmer/cat.html',content)

def prod_page(request,pid):
    ret_mail = "abc@kartk5.com"
    ret = retailer.objects(email=ret_mail).get()
    
    for i in ret.products:
        if i.product_id == pid:
            prod = i
            lmg = i["photo"].grid_id
            col = db.images.chunks.find({"files_id":lmg})
            my_string = base64.b64encode(col[0]["data"])
            l = my_string.decode('utf-8')
            prod_image = l
            break
    print(prod.reviews)
    content = {'prod':prod,'prod_image':prod_image,'status':2}
    return render(request,'farmer/prod.html',content)


def prod_review(request,pid):
    ret_mail = "abc@kartk5.com"
    ret = retailer.objects(email=ret_mail).get()
    mail = request.session['username']
    farm = farmer.objects(email=mail).get()
    name = farm.l_name
 
    for i in ret.products:
        if i.product_id == pid:
            current = i
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = request.POST.get('rate')
        rating = int(rating)
        date = datetime.now()
        print(content,rating)
        comment = Comment(title=title,content=content,rating=rating,name = name,date=date)
        current.reviews.append(comment)
        print(current.reviews)
        if current.rating != None:
            current.rating = (current.rating+rating)/len(current.reviews)+1
        else:
            current.rating = rating
        ret.save()   
        return prod_page(request,pid)
    else:
        content = {'status':2}
        return render(request,'farmer/review_prod.html',content)



def star(request):
    content = {'rat':3}
    return render(request,'farmer/rating.html',content)

