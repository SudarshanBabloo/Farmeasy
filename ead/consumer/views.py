from django.shortcuts import render, redirect
from user_auth.models import farmer,Inventory,consumer,Comment,retailer,transactions
import hashlib
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.
def reviewtext(request,f_mail):
    mail = request.session['username']
    farmer = Farmer.objects(email=f_mail).get()
    cons = consumer.objects(email = mail).get()
    name = cons.name
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        date = datetime.now()
        print(content,rating)
        comment = Comment(content=content,rating=rating,name = name,date=date)
        farmer.reviews.append(comment)
        farmer.save()   
        return viewreview(request)

    return render(request, 'farmer/writereview.html')


def search(request):
    if request.session.has_key('username'):
        u = consumer.objects.get(email = request.session['username'])
        if request.method == 'GET':
            return render(request, 'consumer/search.html')
        elif request.method == 'POST':
            product = request.POST.get('product')
            distance = request.POST.get('distance')
            quantity = request.POST.get('quantity')
            farmers = farmer.objects(stock__crop = product, location__geo_within_center=[u.location['coordinates'], float(distance)])
            vlist = []
            for i in farmers:
                a = {}
                for j in i.stock:
                    if j.crop == product:
                        if j.qty > int(quantity):
                            a['name'] = i.f_name
                            a['product'] = product
                            a['stock'] = j.qty
                            a['enc'] = product + '-' + urlsafe_base64_encode(force_bytes(i.email))
                vlist.append(a)
            print(vlist)
            return render(request, 'consumer/search.html', {'vlist': vlist})
    else:
        return redirect('user_auth:login')

def farmer_page(request, enc):
    if request.session.has_key('username'):
        if request.method == 'GET':
            u = consumer.objects.get(email = request.session['username'])
            email_enc = enc.split('-')[1]
            product = enc.split('-')[0]
            a = {}
            a['email'] = email_enc
            a['product'] = product
            return render(request, 'consumer/farmer_page.html', {'a': a})
        elif request.method == 'POST':
            u = consumer.objects.get(email = request.session['username'])
            f = farmer.objects.get(email = force_text(urlsafe_base64_decode(request.POST.get('email'))))
            t = transactions(price = request.POST.get('price'), quantity = request.POST.get('quantity'), product = request.POST.get('product'), consumer_id = u, farmer_id = f, deal_status = "c_accepted")
            t.save()
            return render(request, 'consumer/farmer_page.html')
    else:
        return redirect('user_auth:login')