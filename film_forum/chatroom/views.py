from django.shortcuts import render
#新加入的function
def testPage(request):
    return render(request, "chatroom.html")