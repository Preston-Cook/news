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
import json
from datetime import datetime


def index(request):

    # Check if user was redirected to index after logout. If so, logout user
    log_out = request.session.get('logout')

    if log_out:
        logout(request)

    saved_articles = request.user.saved_articles.all() if request.user.is_authenticated else []

    # Retrieve client IP, country, and trending articles in their country
    ip = get_client_ip(request)
    country = get_country(ip).lower()

    # If user is connected to site on localhost, country is None
    if not country:
        country = 'us'
    
    json_data = get_trending(country)
    articles = json_data['articles']

    # Initialize array for webpage context
    article_data = []

    for article in articles:

        # If API did not retrieve article content continue
        if not article['content']:
            continue

        # Find elipses and save article content
        content = article['content'][:article['content'].find('…') + 1]

        # Get urls from response
        img = article['urlToImage'] if article['urlToImage'] else 'https://s3.amazonaws.com/libapps/accounts/9189/images/newspaper.jpg'
        
        url = article['url'] if article['url'] else '#'


        # Check if article is already saved inside database
        try:
            article_from_database = Saved_Article.objects.get(
                title=article['title'],
                url=url,
                img=img,
                content=content
            )

        except Saved_Article.DoesNotExist:
            article_from_database = None

        # Parse ISO string and append article data to context array
        article_data.append((
            article['title'],
            url,
            img,
            content,
            dateutil.parser.isoparse(article['publishedAt']),
            article_from_database in saved_articles
        ))

    return render(request, 'articles/index.html', {
        'articles': articles,
        'logout': log_out,
        'country': country,
        'article_data': article_data
    })


def account(request):

    # Render account page
    if request.method == 'GET':
        return render(request, 'articles/account.html')


def login_view(request):

    # POST route for retrieving login from data from user
    if request.method == "POST":
        email = request.POST['email']

        password = request.POST['password']


        # authenticate user by comparing hash
        user = authenticate(request, email=email, password=password)

        # Login user if authentification successful else render error message
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "articles/login.html", {
                "message": "Invalid email and/or password."
            })

    return render(request, 'articles/login.html')


