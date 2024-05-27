from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from member.models import *
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.utils import timezone

#新加入的function
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def testPage(request):
    return render(request, "chatroom.html")

def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # context = {}

    if request.user.is_authenticated:
        user_id = request.user.id

    userList = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM User
            WHERE User.id = %s
        """, [user_id])
        userInfo = dictfetchall(cursor)
        userList.append(userInfo)

    chatlist = list()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.username, User.img, Message.time, Chatroom.aid, Chatroom.be_uid, Chatroom.uid_id, Message.conent
            FROM Chatroom
            JOIN User ON User.id = Chatroom.be_uid
            JOIN (
                SELECT aid_id, MAX(time) AS latest_time
                FROM Message
                GROUP BY aid_id
            ) AS LatestMessage ON LatestMessage.aid_id = Chatroom.aid
            JOIN Message ON Message.aid_id = LatestMessage.aid_id AND Message.time = LatestMessage.latest_time
            WHERE uid_id = %s
            ORDER BY Chatroom.aid
        """, [user_id])
    
        user_chatrooms = dictfetchall(cursor)
        # print(user_chatrooms)

    # 获取以用户自己为 be_uid 的聊天室最新消息（用户信息由 be_uid 提供）
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.username, User.img, Message.time, Chatroom.aid, Chatroom.be_uid, Chatroom.uid_id, Message.conent
            FROM Chatroom
            JOIN User ON User.id = Chatroom.uid_id
            JOIN (
                SELECT aid_id, MAX(time) AS latest_time
                FROM Message
                GROUP BY aid_id
            ) AS LatestMessage ON LatestMessage.aid_id = Chatroom.aid
            JOIN Message ON Message.aid_id = LatestMessage.aid_id AND Message.time = LatestMessage.latest_time
            WHERE be_uid = %s
            ORDER BY Chatroom.aid
        """, [user_id])
    
        be_user_chatrooms = dictfetchall(cursor)
        # print(be_user_chatrooms)

        for user_chatroom in user_chatrooms:
            for be_user_chatroom in be_user_chatrooms:
                if be_user_chatroom['be_uid'] == user_chatroom['uid_id'] and be_user_chatroom['uid_id'] == user_chatroom['be_uid']:
                    # print(f'be_user_chatroom[aid]:{be_user_chatroom['aid']}, be_user_chatroom[be_uid]:{be_user_chatroom['be_uid'], }')
                    if user_chatroom['conent'] != None or be_user_chatroom['conent'] != None:
                        if be_user_chatroom['time'] > user_chatroom['time']:
                            # chatlist.append(be_user_chatroom)
                            user_chatroom['conent'] = None
                        else:
                            # chatlist.append(be_user_chatroom)
                            be_user_chatroom['conent'] = None
        
        for user_chatroom in user_chatrooms:
            if user_chatroom['conent'] != None:
                chatlist.append(user_chatroom)
        for be_user_chatroom in be_user_chatrooms:
            if be_user_chatroom['conent'] != None:
                chatlist.append(be_user_chatroom)

        # 对 chatlist 按时间降序排序
        chatlist.sort(key=lambda x: x['time'], reverse=True)

        # print("THE result: ")
        print(f'THE result: {chatlist}')      
        # print(be_user_chatrooms)

    # chatlist.append(user_as_be_uid_chatrooms)
    # print(user_id, chatlist)

    Nochatlist = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM Chatroom AS C1
            JOIN User ON User.id = C1.be_uid
            WHERE C1.uid_id = %s
            AND NOT EXISTS (
                SELECT 1
                FROM Chatroom AS C2
                JOIN Message ON Message.aid_id = C2.aid
                WHERE C2.uid_id = %s
                AND C1.aid = C2.aid
            )
        """, [user_id, user_id])
        Nochatroom = dictfetchall(cursor)
        Nochatlist.append(Nochatroom)

    


    # messagelist = list()
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT Message.time, Message.conent
    #         FROM Message
    #         JOIN Chatroom ON Chatroom.aid = Message.aid_id
    #         WHERE Message.aid_id = %s
    #         ORDER BY Message.time
    #     """, [user_id])
    #     messageResult = dictfetchall(cursor)
    #     messagelist.append(messageResult)
    #     print(messagelist)
    # messagelist = list()
    if request.method == 'POST':
        if request.POST.get('mode') == 'sendMessage':
            time = timezone.now()
            content = request.POST.get('messageContent')
            chatroom_id = request.POST.get('aid')
            print('chatroom_id: ', chatroom_id)

            # 获取当前用户的ID
            user_id = request.user.id

            # 检查当前聊天室的发送者是否是当前用户
            current_chatroom = Chatroom.objects.get(aid=chatroom_id)
            if current_chatroom.uid_id != user_id:
                # 找到发送者是当前用户且接收者是原始发送者的聊天室
                chatroom = Chatroom.objects.filter(uid_id=user_id, be_uid=current_chatroom.uid_id).first()
                if chatroom:
                    # 创建消息并保存到该聊天室
                    NewMessage = Message(time=time, conent=content, aid_id=chatroom.aid)
                    NewMessage.save()
                    return HttpResponseRedirect('/chat/')

            # print(user_id, time, content, chatroom_id)
            NewMessage = Message(time=time, conent=content, aid_id=chatroom_id)
            NewMessage.save()
            return HttpResponseRedirect('/chat/')
        elif request.POST.get('mode') == 'sendAid':
            chatroom_aid = request.POST.get('aid')
            chatroomUid = request.POST.get('chatroomUid')
            chatroomBe = request.POST.get('chatroomBe')
            print(chatroomUid, chatroomBe)
            # messagelist = list()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Chatroom.uid_id, Chatroom.be_uid, Message.conent, DATE_FORMAT(Message.time, '%%Y/%%m/%%d %%H:%%i') AS formatted_datetime
                    FROM Message
                    JOIN Chatroom ON Chatroom.aid = Message.aid_id
                    WHERE (Chatroom.uid_id = %s AND Chatroom.be_uid = %s) OR (Chatroom.uid_id = %s AND Chatroom.be_uid = %s)
                    ORDER BY Message.time
                """, [chatroomBe, chatroomUid, chatroomUid, chatroomBe])
                message_result = cursor.fetchall()
            # 將訊息數據轉換為 JSON 格式
            messages = []
            for row in message_result:
                message = {
                    'uid': row[0],
                    'beuid': row[1],
                    'content': row[2],  # 設置為您的 content 欄位
                    'time': row[3],     # 設置為您的 time 欄位
                    # 添加其他欄位...
                }
                messages.append(message)
            return JsonResponse(messages, safe=False)

    # print(messagelist)      
    # return render(request, "chatPage.html", {'chatlist': chatlist, 'message_result': message_result, 'Nochatlist':Nochatlist})
    return render(request, "chatPage.html", {'chatlist': chatlist, 'Nochatlist':Nochatlist, 'userList':userList})

@csrf_protect
def addChatPage(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.get('mode') == 'addFriends':
                uid = request.user.id
                buid = request.POST.get('be_uid')
                print(uid, buid)
                # 檢查資料庫中是否已存在相同組合的資料
                existing_chat = Chatroom.objects.filter(uid_id=uid, be_uid=buid).exists()
                if not existing_chat:
                    newChat1 = Chatroom(uid_id=uid, be_uid=buid)
                    newChat1.save()
                    newChat2 = Chatroom(uid_id=buid, be_uid=uid)
                    newChat2.save()
                    return HttpResponseRedirect('/chat/')
    return render(request, 'addChatPage.html')

def search_member(request):
    query = request.POST.get('q')
    members = []
    if query and request.user.is_authenticated:
        user_id = request.user.id
        try:
            # 使用exact查詢條件來完全匹配使用者名稱
            member = User.objects.get(username=query)
            if user_id != member.id:
                members.append(member)
        except User.DoesNotExist:
            pass  # 如果沒有找到相應的使用者，就不添加到結果列表中
    return render(request, 'addChatPage.html', {'members': members})

# class MemberSearchView(ListView):
#     model = User
#     template_name = 'addChatPage.html'
#     context_object_name = 'users'

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             queryset = User.objects.filter(username__icontains=query)
#             if self.request.user.is_authenticated:
#                 queryset = queryset.exclude(id=self.request.user.id)
#             return queryset
#         return User.objects.none()

# def autocomplete(request):
#     if 'term' in request.GET:
#         qs = User.objects.filter(username__istartwith=request.GET('term'))
#         usernames = list()
#         for user in qs:
#             usernames.append(User.username)
#     return JsonResponse(usernames, safe=False)

# def search_members(request):
#     query = request.GET.get("q")
#     if query:
#         return User.objects.filter(username__icontains=query)
#     return render(request, 'addChatPage.html')