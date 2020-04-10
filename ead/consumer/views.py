from django.shortcuts import render

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
