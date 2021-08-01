from django.urls import path

from webinterfaceapp.views import views

app_name = 'webinterfaceapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.registration, name='register'),
    path('pca/', views.pca, name='pca'),
    path('twitter_analysis/', views.twitter, name='twitter_analysis'),
    path('twitter/', views.twitter_response, name='twitter'),
    path('news_analysis/', views.news, name='news_analysis'),
    path('news/', views.news_response, name='news'),
    path('stock_analysis/', views.stock, name='stock_analysis'),
    path('stock/', views.stock_response, name='stock'),
    path('stop/', views.stop_processing, name='stop'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('twitter_analytics/', views.twitter_analytics, name='twitter_analytics'),
    path('news_analytics/', views.news_analytics, name='news_analytics'),
    path('stock_analytics/', views.stock_analytics, name='stock_analytics'),
    path('facebook_analysis/', views.facebook, name='facebook_analysis'),
    path('facebook_analytics/', views.facebook_analytics, name='facebook_analytics'),
    path('google_search_trend/', views.google_search_trend, name='google_search_trend'),
    path('google_search/', views.google_search, name='google_search')
]

