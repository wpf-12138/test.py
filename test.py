import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix


text='喂你好,唉请问是王银军先生是吧?噢您这个号码大概用了多长时间了'
print((text.index('时间') - text.index('号'))<10)
print((text.index('时间') > text.index('号')))
if (text.index('时间') - text.index('号')) < 10 and (text.index('时间') > text.index('号')):
    print('M')