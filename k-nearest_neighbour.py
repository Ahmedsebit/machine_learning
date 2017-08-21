import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from math import log
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import urllib
from urllib.request import Request, urlopen

def getWashPostText(url,token):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        page =  (response.read().decode('utf-8'))
    except:
        return (None, None)
    soup = BeautifulSoup(page)

    if soup is None:
        return None

    text = " "

    if soup.findAll(token) is not None:
        text = ''.join(map(lambda p: p.text, soup.findAll(token)))
        soup2 = BeautifulSoup(text)
        if soup2.findAll('p') is not None:
            text = ''.join(map(lambda p: p.text, soup2.findAll('p')))

    return text, soup.title.text

def getNYTText(url,token):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content)
    page = str(soup)
    title = soup.find('title').text
    mydivs = soup.findAll("p", {"class":"story-body-text story-content"})
    text = ''.join(map(lambda p: p.text, mydivs))
    return text, title

    if soup.findAll(token) is not None:
        text = ''.join(map(lambda p: p.text, soup.findAll(token)))
        soup2 = BeautifulSoup(text)
        if soup2.findAll('p') is not None:
            text = ''.join(map(lambda p: p.text, soup2.findAll('p')))

    return text, soup.title.text

def scrapeSource(url, magicFrag='2015', scrapeFunction=getNYTText, token='None'):

    urlbodies = {}
    webpage = urlopen(url).read()
    soup = BeautifulSoup(webpage)

    numErrors = 0
    for a in soup.findAll('a'):
        try:
            url = a['href']
            if ((url not in urlbodies) and (magicFrag is not None and magicFrag in url or magicFrag is None)):
                body = scrapeFunction(url, token)
                if body and len(body)>0:
                    urlbodies[url] = body
        except:
            numErrors +=1

class FrequencySummarizer:

    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut

        self._stopwords = set(stopwords.words('english') + list(punctuation) + [u"'s", "'"])

    def _compute_frequency(self, word_sent, customStopWords=None):
        freq = defaultdict(int)
        if customStopWords is None:
            stopwords = set(self._stopwords)
        else:
            stopwords = set(customStopWords).union(self._stopwords)
        for sentence in word_sent:
            for word in sentence:
                if word not in stopwords:
                    freq[word] +=1
        m = float(max(freq.values()))
        for word in freq.keys():
            freq[word] = freq[word]/m

        if freq[word] >= self._max_cut or freq[word]<= self._min_cut:
            del freq[word]

        return freq

    def exctract_features(self, article, n, customStopWords=None):
        text = article[0]
        title = article[1]
        sentences = sent_tokenize(text)
        word_sent = [word_tokenize(sentence.lower()) for sentence in sentences]
        self._freq = self._compute_frequency(word_sent, customStopWords)
        if n < 0:
            return nlargest(len(self._freq.keys()), self._freq, key=self._freq.get)
        else:
            return nlargest(n,self._freq,key=self._freq.get)


    def exctractRawFrequencies(self,article):
        text = article[0]
        title = article[1]

        sentences = sent_tokenize(text)
        word_sent = [word_tokenize(sentence.lower() for sentence in sentences)]
        freq = defaultdict(int)

        for sentence in word_sent:
            for word in sentence:
                if word not in self._stopwords:
                    freq[word] += 1

        return freq

    def summarize(self, article,n):
        text = article[0]
        title = article[1]

        sentences = sent_tokenize(text)
        word_sent = [word_tokenize(sentence.lower() for sentence in sentences)]
        self._freq = self._compute_frequency(word_sent)
        ranking = defaultdict(int)

        for i,sentence in enumerate(word_sent):
            for word in sentence:
                if word in self._freq:
                    ranking[i] += self._freq[word]

        sentences_index = nlargest(n,ranking,key=ranking.get)
        return [sentences[sentence] for sentence in sentences_index]

urlWashingtonPostNonTech = "https://www.washingtonpost.com/sports"
urlNewYorkTimesNonTech = "https://www.nytimes.com/pages/sports/index.html"
urlWashingtonPostTech = "https://www.washingtonpost.com/business/technology"
urlNewYorkTimesTech = "http://www.nytimes.com/pages/technology/index.html"

