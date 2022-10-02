from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import User, Saved_Article
from .utils import *
import dateutil.parser
from django.core.paginator import Paginator
import json
from django.db import IntegrityError
from datetime import datetime

# Create your views here.
def index(request):

    if request.method == 'POST':
        pass
    
    log_out = request.session.get('logout')
    
    if log_out:
        logout(request)

    ip = get_client_ip(request)

    country = get_country(ip)

    json_data = get_trending(country)
    
    articles = json_data['articles']

    article_data = []

    for article in articles:
        img = article['urlToImage'] if article['urlToImage'] else 'https://s3.amazonaws.com/libapps/accounts/9189/images/newspaper.jpg'
        content = article['content'][:article['content'].find('…') + 1] if article['content'] else ''
        url = article['url'] if article['url'] else '#'

        article_data.append((
            article['title'],
            url,
            img,
            content,
            dateutil.parser.isoparse(article['publishedAt'])
        ))

    return render(request, 'articles/index.html', {
        'articles': articles,
        'logout': log_out,
        'article_data': article_data
    })


def account(request):
    return render(request, 'articles/account.html')


def login_view(request):
    
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        password = request.POST['password']
    
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "articles/login.html", {
                    "message": "Invalid email and/or password."
                })
    
    return render(request, 'articles/login.html')




def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render(request, 'articles/register.html', {
                'message': 'Passwords Must Match.'
            })
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        
        except IntegrityError:
            return render(request, "articles/register.html", {
                    "message": "There is already an Account Associated with this Email."
                })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "articles/register.html")


def logout_view(request):
    
    request.session["logout"] = True
    
    return HttpResponseRedirect(reverse('index'))


def account(request):
    return render(request, 'articles/account.html')



@login_required(login_url='/login')
def search(request):

    query = request.GET['q']

    ip = get_client_ip(request)

    country = get_country(ip)
    
    if query.lower() in categories:
        articles = get_category(country, query)
    
    else:
        articles = get_everything(query)
    
    article_data = []

    for article in articles['articles']:
        img = article['urlToImage'] if article['urlToImage'] else 'https://s3.amazonaws.com/libapps/accounts/9189/images/newspaper.jpg'
        content = article['content'][:article['content'].find('…') + 1] if article['content'] else ''
        url = article['url'] if article['url'] else '#'

        article_data.append((
            article['title'],
            url,
            img,
            content,
            dateutil.parser.isoparse(article['publishedAt'])
        ))

    return render(request, 'articles/search.html', {
        "query": query,
        "article_data": article_data
    })

@csrf_exempt
@login_required(login_url='/login')
def save_post(request):

    # if request.method == "PUT":
    #     try:
    #         user = User.objects.get(username=username)
        
    #     except User.DoesNotExist:
    #         return JsonResponse({'error': "Post not found"}, status=404)
        
    #     follow_bool = json.loads(request.body).get("follow")
        
    #     if follow_bool:
    #         UserFollowing.objects.create(user_id=request.user, following_user_id=user).save()
    #     else:
    #         UserFollowing.objects.get(user_id=request.user, following_user_id=user).delete()

    #     return HttpResponse(status=204)
    
    # return JsonResponse({"error": "PUT request required"}, status=400)

    if request.method == 'PUT':

        res = json.loads(request.body)

        title = res['title']
        content = res['content']
        url = res['url']
        img = res['url']
        # publication_date = datetime.strptime(res['publication_date'].replace('.',''), 
        # '%b -%d, %Y, -%I:%M %p')

        # print(publication_date)


        # Check if post already exists
        # article = Saved_Article.objects.get(
        #     title=title,
        #     content=content,
        #     url=url,
        #     img=img,
        #     publication_date=publication_date
        # )

        # Save post to database if not exists
        # if not article:
        #     article = Saved_Article.objects.get(
        #     title=title,
        #     content=content,
        #     url=url,
        #     img=img,
        #     publication_date=publication_date
        # ).save()

        return HttpResponse(status=204)

    return JsonResponse({"error": "PUT request required"}, status=400)
    

