from django.shortcuts import render
import tweepy

from webinterfaceapp.models import (
    TwitterData, TwitterDataRead,
    NewsData, NewsDataRead,
    StockData)
from webinterfaceapp.library import twitter_listener
from django.http import JsonResponse

from webinterfaceapp.library.pca_text import PcaRealTime
from webinterfaceapp.library.news import NewsApi
from webinterfaceapp.library.stock import StockMarketApi
import random
from django.http import HttpResponseRedirect

consumer_key = 'IVSop90ELns94Qw5VxADmKYpK'
consumer_secret = 'WrOELrh2N9IU14APZNgNGbRfxyjIyJFght6GG3GZmZsbAYdu5a'
access_token = '829226041386336257-28HGNC8sLOnygG2Bzjq0RXzda23DoUt'
access_token_secret = '9qgGNNbul7tULzlPBUkK3npMNQVPZVPPMbW8vFShmmxzx'
stream = ''

block_size = 15
ouput_dimension = 10

def ValidateLogin(user,password):
    if(user == 'admin' and password == '1234'):
        return True
    else:
        return False


def login(request):
    #If logged in, redirect him to home page
    if 'userid' in request.session and request.session['userid'] is not None:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        if ValidateLogin(userid, password):
            request.session['userid'] = userid
            request.session['password'] = password
            return HttpResponseRedirect('/')
        else:
            return render(request, 'webinterfaceapp/login.html',{'message': 'Login Failed. Please contact system administrator.'})
    return render(request, 'webinterfaceapp/login.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')

def registration(request):
    if request.method == 'POST':
        context = {}
        context['result'] = []
        return render(request, 'webinterfaceapp/home.html', context)
        # userid = request.POST.get('userid')
        # password = request.POST.get('password')
        # if ValidateLogin(userid, password):
        #     request.session['userid'] = userid
        #     request.session['password'] = password
        #     return HttpResponseRedirect('/')
        # else:
        #     return render(request, 'webinterfaceapp/login.html',{'message': 'Login Failed. Please contact system administrator.'})
    return render(request, 'webinterfaceapp/register.html')

def home(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/home.html', context)

def about_us(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/about_us.html', context)

def contact_us(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/contact_us.html', context)

def pca(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/pca_analysis.html', context)

def twitter(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/twitter_analysis.html', context)

def news(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/news_analysis.html', context)

def stock(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/stock_analysis.html', context)

def facebook(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/facebook_analysis.html', context)

def twitter_analytics(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/twitter_analytics.html', context)

def news_analytics(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/news_analytics.html', context)

def stock_analytics(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/stock_analytics.html', context)

def facebook_analytics(request):
    context = {}
    context['result'] = []
    return render(request, 'webinterfaceapp/facebook_analytics.html', context)

def google_search_trend(request):
    context = {}
    if request.method == 'POST':
        value = request.POST.get('google-text')
        context['result'] = value
    else:
        context['result'] = 'bangla'
    return render(request, 'webinterfaceapp/google_search.html', context)

def google_search(request):
    data = {
        'status': True
    }

    return JsonResponse(data, safe=False)

def twitter_response(request):
    key = request.GET.get('key')
    print(key)

    tw = TwitterData.objects.all()
    tw_len = len(list(tw))
    print("twitter data")
    print(tw_len)
    if tw_len <= 100:
        global stream
        auth = ''
        api = ''
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
        except:
            print("Error: Authentication Failed Here.")

        listen = twitter_listener.SListener(api, 'myprefix', time_limit=5)
        stream = tweepy.Stream(auth, listen)

        try:
            if key:
                stream.filter(track = key)
            else:
                stream.sample(languages = ["en"])

        except:
            print("error!")
            stream.disconnect()
    print(key)
    tweets = TwitterData.objects.filter(twitterdataread__flag=False)
    t_length = len(list(tweets))
    if t_length == 0:
        tweets = TwitterData.objects.filter(twitterdataread__flag=True)
    # tweets = TwitterData.objects.all()

    tweet_text = list(tweets.values_list('text', flat=True))

    print(len(tweet_text))
    if len(tweet_text) > 40:
        tweet_text = random.sample(tweet_text, 40)
        # print("tweets")
    print(len(tweet_text))
    # tweet_text = random.sample(tweet_text,40)     #should be removed from comment
    twitter_data_update_list = tweets.values_list('id', flat=True)
    TwitterDataRead.objects.filter(tweet_id__in=twitter_data_update_list).update(flag=True)


    try:
        max_value_of_each_eigenvector, index_of_max_value, words, frequency, word_list = pca_text_calculation(tweet_text)
        data = {
            'status': True,
            'words': words,
            # 'frequency': frequency
            'word_list':word_list
        }

        print(data)


    except:
        data = {
            'status': False
        }

    return JsonResponse(data, safe=False)


def stop_processing(request):
    source = request.GET.get('source', None)
    data = {}
    if source == 'twitter':
        global stream
        try:
            stream.disconnect()
            data['status'] = True
        except:
            data['status'] = False

    return JsonResponse(data, safe=False)


def news_response(request):
    news = NewsData.objects.all()
    if len(list(news)) < 100:
        count = NewsApi().get_news()
        news = NewsData.objects.all()

    # news = NewsData.objects.filter(newsdataread__flag=False)
    # news = NewsData.objects.all()
    news_text = list(news.values_list('text', flat=True))
    # print("News")
    # print(len(news_text))

    if len(list(news_text)) > 40:
        news_text = random.sample(news_text,40)
    news_data_update_list = news.values_list('id', flat=True)
    NewsDataRead.objects.filter(news_id__in=news_data_update_list).update(flag=True)


    try:
        max_value_of_each_eigenvector, index_of_max_value, words, frequency,word_list = pca_text_calculation(news_text)

        data = {
            'status': True,
            'words': words,
            'word_list':word_list
        }

        print(data)


    except:
        data = {
            'status': False
        }

    return JsonResponse(data, safe=False)


def pca_text_calculation(data):
    pcaRealTime = PcaRealTime()
    dictionary,input_matrix,frequency_per_word = pcaRealTime.convert_text_to_vector(data)
    output_matrix, eigen_vectors, eigen_values = pcaRealTime.robust_real_time_PCA_target_dimension(input_matrix,block_size,ouput_dimension)
    max_value_of_each_eigenvector, index_of_max_value, words, frequency,word_list = pcaRealTime.maximum_from_eigen_vector(eigen_vectors,dictionary, frequency_per_word)

    return max_value_of_each_eigenvector, index_of_max_value, words, frequency,word_list


def stock_response(request):
    key = request.GET.get('key')
    # print(key)
    if not key:
        key = "MSFT"

    stocks = StockData.objects.filter(symbol=key)

    print("stock data")
    print(len(list(stocks)))

    stocks = StockData.objects.filter(symbol=key).order_by('-id')[:10]

    print("stock data")
    print(len(list(stocks)))

    if len(list(stocks)) < 10:
        count = StockMarketApi().get_stock_data(key)
        stocks = StockData.objects.filter(symbol=key).order_by('-id')[:10]

    datetime = []
    dimension = []

    for stock in stocks.values():
        datetime.append(stock['datetime'])
        dimension.append(stock['dimension'])


    data = {
        'status': True,
        'datetime': datetime,
        'dim': dimension
    }

    print(data)

    return JsonResponse(data, safe=False)