washingtonPostTechArticles = scrapeSource(urlWashingtonPostTech,
                                          '2016',
                                         getWashPostText,
                                         'article') 
washingtonPostNonTechArticles = scrapeSource(urlWashingtonPostNonTech,
                                          '2016',
                                         getWashPostText,
                                         'article')
                
                
newYorkTimesTechArticles = scrapeSource(urlNewYorkTimesTech,
                                       '2016',
                                       getNYTText,
                                       None)
newYorkTimesNonTechArticles = scrapeSource(urlNewYorkTimesNonTech,
                                       '2016',
                                       getNYTText,
                                       None)

articleSummary = {}
for techurlDictionary in [washingtonPostTechArticles, newYorkTimesTechArticles]:
    for articleUrl in techurlDictionary:
        if len(techurlDictionary(articleUrl)[0]) > 0:
            fs = FrequencySummarizer()
            summary = fs.exctract_features(techurlDictionary[articleUrl], 25)
            articleSummary[articleUrl] = {'feature vector': summary, 'lable':'Tech'}  

for techurlDictionary in [washingtonPostNonTechArticles, newYorkTimesNonTechArticles]:
    for articleUrl in nontechurlDictionary:
        if len(nontechurlDictionary(articleUrl)[0]) > 0:
            fs = FrequencySummarizer()
            summary = fs.exctract_features(nontechurlDictionary[articleUrl], 25)
            articleSummary[articleUrl] = {'feature vector': summary, 'lable':'Non Tech'}  

def getDoxyDonkeyText(textUrl, token):
    response = response.get(url)
    soup = BeautifulSoup(response.content)
    title = soup.find('title').text
    mydivs = soup.findAll('divs', {'class':token})
    text = ''.join(map(lambda p:p.text, mydivs))
    return text, title

testUrl = "http://doxydonkey.blogpost.in"

testArtice = getDoxyDonkeyText(testUrl, "post-body")

fs = FrequencySummarizer()

testArticleSummary = fs.exctract_features(testArtice, 25)

similarities = {}

# for articleSummary in articleSummary:
#     oneArticleSummary = articleSummary[articleSummary]['feature vector']
#     similarities[articleUrl] = len(set(testArticleSummary)).intersection(set(oneArticleSummary))

# lables = defaultdict(int)
# knn = nlargest(5, similarities, key=similarities.get)

# for oneneighbour in knn:
#     lables[articleSummary[oneneighbour]['lable']] +=1

# nlargest(1, lables, key=lables.get)

cummulativeRawFrequency = {'Tech':defaultdict(int),'Non Tech':defaultdict(int)}
trainingData = {'Tech':newYorkTimesTechArticles, 'Non Tech':newYorkTimesNonTechArticles}
for lable in trainingData:
    for articleUrl in trainingData[lable]:
        if len(trainingData[lable][articleUrl])>0:
            fs =FrequencySummarizer()
            rawFrequency = fs.exctractRawFrequencies(trainingData[lable][articleUrl])
            for word in rawFrequency:
                cummulativeRawFrequency[lable][word] += rawFrequency[word]

techinese = 1.0
nontechinese = 1.0

for word in testArtice:
    if word in cummulativeRawFrequency[tech]:
        techinese *= 1e3*cummulativeRawFrequency['Tech'][word]/float(sum(cummulativeRawFrequency['Tech'].values()))
    else:
        nontechinese /= 1e3
    if word in cummulativeRawFrequency[nontech]:
        nontechinese *= 1e3*cummulativeRawFrequency['Non Tech'][word]/float(sum(cummulativeRawFrequency['Non Tech'].values()))
    else:
        techinese /= 1e3

techinese *= float(sum(cummulativeRawFrequency['Tech'].values())) / (float(sum(cummulativeRawFrequency['Tech'].values()))) + (float(sum(cummulativeRawFrequency['Non Tech'].values())))
nontechinese *= float(sum(cummulativeRawFrequency['Non Tech'].values())) / (float(sum(cummulativeRawFrequency['Non Tech'].values()))) + (float(sum(cummulativeRawFrequency['Tech'].values())))

if techinese > nontechinese:
    lable = 'Tech'
else:
    lable = 'Non Tech'
print lable, techinese, nontechinese