from django.shortcuts import render
#新加入的function
def testPage(request):
    return render(request, "chatroom.html")

def testPage(request):
    i = [x for x in range(1,10)] #一個0~9的list
    data = {
        "data1":"資料1",
        "data2":"資料2",
        "list":i,
    }
    return render(request, "chatroom.html", data)