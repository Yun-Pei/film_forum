from django.shortcuts import render
from .forms import ForumsForm

# Create your views here.
def forum(request):
    if request.method == "GET":
        return render(request, "forum.html")
    
def movie(request):
    if request.method == "GET":
        form = ForumsForm()

        return render(request, "movie.html", context={'form':form})