from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    print('hii')
    if 'username' not in request.session:
        return HttpResponse('Log in to chat') 
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.session['username'])),
    })