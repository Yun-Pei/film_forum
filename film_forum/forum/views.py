from django.shortcuts import render

# Create your views here.
def forum(request):
    if request.method == "GET":
        return render(request, "forum.html")