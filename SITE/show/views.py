from django.shortcuts import render, Http404, redirect
from .models import Actor, Movie
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse

from datetime import datetime
# Create your views here.

def show_movie(request):
    movie = Movie.objects.all()
    movie_list = []
    for m in movie:
        movie_list.append(m)
    l=len(movie_list)
    paginator = Paginator(movie_list, 20)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            movie_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            movie_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            movie_list = paginator.page(paginator.num_pages)

    template_view = 'movie_page.html'
    return render(request, template_view, {'movie': movie_list,'len':l})


def show_actor(request):
    actor = Actor.objects.all()
    actor_list = []
    for a in actor:
        actor_list.append(a)
    l=len(actor_list)
    paginator = Paginator(actor_list, 20)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            actor_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            actor_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            actor_list = paginator.page(paginator.num_pages)

    template_view = 'actor_page.html'
    return render(request, template_view, {'actor': actor_list,'len':l})

def show_movie_page(request, movie_id):
    movies=Movie.objects.all()
    movie_list = []
    for m in movies:
        movie_list.append(m)
    movie=movie_list[movie_id-1]
    actors=movie.actors.all()
    return render(request, 'movie.html', {'movie': movie, 'actors': actors})


def show_actor_page(request, actor_id):
    actor=Actor.objects.get(id=actor_id)
    movies=actor.movie_set.all()
    co_actors={}
    for m in movies:
        actors=m.actors.all()
        for a in actors:
            if a!=actor:
                if a in co_actors:
                    co_actors[a]=co_actors[a]+1
                else:
                    co_actors[a]=1
    co_actors = sorted(co_actors.items(), key=lambda x: x[1], reverse=True)
    co_actors=co_actors[:10]

    return render(request, 'actor.html', {'actor': actor, 'movies': movies,'co_actors':co_actors})



def search_target(request):
    start = datetime.now()
    if request.method != 'GET':
        raise Http404()

    key_word = request.GET.get('keyword')
    if not key_word:
        return render(request, 'search.html')
    choice=request.GET.get('choice')
    if choice=="movie":
        return search_movie(request,key_word,start)
    if choice=="actor":
        return search_actor(request, key_word, start)
    if choice=="comment":
        return search_comment(request, key_word, start)

def search(request,choice,keyword):
    start = datetime.now()
    if choice=="movie":
        return search_movie(request,keyword,start)
    if choice=="actor":
        return search_actor(request, keyword, start)
    if choice=="comment":
        return search_comment(request, keyword, start)
    return render(request, 'search.html')


def search_movie(request,key_word,start):
    movie_list=[]
    movies=Movie.objects.all()
    for m in movies:
        if m.title.find(key_word)!=-1:
            movie_list.append(m)
            continue
        for a in m.actors.all():
            if a.name.find(key_word)!=-1:
                movie_list.append(m)
                break

    l=len(movie_list)
    paginator = Paginator(movie_list, 10)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            movie_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            movie_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            movie_list = paginator.page(paginator.num_pages)
    str="choice=movie&keyword="+key_word
    params = {'movie': movie_list,
              'cost': (datetime.now() - start).total_seconds(),
              'total':l,
              'other_string':str,
              'keyword':key_word,
              'choice':"movie"}

    return render(request, 'search_movie.html', params)

def search_actor(request,key_word,start):
    actor_list=[]
    movies=Movie.objects.all()
    for m in movies:
        if m.title.find(key_word) != -1:
            for a in m.actors.all():
                actor_list.append(a)
            continue
        for a in m.actors.all():
            if a.name.find(key_word) != -1:
                actor_list.append(a)
                break
    actor_list=set(actor_list)
    actor_list=list(actor_list)
    l=len(actor_list)
    paginator = Paginator(actor_list, 10)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            actor_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            actor_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            actor_list = paginator.page(paginator.num_pages)

    str="choice=actor&keyword="+key_word
    params = {'actor': actor_list,
              'cost': (datetime.now() - start).total_seconds(),
              'total':l,
              'other_string':str,
              'keyword':key_word,
              'choice':"actor",}

    return render(request, 'search_actor.html', params)

def search_comment(request,key_word,start):
    comment_list=[]
    movies=Movie.objects.all()
    for m in movies:
        if m.comment1.find(key_word)!=-1:
            t=(m,m.comment1)
            comment_list.append(t)
            continue
        if m.comment2.find(key_word)!=-1:
            t = (m, m.comment2)
            comment_list.append(t)
            continue
        if m.comment3.find(key_word)!=-1:
            t = (m, m.comment3)
            comment_list.append(t)
            continue
        if m.comment4.find(key_word)!=-1:
            t = (m, m.comment4)
            comment_list.append(t)
            continue
        if m.comment5.find(key_word)!=-1:
            t = (m, m.comment5)
            comment_list.append(t)
            continue

    l=len(comment_list)
    paginator = Paginator(comment_list, 10)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')

        try:
            comment_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            comment_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            comment_list = paginator.page(paginator.num_pages)
    str="choice=comment&keyword="+key_word
    params = {'cost': (datetime.now() - start).total_seconds(),
              'total':l,
              'other_string':str,
              'comment':comment_list,
              'keyword':key_word,
              'choice':"comment"}

    return render(request, 'search_comment.html', params)