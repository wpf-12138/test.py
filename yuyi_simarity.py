import gensim
import jieba
from gensim.models import word2vec
import pandas as pd
text=pd.read_excel('../催收员话术库.xlsx')
text=text[['催收员节点话术']].values.tolist()
sentence=[]
for i in text:
    sentence.append(i[0])
text=[]
for i in sentence:
    text.append(jieba.cut(i,cut_all=False))
for i in text:
    print(i)
