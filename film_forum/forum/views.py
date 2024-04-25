from django.shortcuts import render, redirect
from django.utils import timezone
# from .forms import ForumsForm
from .models import *

# Create your views here.
def forum(request):
    if request.method == "GET":
        return render(request, "forum.html")
    
