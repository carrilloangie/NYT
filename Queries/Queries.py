
# coding: utf-8

# In[1]:


import os
import xml.etree.cElementTree as et
from progressbar import ProgressBar
import csv
import itertools
import nltk
from nltk.corpus import stopwords
import re
import string
import pickle


# In[ ]:


####STEP 1: Collect the keywords in order to create the queries
###Create a list with all the paths (going through every forlder and subfolder) in which the documents are located
def GetPaths(path):
    allArticles=[]
    years=os.listdir(path)
    for i in years:
        pathyear=path+str(i)
        months=os.listdir(pathyear)
        pathyear=pathyear+'/'
        for j in months:
            pathmonth=pathyear+str(j)
            days=os.listdir(pathmonth)
            pathmonth=pathmonth+'/'
            for k in days:
                pathdays=pathmonth+str(k)
                articles=os.listdir(pathdays)
                for l in range(len(articles)):
                    articles[l]=pathdays+'/'+articles[l]
                allArticles=allArticles+articles
    return allArticles


# In[ ]:


###Extract the keywords
def Extraction(allArticles):
    pbar=ProgressBar()
    kw=[]
    for i in pbar(allArticles):
        doc=0
        doc = et.parse(i)
        element=0
        element = doc.find('head')
        y=[]
        z=[]
        x=k1=k2=v1=v2=0
        for node in element.getiterator():
            x=node.attrib
            if len(x)==2:
                k1=list(x.keys())[0]
                v1=list(x.values())[0]
                if (k1=='class' or k1=='type' or k1=='classifier type') and (v1=="descriptor" or v1=="indexing_service"):
                    k2=list(x.keys())[1]
                    v2=list(x.values())[1]
                    if (k2=='class' or k2=='type' or k2=='classifier type') and (v2=="indexing service" or v2=="descriptor"):
                        y.append(node.text)
                if (k1=='class' or k1=='type' or k1=='classifier type') and (v1=="online_producer" or v1=="general_descriptor"):
                    k2=list(x.keys())[1]
                    v2=list(x.values())[1]
                    if (k2=='class' or k2=='type' or k2=='classifier type') and (v2=="general_descriptor" or v2=="online_producer"):
                        z.append(node.text)
        kw.append(y)
        kw.append(z)
    return kw


# In[7]:


###Delete empty keywords
def Delete_empty(kw):
    pbar=ProgressBar()
    n_kw = [x for x in pbar(kw) if x != []]
    return n_kw


# In[8]:


def SaveBinary(FileName,file):
    output_file = open(FileName, "wb")
    pickle.dump(file, output_file)
 
    output_file.close()
    return()


# In[97]:

def Remove_Dups(n_kw):
    pbar=ProgressBar()
    new_k = []
    for elem in n_kw:
        if elem not in new_k:
            new_k.append(elem)
    k = new_k
    return(k)

####STEP 2: Tokenize each text, turning each document into a list of tokens
def Tokenize(n_kw):
    pbar=ProgressBar()
    tokens=[]
    for element in pbar(n_kw):
        b=[]
        for tok in element:
            b=nltk.word_tokenize(tok)
        tokens.append(b)
    return tokens

####STEP 3: Do linguistic preprocessing, producing a list of normalized tokens, which are the indexed terms.
def Normalize(tokens):

    pbar=ProgressBar()

    #Normalization

    x=re.compile('[%s]'%re.escape(string.punctuation))
    normalized=[]
    stemmer=nltk.PorterStemmer()

    for element in pbar(tokens):
        new=[]
        for token in element:
            new_NoSW=x.sub(u'',token)
            new_NoSW=stemmer.stem(new_NoSW)
            if not new_NoSW == u'':
                new.append(new_NoSW.lower())
        normalized.append(new)
    return normalized


# In[28]:

    
def removeSW(normalized):
    pbar=ProgressBar()

    #Remove Stopwords Body
    noStopWords=[]
    i=0
    stopWords=set(stopwords.words('english'))
    for element in pbar(normalized):
        withoutSW=[i for i in element if i not in stopWords]
        noStopWords.append(withoutSW)
    return noStopWords

def saveCSV(file,name):
    with open(name, "w",encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)
    return