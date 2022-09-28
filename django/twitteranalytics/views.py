from ast import keyword
from glob import glob
from urllib import request
from django.shortcuts import render
import MeCab
import tweepy
import re
from wordcloud import WordCloud
from django.views import View
from django.views.generic import TemplateView
import base64
from PIL import Image
from io import BytesIO
import csv
from collections import Counter
import matplotlib.cm as cm
import matplotlib.colors as mcolors



# Create your views here.

class IndexView(TemplateView):
    template_name = 'src/index.html'

    consumer_key = 'Iebp6upiZxRCxSLRcQKIFWos6'
    consumer_secret = 'ODjiu86H0TZUOMhVMgz9mg9sSBHcckMQngyRn1SuWjK0pjYhgl'
    access_token = 'gXWIkQaklDqU6GqL8X9Iw3nYnCO1z8H6sFXQlU9iiI8sP'
    access_token_secret = 'gXWIkQaklDqU6GqL8X9Iw3nYnCO1z8H6sFXQlU9iiI8sP'
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAAgWhAEAAAAAKsZhYvmcNSiZQQIRUNCJzfpdtAQ%3DrZWic2NLOYtYA7VFwXl7wvMgUdc5yDbSKqnU1fI09gCUWi69me"
    client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

    # ポストリクエスト
    def post(self, request, *args, **kwargs):
        wordcloud,res, cnt,exe=self.wordcloud(request)
        negativeper=res['n']/cnt
        pojitiveper=res['p']/cnt
        context={
            'wordcloud':wordcloud,
            'negative':res['n'],
            'positive':res['p'],
            'natural':res['e'],
            'exeption':exe,
            'negativeper':negativeper,
            'pojitiveper':pojitiveper
        }
        return  render(request, self.template_name, context)

    # twitterの上位100件を取得
    def tweet_list(self,request):
        search=request.POST.get('search')
        searchlist=[]
        tweet_max = 100
        tweets = self.client.search_recent_tweets(query = search, max_results = tweet_max)

        for tweet in tweets.data:
            text = re.sub(r'\n', '', tweet.text)
            searchlist.append(text)
        return searchlist

    # 形態素分解
    def morphological_analysis(self, request):
        searchlist=self.tweet_list(request)
        mecab = MeCab.Tagger()
        feature="名詞"
        lis=[]
        
        for cnt in range(len(searchlist)):
            node=mecab.parseToNode(searchlist[cnt])

            while node:
                if feature == node.feature.split(",")[0]:
                    if len(node.surface)>1:
                        lis.append(node.surface)
                node = node.next

        words_count = Counter(lis)
        result = words_count.most_common()
        dic_result = dict(result)

        return  dic_result


    # wordcloud画像生成
    def wordcloud(self, request):
        res, cnt, np_word_dic, dic_result=self.negapoji(request)
        global exe
        exe=0
        # 文字ごとに色を返す関数
        def pos_color_func(word,**kwargs):
            global exe
            cmap = cm.get_cmap("tab20")
            negapoji=np_word_dic[word]
            if negapoji=='n':
                color_index=0
            elif negapoji=='p':
                color_index=6
            elif negapoji=='e':
                color_index=14
            else:
                exe+=1
                color_index=8
    
            rgb = cmap(color_index)
            return mcolors.rgb2hex(rgb)

        # FONT_PATH = "../sys/fonts-japanese-gothic.ttf"
        FONT_PATH="/etc/sys/fonts/fonts-japanese-gothic.ttf"
        wordcloud = WordCloud(font_path=FONT_PATH,width=700, height=400,background_color='white', color_func = pos_color_func).fit_words(dic_result).to_image()
        buffer = BytesIO() 
        wordcloud.save(buffer, format="PNG") 

        base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")

        return base64Img,res, cnt, exe

    # ネガポジ判定
    def negapoji(self, request):
        np_dic = {}
        np_word_dic={}
        dic_result=self.morphological_analysis(request)
        fp = open("sys/pn.csv", "rt", encoding="utf-8")
        reader = csv.reader(fp, delimiter='\t')
        for row in reader:
            name = row[0]
            result = row[1]
            np_dic[name] = result


        res = {"p":0, "n":0, "e":0}
        for analytics_word in dic_result.keys():
            if analytics_word in np_dic:
                r = np_dic[analytics_word]
                if analytics_word not in np_word_dic:
                    np_word_dic[analytics_word]=r
                if r in res:
                    res[r] += 1
            else:
                res['e']+=1
                np_word_dic[analytics_word]='e'

        cnt = res["p"] + res["n"] + res["e"]

        return res, cnt, np_word_dic, dic_result


