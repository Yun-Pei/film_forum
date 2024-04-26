from django.shortcuts import render, redirect
#新加入的function
def testPage(request):
    return render(request, "chatroom.html")

def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)