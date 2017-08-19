from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


from collections import defaultdict
from string import punctuation
from heapq import nlargest

import urllib.request
from bs4 import BeautifulSoup


class FrequencySummarizer:

    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut

        self._stopwords = set(stopwords.words('english') + list(punctuation))


    def _compute_frequency(self, word_sent):
        freq = defaultdict(int)
        for sentence in word_sent:
            for word in sentence:
                if word not in self._stopwords:
                    freq[word] +=1
        max_freq = float(max(freq.values())) 

        for word in freq.keys():
            freq[word] = freq[word]/max_freq

            if freq[word] >= self._max_cut or freq[word] <= self._min_cut:
                del freq[word]

        return freq

    def summarize(self, text, n):
        sents = sent_tokenize(text)
        assert n <= len(text)
        word_sent = [word_tokenize(sent.lower()) for sent in sents]

        self._freq = self._compute_frequency(word_sent)
        ranking = defaultdict(int)
        for i,sent in enumerate(word_sent):
            for word in sent:
                ranking[i] += self._freq[word]

        sents_idx = nlargest(n,ranking, key = ranking.get)
        return [sent[j] for j in sents_idx]


def get_only_text_weashington_post(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    page =  (response.read().decode('utf-8'))
    # page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page, "html.parser")
    text = ''.join(map(lambda p: p.text, soup.findAll('article')))
    soup2 = BeautifulSoup(text, "html.parser")
    text = ''.join(map(lambda p: p.text, soup2.findAll('p')))
    return soup.title.text, text

someUrl = 'https://www.washingtonpost.com/politics/trump-decides-to-get-rid-of-white-house-chief-strategist-stephen-bannon/2017/08/18/98cd5c40-8430-11e7-902a-2a9f2d808496_story.html?hpid=hp_hp-top-table-main_bannon-109pm%3Ahomepage%2Fstory&utm_term=.2803b256efc9'
textOfUrl = get_only_text_weashington_post(someUrl)
fs = FrequencySummarizer(textOfUrl[1],3)