def register(request):

    # POST route for retrieving registration form data from user
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Check password confirmation
        if password != confirmation:
            return render(request, 'articles/register.html', {
                'message': 'Passwords Must Match.'
            })

        # Try to create user unless integrity error, then return message to user
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()

        except IntegrityError:
            return render(request, "articles/register.html", {
                "message": "There is Already an Account Associated with this Email."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "articles/register.html")


def logout_view(request):

    # Set session logout variable to true and redirect user to index route
    request.session["logout"] = True

    return HttpResponseRedirect(reverse('index'))


def account(request):
    return render(request, 'articles/account.html')


def saved(request):

    # Gather all saved articles
    saved_articles = request.user.saved_articles.all().order_by('-publication_date')

    return render(request, 'articles/saved.html', {
        'articles': saved_articles
    })


@login_required(login_url='/login')
def category(request, category):

    # Gather client IP 
    ip = get_client_ip(request)
    country = get_country(ip).lower()

    # Set country to US if no country is returned
    if not country:
        country = 'us'

    # Gather lowercased categories
    articles = get_category(country, category)

    # Gather all of user's saved articles
    saved_articles = request.user.saved_articles.all()

    # Initialize list for article data
    article_data = []


    for article in articles['articles']:

        # If API did not retrieve article content continue
        if not article['content']:
            continue

        content = article['content'][:article['content'].find('…') + 1]

        # Pull article urls
        img = article['urlToImage'] if article['urlToImage'] else 'https://s3.amazonaws.com/libapps/accounts/9189/images/newspaper.jpg'
        
        url = article['url'] if article['url'] else '#'

        # Check if article already exists inside database
        try:
            article_from_database = Saved_Article.objects.get(
                title=article['title'],
                url=url,
                img=img
            )
            print('I found it inside the database!')

        except Saved_Article.DoesNotExist:
            article_from_database = None

        # Append article data to list
        article_data.append((
            article['title'],
            url,
            img,
            content,
            dateutil.parser.isoparse(article['publishedAt']),
            article_from_database in saved_articles
        ))

    # Render categories.html with context
    return render(request, 'articles/categories.html', {
        "category": category,
        "article_data": article_data
    })


@login_required(login_url='/login')
def search(request):

    # Pull parameter from URL
    query = request.GET['q']

    # Check if lowered query is a category. If so, redirect
    if query.lower() in categories:
        return HttpResponseRedirect(f'/category/{query.lower()}')
    else:
        articles = get_everything(query)

    # Collect all of user's saved articles
    saved_articles = request.user.saved_articles.all()

    # Initialize article list
    article_data = []

    # Loop through articles and extract data
    for article in articles['articles']:

        # If API did not retrieve article content continue
        if not article['content']:
            continue

        content = article['content'][:article['content'].find('…') + 1]

        # Pull urls from articles
        img = article['urlToImage'] if article['urlToImage'] else 'https://s3.amazonaws.com/libapps/accounts/9189/images/newspaper.jpg'
        
        url = article['url'] if article['url'] else '#'

        # Try to locate article within database
        try:
            article_from_database = Saved_Article.objects.get(
                title=article['title'],
                url=url,
                img=img
            )

        except Saved_Article.DoesNotExist:
            article_from_database = None

        # Append article data to data list
        article_data.append((
            article['title'],
            url,
            img,
            content,
            dateutil.parser.isoparse(article['publishedAt']),
            article_from_database in saved_articles
        ))

    # Render search.html with proper context
    return render(request, 'articles/search.html', {
        "query": query,
        "article_data": article_data
    })


@csrf_exempt
@login_required(login_url='/login')
def save_post(request):

    if request.method == 'PUT':

        # Parse JSON response and retrieve data
        res = json.loads(request.body)

        title = res['title']
        content = res['content']
        url = res['url']
        img = res['img']
        publication_date = res['publication_date']

        # Slice publication date and convert into datetime object
        publication_date = publication_date[6:].upper().replace(
            '.', '').replace('NOON', '12:00')

        publication_date = datetime.strptime(
            publication_date, '%b %d, %Y, %I:%M %p')

        try:
            # Check if article exists inside the database
            saved_article = Saved_Article.objects.get(
                title=title,
                content=content,
                url=url, img=img,
                publication_date=publication_date)

        except Saved_Article.DoesNotExist:

            # Create new article object
            Saved_Article.objects.create(
                title=title,
                content=content,
                url=url,
                img=img,
                publication_date=publication_date).save()

            # Retrieve newly-created objects
            saved_article = Saved_Article.objects.get(
                title=title,
                content=content,
                url=url, img=img,
                publication_date=publication_date)

        # Add user_id and saved_article to linking table
        request.user.saved_articles.add(saved_article)

        return HttpResponse(status=204)

    return JsonResponse({"error": "PUT request required"}, status=400)


@csrf_exempt
@login_required(login_url='/login')
def delete_post(request):
    if request.method == 'PUT':

        # Parse JSON response and retrieve data
        res = json.loads(request.body)

        title = res['title']
        content = res['content']
        url = res['url']
        img = res['img']
        publication_date = res['publication_date']

        # Slice publication date and convert into datetime object
        publication_date = publication_date[6:].upper().replace(
            '.', '').replace('NOON', '12:00').replace('1 PM', '1:00 PM')

        publication_date = datetime.strptime(
            publication_date, '%b %d, %Y, %I:%M %p')

        try:
            # Check if article exists inside the database
            saved_article = Saved_Article.objects.get(
                title=title,
                content=content,
                url=url, img=img,
                publication_date=publication_date)

        except Saved_Article.DoesNotExist:

            # Create new article object
            return JsonResponse({"error": "PUT request required"}, status=400)

        # Add user_id and saved_article to linking table
        request.user.saved_articles.remove(saved_article)
        saved_article.delete()

        return HttpResponse(status=204)

    # Return error if not PUT request
    return JsonResponse({"error": "PUT request required"}, status=400)