import datetime
from django.shortcuts import render
from django.http import HttpResponse   
from django.shortcuts import render 

def home(request):
    return HttpResponse("Hello, Django!")

def hello_there(request):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'main/home.html',
    )