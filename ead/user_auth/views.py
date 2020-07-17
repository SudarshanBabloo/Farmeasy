from user_auth.models import consumer,retailer,farmer
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .tokens import account_activation_token
from farmer.views import add
import hashlib

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# Create your views here.
def home(request):
    #x=crops(vegetable="x",quantity=1)
    #x.save()
    return render(request,'user_auth/home.html')





def check_user_exists(request,email):
    if request==None:
        return (None,None)
    if request.session.has_key('username'):
        request.session.flush()
    for u in consumer.objects.all():
        if u["email"] == email:
            return (True,u,"consumer")
    for u in retailer.objects.all():
        if u["email"] == email:
            return (True,u,"retailer")
    for u in farmer.objects.all():
        if u["email"] == email:
            return (True,u,"farmer")                
    return (False,None,"None")




def signup(request):
    if request.method=='GET':
        if request.session.has_key('username'):
            return loggedinhome(request)
    if request.method=='POST':
        if "email" in request.POST and "password" in request.POST and "Retype_password" in request.POST  :
            # print("passed1")
            if request.POST["password"] == request.POST["Retype_password"]:
                if len(request.POST["phone_no"])==10:

                # print("passed2")
                    if not check_user_exists(request,request.POST["email"])[0]:#check unique user or not
                        mail = request.POST["email"]
                        password=encrypt_string(str(request.POST["password"]))
                        if(request.POST["user_type"]=="consumer"):
                            user = consumer(email=request.POST["email"], password=password,f_name=request.POST["f_name"],l_name=request.POST["l_name"],address=request.POST["address"],phone_no=request.POST["phone_no"],created_date=datetime.datetime.now(),location=[float(request.POST['latitude']), float(request.POST['longitude'])])
                            user.email_verified = False
                            user.save()
                            request.session['status']=0
                        elif(request.POST["user_type"]=="retailer"):
                            user = retailer(email=request.POST["email"], password=password,f_name=request.POST["f_name"],l_name=request.POST["l_name"],address=request.POST["address"],phone_no=request.POST["phone_no"],created_date=datetime.datetime.now(),location=[float(request.POST['latitude']), float(request.POST['longitude'])])
                            user.email_verified = False
                            user.save()
                            request.session['status']=1
                        elif(request.POST["user_type"]=="farmer"):
                            user = farmer(email=request.POST["email"], password=password,f_name=request.POST["f_name"],l_name=request.POST["l_name"],address=request.POST["address"],phone_no=request.POST["phone_no"],created_date=datetime.datetime.now(),location=[float(request.POST['latitude']), float(request.POST['longitude'])])
                            user.email_verified = False
                            user.save()
                            request.session['status']=2        
                        request.session['username'] = request.POST["email"]
                        #return loggedinhome(request)
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your account.'
                        message = render_to_string('actimail.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        })
                        to_email = mail
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        return render(request,'user_auth/verify.html')

                    else:
                        return render(request,'user_auth/index.html',{'warning':"User already exists"})
                else:
                    return render(request,'user_auth/index.html',{'warning':"Phone Number must be 10 digit"})

            else:
                return render(request,'user_auth/index.html',{'warning':"Password doesn't match"})
        else:
            return render(request,'user_auth/index.html',{'warning':"Fill all elements"})
    else:
        return render(request,'user_auth/index.html')

e,u=check_user_exists(None,'a@gmail.com')
def login(request):
    if request.method=='GET':
        if request.session.has_key('username'):
            return loggedinhome(request)
        else:
            return render(request,'user_auth/newlogin.html',{'type':'username'})
    elif request.method=='POST':
        if "1" in request.POST:
            if "email" in request.POST:
                print("see man")
                e,u,t = check_user_exists(request,request.POST["email"])
                if e:
                    
                    return render(request,'user_auth/newlogin.html',{'type':'password','email':str(request.POST["email"])})
                    
                    
                else:
                    return render(request,'user_auth/newlogin.html',{'warning':"User dosent exist"})
            else:
                return render(request,'user_auth/newlogin.html',{'warning':"Fill all elements"})
        elif "2" in request.POST:        
            if "password" in request.POST:
                print("hii came here")
                print(str(request.POST["2"]))
                e,u,t = check_user_exists(request,str(request.POST["2"]))
                password=encrypt_string(str(request.POST["password"]))
                if password==u["password"]:
                    request.session['username'] = request.POST["2"]
                    if t=="consumer":
                        request.session['status']=0
                    if t=="retailer":
                        request.session['status']=1
                    if t=="farmer":
                        request.session['status']=2             
                    return loggedinhome(request)
                
                else:
                    return render(request,'user_auth/newlogin.html',{'warning':"Incorrect Password",'type':'password','email':str(request.POST["2"])})
            
            else:
                return render(request,'user_auth/newlogin.html',{'warning':"Fill all elements"})    

    return render(request,'user_auth/newlogin.html',{})


def activate(request, uidb64, token):
    print(request.session['status'])
    if request.session["status"]==0:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))

            user = consumer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, consumer.DoesNotExist):
            user = None
    if request.session["status"]==1:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))

            user = retailer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, retailer.DoesNotExist):
            user = None
    if request.session["status"]==2:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))

            user = farmer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, farmer.DoesNotExist):
            user = None                
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect('user_auth:loggedinhome')
    else:
        return HttpResponse('user_auth:login')


