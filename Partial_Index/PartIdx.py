import pickle


def Retrieve(file):
    input_file = open(file, "rb")
    return input_file

def Selectivity(Queries,Lex,Freq):
    q=[]
    for i in Queries:
        d={}
        for j in i:
            for l in Lex:
                if j==l:
                    d[l[0]]=l[1]
                   
        sorted(d.items(), key=lambda x: x[1])
    return d


    
   