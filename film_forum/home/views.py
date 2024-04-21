from django.shortcuts import render
#新加入的function
def testPage(request):
    return render(request, "index.html")

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Blog.objects.all().filter(title=search)
        return render(request, 'searchbar.html', {'post':post})
    
