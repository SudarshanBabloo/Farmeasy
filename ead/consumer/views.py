from django.shortcuts import render
from user_auth.models import farmer,Inventory,consumer,Comment,retailer

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
    if request.method == 'GET':
        return render(request, 'consumer/search.html')
    elif request.method == 'POST':
        product = request.POST.get('product')
        distance = request.POST.get('distance')
        farmers = farmer.objects(stock__crop = product, location__geo_within_center=[(18.32406, 78.5), float(distance)])
        # vlist = []
        # for i in farmers:
        #     a = {}
        #     a['name'] = i.f_name
        #     a['stock'] = 
        print(farmers)
        return render(request, 'consumer/search.html')