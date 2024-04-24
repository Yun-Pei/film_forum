from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import ForumsForm
from .models import *

# Create your views here.
def forum(request):
    if request.method == "GET":
        return render(request, "forum.html")
    
def movie(request):
    if request.method == "GET":
        form = ForumsForm()

    elif request.method == 'POST':
        form = ForumsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            m_id = form.cleaned_data['m_id']
            
            # 获取提交表单的时间
            submission_time = timezone.now()
            
            # 将数据保存到数据库
            forum = Forums(title=title, content=content, m_id=m_id, time=submission_time)
            forum.save()
            
            # 重定向到成功页面或其他页面
            return redirect('movie')  # 導入路徑
        else:
            form = ForumsForm()

    return render(request, "movie.html", context={'form':form})