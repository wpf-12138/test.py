import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
# 提取关键词
def keyword_split(data):
    data_length=len(data)
    for i in range(data_length):
        if len(data[i]) > 1:
            data_i_length=len(data[i])
            lis=[]
            for k in range(data_i_length):
                list_k=data[i][k].split('、')
                lis.append(list_k)
            data[i] = lis
        if len(data[i]) == 1:
            data[i]=data[i][0].split('、')
    return data

def hit_point(input,keywords):
    text=input
    i=0
    id_semantics=[]
    for keyword in keywords:  # 只有一个方面的关键词
        if isinstance(keyword[0], str):
            for key in keyword:
                if '...' in key:
                    f=key[:key.index('...')]
                    e=key[key.index('...')+3:]
                    if (f in text) and (e in text):
                        if (text.index(e)-text.index(f)) < 8 and (text.index(e) > text.index(f)):
                            id_semantics.append(i)
                else:
                    if key in text:
                        id_semantics.append(i)
        else:  # 有多个方面的关键词
            aspect_num = len(keyword)
            aspect_i=[]
            for keyword_i in keyword:
                mul_aspect_keyword=[]
                for key in keyword_i:
                    if '...' in key:
                        f = key[:key.index('...')]
                        e = key[key.index('...') + 3:]
                        if (f in text) and (e in text):
                            if (text.index(e) - text.index(f)) < 10 and (text.index(e) > text.index(f)):
                                mul_aspect_keyword.append('True')
                    else:
                        if key in text:
                            mul_aspect_keyword.append('True')
                if 'True' in mul_aspect_keyword:
                    aspect_i.append('True')
                else:
                    aspect_i.append('False')
            if 'False' in aspect_i:
                pass
            else:
                id_semantics.append(i)
        i=i+1
    return id_semantics

yuyi_total = ['协商还款时间'] #'首逾施压','自我介绍','协商还款时间','确认身份','确认欠款信息'
for yuyi_i in yuyi_total:
    path = './催收员节点语义表.xlsx'
    data = pd.read_excel(path,sheet_name='语义表')[:20000]
    # 将语义点中有&符号的拆分
    index = data['序号']
    sematics=data['语义点']
    data['关键词'] = data['关键词'].astype('str')
    data['关键词'] = data['关键词'].apply(lambda x : x.split('&'))
    data['关键词_length'] = data['关键词'].apply(lambda x:len(x))
    keywords = keyword_split(data['关键词'])
    input='aflj'
    points=hit_point(input=input,keywords=keywords)
    #测试
    path='./催收员画像数据all_本人v2.xlsx'
    data=pd.read_excel(path)
    yuyi= yuyi_i
    data.fillna(0,inplace=True)
    sample_a = data[data[yuyi]==1]
    sample_b = data[data[yuyi]==0]
    sample_b = sample_b[:len(sample_a)]
    data = pd.concat([sample_a,sample_b],axis=0)
    data_text=data[['文本']]
    data.reset_index(inplace=True)
    result=[]
    for text in data_text.values.tolist():
        input=str(text[0])
        points = hit_point(input=input, keywords=keywords)
        if yuyi in list(sematics[points]):
            result.append(1)
        else:
            result.append(0)
    result_r = list(data[yuyi].fillna(0))
    ind = []
    for i in range(len(result)):
        if result[i] != result_r[i]:
            ind.append(i)
    for i in ind:
        print(data_text.values.tolist()[i])
        print(result_r[i],result[i])
    print(yuyi)
    print('accuracSy_score的精度为',accuracy_score(result_r, result))
    print('precision_score的值为',precision_score(result_r, result, average='macro'))
    print('precision_score的值为',precision_score(result_r, result, average='micro'))
    print('recall_score的值为',recall_score(result_r, result, average='macro'))
    print('recall_score的值为',recall_score(result_r, result, average='micro'))
    print('混淆矩阵', confusion_matrix(result_r, result,labels=[0,1]))