def loggedinhome(request):
    user_type='';status=4
    if request.session.has_key('username'):
        status=1
        
        if request.session['status']==0:
            user_type='consumer'
        if request.session['status']==1:
            user_type='retailer'
            return redirect('vendor:index')
        if request.session['status']==2:
            user_type='farmer'
            return redirect('farmer:add') 
    print(user_type)               

    return render(request,'user_auth/home.html',{'status':status,'user_type':user_type})

def logout(request):
    if request.session.has_key('username'):
        request.session.flush()
    return redirect('user_auth:loggedinhome')

def verify_email(request):
    return render(request,'user_auth/verify_email.html',{})



def resetpasswordview(request):
    if request.method == 'POST':
        mail = request.POST["email"]
        e,u,t = check_user_exists(request,mail)
                
        request.session['username'] = mail
        if t=="consumer":
            request.session['status']=0
        if t=="retailer":
            request.session['status']=1
        if t=="farmer":
            request.session['status']=2
        if request.session['status']==0:
            user = consumer.objects.get(email=mail)
        if request.session['status']==1:
            user = retailer.objects.get(email=mail)
        if request.session['status']==2:
            user = farmer.objects.get(email=mail)        
        current_site = get_current_site(request)
        mail_subject = 'Password Reset Link.'
        message = render_to_string('reset_confirm_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        print('came here reset')
        send_mail(mail_subject, message, 'harshaofficial852@gmail.com', [mail])
        return render(request, 'reset_email.html', {'email': mail,'message':'Email has been sent to '+mail})
    else:
        return render(request, 'reset_email.html', {'message':''})


def display_reset_password(request, uidb64, token):
    if request.session['status']==0:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = consumer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, consumer.DoesNotExist):
            user = None
    if request.session['status']==1:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = retailer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, retailer.DoesNotExist):
            user = None     
    if request.session['status']==2:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = farmer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, farmer.DoesNotExist):
            user = None           
    if user is not None and account_activation_token.check_token(user, token):
        # login(request, user)
        request.session['email'] = user.email
        return redirect('user_auth:save_password')

    else:
        return HttpResponse('Activation link is invalid!')


def save_password(request):
    if request.method == "POST":
        password=encrypt_string(str(request.POST["password"]))
        mail = request.session['email']
        if request.session['status']==0:
            user = consumer.objects.get(email=mail)
        if request.session['status']==1:
            user = retailer.objects.get(email=mail)
        if request.session['status']==2:
            user = farmer.objects.get(email=mail)
    

        print(user)
        
        user.update(password = password)
        return render(request, 'after_reset.html')
    else:
        return render(request, 'reset_password.html')