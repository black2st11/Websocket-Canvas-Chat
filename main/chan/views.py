from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
# Create your views here.

def index(requset):
    return render(requset, 'chan/index.html', {})

def draw(request, room_name):
    return render(request, 'chan/draw.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })




