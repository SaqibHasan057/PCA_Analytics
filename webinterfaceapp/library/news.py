import requests
from webinterfaceapp.models import NewsData, NewsDataRead


class NewsApi:

    def api_access(self, url):
        response = requests.get(url)
        result = response.json()
        return result

    def get_news(self):
        # Your API key is: CVLWNI4QL796D3PJ
        key = "699cbf8e77c14f199b5383b78e3784e1"
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=699cbf8e77c14f199b5383b78e3784e1"
        result = self.api_access(url)
        count = result["totalResults"]
        articles = result["articles"]
        print(result["totalResults"])

        for article in articles:
            text = article['title']
            source = article['url']
            news = NewsData(text=text, source=source)
            news.save()
            news_data = NewsDataRead(news=news, flag=False)
            news_data.save()

        return count




