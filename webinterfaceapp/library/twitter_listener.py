from sqlalchemy import create_engine
from tweepy import StreamListener
import json, time, sys
from webinterfaceapp.models import TwitterData, TwitterDataRead
from webinterfaceapp.library.text_cleaner import TweetCleaner
from text_cleaner import keep
from text_cleaner.processor.common import ASCII
from text_cleaner.processor.misc import URL
import re
import json

'''OAuth Authentication'''
consumer_key = 'IVSop90ELns94Qw5VxADmKYpK'
consumer_secret = 'WrOELrh2N9IU14APZNgNGbRfxyjIyJFght6GG3GZmZsbAYdu5a'
access_token = '829226041386336257-28HGNC8sLOnygG2Bzjq0RXzda23DoUt'
access_token_secret = '9qgGNNbul7tULzlPBUkK3npMNQVPZVPPMbW8vFShmmxzx'


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer', time_limit=5):
        self.start_time = time.time()
        self.limit = time_limit
        self.api = api 
        self.counter = 0
        self.fprefix = fprefix
        # self.output  = open(fprefix + '.'
        #                     + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')
        self.engine = create_engine('postgresql://postgres:rot@localhost:5432/interface')
        self.tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)

    def on_data(self, data):
        if (time.time() - self.start_time) > self.limit:
            # self.output.close()
            return False
        if 'in_reply_to_status' in data:
            self.on_status(data)

        if 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print(warning['message'])
            return False

    def on_status(self, status):
        # self.output.write(status + "\n")
        result = json.loads(status)
        status_text = result["text"]
        # print(status_text)
        text = self.tc.get_cleaned_text(status_text)
        print(text)

        source = result["source"]
        # print(source)

        tweet = TwitterData(text=text, source=source)
        tweet.save()
        tweet_data = TwitterDataRead(tweet=tweet, flag=False)
        tweet_data.save()

        # TwitterData.objects.create(text=status_text, source=source)

        self.counter += 1
        print(self.counter)
        return

    def on_delete(self, status_id, user_id):
        # self.delout.write( str(status_id) + "\n")
        print( str(status_id) + "\n")
        return

    def on_limit(self, track):
        # sys.stderr.write(track + "\n")
        print(track + "\n")
        return

    def on_error(self, status_code):
        # sys.stderr.write('Error: ' + str(status_code) + "\n")
        print('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        # time.sleep(60)
        return

    def CleanText(self, text):
        result = text
        try:
            result = keep(
                text,
                [ASCII],
            )
            result = URL.remove(result)

            expression = '(\#[a-zA-Z0-9]+)|(\@[A-Za-z0-9]+)|\$(\w+)|([#@$"|])|([0-9]+)'

            result = ' '.join(re.sub(expression, " ", result).split())
        except:
            print("andsnn")
        return result