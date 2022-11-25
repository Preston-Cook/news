import requests
import os
import sys
from newsapi import NewsApiClient
import datetime

categories = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]


os.environ['API_KEY'] = '' # <-- Insert API Key here

def get_trending(country):

    NEWS_API_KEY = os.environ.get('API_KEY')

    newsapi = NewsApiClient(NEWS_API_KEY)

    if not country:
        country = 'us'

    try:
        top_headlines = newsapi.get_top_headlines(language='en', country='us')

    except Exception as e:
        print(e)
        sys.exit(1)

    return top_headlines


def get_category(country, category):

    NEWS_API_KEY = os.environ.get('API_KEY')

    newsapi = NewsApiClient(NEWS_API_KEY)

    try:
        stories = newsapi.get_top_headlines(language='en',
                                            country=country, category=category.lower())

    except Exception as e:
        print(e)
        sys.exit(1)

    return stories


def get_everything(query):

    date = (datetime.datetime.today() -
            datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    NEWS_API_KEY = os.environ.get('API_KEY')

    newsapi = NewsApiClient(NEWS_API_KEY)

    try:
        stories = newsapi.get_everything(
            q=query,
            from_param=date,
            language='en',
            sort_by='relevancy'
        )

    except Exception as e:
        print(e)
        sys.exit(1)

    return stories


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_country(ip):
    
    try:
        res = requests.get(f'https://ipinfo.io/{ip}')
        res.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)

    json_data = res.json()

    return json_data.get('country')
