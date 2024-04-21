from datetime import datetime

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import user as UserModel
from .models import StoryModel
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseForbidden
import json


#@api_view(["GET"])
#def test(request):
    #print("hello")
    #return HttpResponse("hello")

# Create your views here.
@api_view(["POST"])
def login_view(request):
    #if request.method == 'POST':
        #username = request.POST.get('username')
        #password = request.POST.get('password')

        #user = authenticate(request, username=username, password=password)
    if request.method == 'POST':  ## 如果提交表单信息POST
        print(request.POST)
        username = request.POST.get('username')  ## 获取用户名
        password = request.POST.get('password')  ## 获取提交的密码
        print(username)
        print(password)
        #print(request.POST)

    if username and password:
        user = UserModel.objects.get(username=username,password=password)
        print(user)
        if user:
            #print("1")
            request.session['is_login'] = True
            request.session['user_id'] = request.user.id
            request.session['username'] = user.username
            #print(request.session.get('is_login'))
        return HttpResponse(status=200)
    else:
        error_message = "Invalid username or password."
        response = HttpResponse(error_message, content_type='text/plain')
        response.status_code = 401
        return response

@api_view(["POST"])
def logout_view(request):
    try:
        logout(request)
        request.session.clear()  # 清除会话信息
        response = HttpResponse("Goodbye! You have been logged out.", content_type='text/plain')
        response.status_code = 200
        return response
    except Exception as e:
        response = HttpResponse(f"An error: {e}",content_type='text/plain')
        response.status_code = 400
        return response

@csrf_exempt
def stories(request):
    if request.method == "POST":
        #print(request.user.id,request.session.get('is_login'))
        # 检查用户是否已登录，如果不是，则直接返回403 Forbidden
        if 'is_login' not in request.session or not request.session.get('is_login'):
            return HttpResponseForbidden("User is not authenticated.", content_type="text/plain")

        # 解析JSON请求体

        body_str = request.body.decode('utf-8')
        data = json.loads(body_str)
        headline = data.get('headline', '')
        category = data.get('category', '')
        region = data.get('region', '')
        details = data.get('details', '')

        # 验证必填字段
        if not headline or not category or not region or not details:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        print(request.session['username'])
        # 创建新故事对象并保存到数据库
        story = StoryModel(
            headline=headline,
            category=category,
            region=region,
            details=details,
            author=request.session['username'],  # 假设request.user.username是作者名
            date=timezone.now()
        )
        story.save()

        # 如果故事成功添加到数据库，响应201 Created状态码
        response_data = {"message": "Story created successfully"}
        return JsonResponse(response_data, status=201)
    elif request.method == "GET":
        story_category = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date_str = request.GET.get('story_date', '*')

        # 尝试将日期字符串转换为日期对象，如果 "*" 或无效格式则忽略过滤条件
        try:
            story_date = datetime.strptime(story_date_str, '%Y-%m-%d').date()
        except ValueError:
            story_date = None

        # 构建查询条件
        queryset = StoryModel.objects.all()

        # 过滤故事
        if story_category != '*':
            queryset = queryset.filter(category=story_category)
        if story_region != '*':
            queryset = queryset.filter(region=story_region)
        if story_date:
            queryset = queryset.filter(pub_date__gte=story_date)

        # 转换为JSON响应格式
        stories = [{'key': story.uniqueKey,
                    'headline': story.headline,
                    'story_cat': story.category,
                    'story_region': story.region,
                    'author': story.author,
                    'story_date': story.date.strftime('%Y-%m-%d'),
                    'story_details': story.details}
                   for story in queryset]
        print(stories)
        # 返回响应
        if queryset.exists():
            return JsonResponse({'stories': stories})
        else:
            return HttpResponse("No stories found matching the given criteria.", status=404,
                                content_type="text/plain")
    else:
        print(11111)

@api_view(["DELETE"])
def delete_story(request, key):
    # 检查用户是否已登录，可以使用适当的身份验证机制
    if 'is_login' not in request.session or not request.session.get('is_login'):
        return HttpResponseForbidden("User is not authenticated.", content_type="text/plain")

    # 查找要删除的故事
    story = get_object_or_404(StoryModel, uniqueKey=key)

    # 删除故事
    story.delete()

    return HttpResponse(status=200)