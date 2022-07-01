
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import createpostform

from .models import User,Post


def get_previous_url(page_posts):

    if page_posts.has_previous():
        previous_url = f'?page={page_posts.previous_page_number()}'
    else:
        previous_url = ''
    return previous_url


def get_next_url(page_posts):
    if page_posts.has_next():
        next_url = f'?page={page_posts.next_page_number()}'
    else:
        next_url = ''
    return next_url


def index(request):
    post = Post.objects.all()
    paginator = Paginator(post , 10)
    p_num = request.GET.get('page')
    page_posts = paginator.get_page(p_num)
    return render(request, "network/index.html", context={
        'form': createpostform(),
        'page_posts':page_posts,
        'prev_url': get_previous_url(page_posts),
        'next_url': get_next_url(page_posts)
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method != 'POST':
        return JsonResponse({"error": 'required' } , status = 400)
    
    form = createpostform(request.POST)

    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')


def profile(request,id):

    profile_user = User.objects.get(pk = id )

    posts_profile = Post.objects.filter(author = id)
    paginator = Paginator(posts_profile ,10)
    p_num = request.GET.get('page')
    page_posts = paginator.get_page(p_num)

    if request.user.is_authenticated:
        follow = profile_user.followers.filter(id = request.user.id).exists()
    else:
        follow = False
    
    return render(request,'network/profile.html', context={
        'user_profile': profile_user,
        'following': follow,
        'followingcount': profile_user.follow.all().count(),
        'followerscount': profile_user.followers.all().count(),
        'page_posts': page_posts,
        'prev_url': get_previous_url(page_posts),
        'next_url': get_next_url(page_posts),


    })

@login_required
def follow_user(request,to_user):
    if request.method != 'POST':
        return JsonResponse({'error': 'post is manditory'} , status = 400)

    User.objects.get(pk = request.user.id).follow.add(to_user)
    return HttpResponseRedirect(reverse("profile" , args = (to_user,)))

@login_required
def unfollow_user(request,from_user):
    if request.method != 'POST':
        return JsonResponse({"error":'post required'}, status=400)

    User.objects.get(pk = request.user.id).follow.remove(from_user)
    return HttpResponseRedirect(reverse("profile" , args = (from_user,)))

def following(request):
    following = User.objects.get(pk = request.user.id).follow.all()
    follow_id = following.values_list('pk' ,flat = True)
    follow_post = Post.objects.filter(author__in = follow_id)

    paginator = Paginator(follow_post,10)

    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)

    return render(request,'network/following.html' ,  context={
        'page_posts':posts,
        'posts': follow_post,
        'prev_url': get_previous_url(posts),
        'next_url': get_next_url(posts),

    })


@csrf_exempt
@login_required
def like_update(request,post_id):
    user = request.user 
    try:
        post = Post.objects.get(pk = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": 'doesnt exist post'} , ststus = 404)
    if (user.user_likes.filter(pk =post_id).exists()):
        post.like.remove(user)
        postlike = False
    else:
        post.like.add(user)
        postlike =True
    likes = post.likes()
    return JsonResponse({'postlike':postlike , 'countlike':likes}, status = 200)









@csrf_exempt
@login_required
def edit_post(request,post_id):
   if request.method != 'POST':
      return JsonResponse({'error': 'post is required'} , status = 400)
   try:
        post = Post.objects.get(pk = post_id)
   except Post.DoesNotExist:
        return JsonResponse({'error':' not found '}, status = 404)
   if request.user == post.author:
       body_unicode = request.body.decode('utf-8')
       body = json.loads(body_unicode)
       desc = body['desc']

       Post.objects.filter(pk = post_id).update(desc = f'{desc}')
       return JsonResponse({'message':"post updated success", 'desc': desc} , status = 200)

   else:
         return JsonResponse({'error':'need premision'}, status = 400)