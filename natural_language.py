import nltk

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem.lancaster import LancasterStemmer


# concordance will print all the occurrences of a word along with some context. Let's explore two texts - Moby Dick and 
# Sense and Sensibility. As expected, word usage and language in both these books are pretty different :) 

text1.concordance("monstrous")


# In[ ]:

text2.concordance("monstrous")


# In[ ]:

# As you can see, Melville uses the word 'monstrous' in a different connotation than Austen. He uses it to indicate
# size and things that are terrifying, Austen uses it in a positive connotation
# Let's see what other words appear in the same context as monstrous
text2.similar("monstrous")


# In[ ]:

# Clearly Austen uses "monstrous" to represent positive emotions and to amplify those emotions. She seems to use it 
# interchangeably with "very"  
text2.common_contexts(["monstrous","very"])


# In[ ]:

# These are fun ways to explore the usage of natural language in different contexts or situations. Let's see how the 
# usage of certain words by Presidents has changed over the years. 
# (Do install matplotlib before you run the below line of code)
text4.dispersion_plot(["citizens","democracy","freedom","duties","America"])
text = "This is Andela. Where EPIC is the culture"
sents = sent_tokenize(text)
words = [word_tokenize(sent) for sent in sents]

# print (sents)
# print (words)

customStopWords = set(stopwords.words('english')+list(punctuation))
wordsWOStopWords = [word for word in word_tokenize(text) if word not in customStopWords]
# print (wordsWOStopWords)

text2 = "I was about to call you but I realised I forgot to save your phone number last time we met"

st = LancasterStemmer()
stemword = [st.stem(word) for word in word_tokenize(text2)]

# print (stemword)

print(nltk.pos_tag(word_tokenize(text2)))