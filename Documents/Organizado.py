# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 18:04:54 2018

@author: user
"""

import os
import xml.etree.cElementTree as et
from progressbar import ProgressBar
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import re
import string
import csv
import pickle

# coding: utf-8

# In[19]:



####STEP 1: Collect the documents to be indexed
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


# In[20]:


###Extract the body and title of each document

def Extraction(allArticles):

    pbar=ProgressBar()
    ft=[]
    titles=[]

    for i in pbar(allArticles):
        doc=0
        doc = et.parse(i)
        element=0
        element = doc.find('body')
        el_head=doc.find("head")
        y=""
        try:
            for r in el_head:
                if r.tag=="title":
                    title=r.text
            for t in element.iter('block'):
                if t.attrib['class']=='full_text':
                    node=t
                    for n in node.iter('p'):
                        texto=n.text
                        y=y+texto+" "
        except:
            continue
        ft.append(y)
        titles.append(title)
     
    return ft,titles



# In[21]:


###Delete empty document
def Delete_empty(body,title,path):
    for i in range(len(body)):
        if body[i]==[]:
            body.pop(i)
            title.pop(i)
            path.pop(i)
    return body,title,path

# In[22]:

def SaveBinary(FileName,file):
    output_file = open(FileName, "wb")
    pickle.dump(file, output_file)
 
    output_file.close()
    return()

####STEP 2: Tokenize each text, turning each document into a list of tokens
def Tokenize(data):
    
    pbar=ProgressBar()

    #Tokenization Body
    tokens=[]
    k=0
    for element in pbar(data):
        tokens.append(nltk.word_tokenize(element))
    return tokens


# In[26]:


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
    stop_words = list(stopwords.words('english'))
    for element in pbar(normalized):
        withoutSW=[]
        withoutSW=[i for i in element if i not in stop_words]
        noStopWords.append(withoutSW)
    return noStopWords


# In[29]:


###Create the index of terms:

def TermsID(noStopWords):

    pbar=ProgressBar()

    terms_id={}
    k=0
    for i in pbar(noStopWords):
        for j in i:
            if j not in terms_id.values():
                terms_id[k]=j
                k=k+1
    return terms_id


# In[30]:


###Replaces terms for TermsID.

def ReplaceID(document,term_map):

    pbar=ProgressBar()

    doc_term_id=[]
    for i in pbar(document):
        doc=[]
        for j in i:
            for k,v in term_map.items():
                if v==j:
                    doc.append(k)
        doc_term_id.append(doc)
        
    doc_terms_dict={}

    for i in range(len(doc_term_id)):
        doc_terms_dict[i]=doc_term_id[i]
        
    return doc_terms_dict


# In[31]:


###Save the data

def SaveDataDict(FileName,file):

    with open(FileName, 'w') as f:
        for key in file.keys():
            f.write("%s,%s\n"%(key,file[key]))
    return


# In[32]:


####STEP 4: Index the documents that each term occurs in, by creating an inverted index, consisting of a dictionary and postings

def merge(doc_term_id):

    ###The input to indexing is a list of normalized tokens for each document which we can equally think of as a list of pairs of term and docID
    term_id=[]
    for i in range(len(doc_term_id)):
        for j in doc_term_id[i]:
            term_id_tup=(j,i)
            term_id.append(term_id_tup)

    ###Then we sort the list so the terms are in ascending order
    term_id.sort()

    ###Multiple instances of the same term from the same document are then merged
    merged=list(set(term_id)) 
    
    return merged


# In[33]:


###Instances of the same term are then grouped and the result is split into a dictionary and postings.

##Postings Lists
def PostingsLists(merged):
    posting_lists = defaultdict(list)

    for k,v in merged:
        posting_lists[k].append(v)

    posting_lists = dict(posting_lists)
    
    #Sort postings lists (by termID and then by docID)
    for k in posting_lists.keys():
        posting_lists[k].sort()
    posting_lists=dict(sorted(posting_lists.items()))

    return posting_lists 


# In[34]:

##Document Frequency
def doc_frequency(term_id):
    doc_freq={}
    for i in a:
        if i[0] not in freq.keys():
            doc_freq[i[0]]=1
        else:
            doc_freq[i[0]]=freq[i[0]]+1
    return doc_freq