from django.db import models
from django.db import connection, connections
import json


def ValidateLogin(user,password):
    if(user == 'admin' and password == '1234'):
        return True
    else:
        return False


class TwitterData(models.Model):
    text = models.TextField(max_length=5000, null=False, blank=False)
    source = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.source


class TwitterDataRead(models.Model):
    tweet = models.ForeignKey(TwitterData, on_delete=models.CASCADE)
    flag = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.tweet.source


class NewsData(models.Model):
    text = models.TextField(max_length=5000, null=False, blank=False)
    source = models.TextField(max_length=500, null=False, blank=False)


class NewsDataRead(models.Model):
    news = models.ForeignKey(NewsData, on_delete=models.CASCADE)
    flag = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.news.source


class StockData(models.Model):
    symbol = models.TextField(max_length=5000, null=False, blank=False)
    datetime = models.TextField(max_length=5000, null=False, blank=False)
    dimension = models.TextField(max_length=500, null=False, blank=False)

