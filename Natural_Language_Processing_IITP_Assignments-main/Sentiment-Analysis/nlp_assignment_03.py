# -*- coding: utf-8 -*-
"""NLP_Assignment_03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TkrrKU2RCH5s7aNQ59HWmwP5aCymaXrU

```
NLP Assignment 3 (Sentiment Analysis)
Name : Krishna Kant Verma
Roll No : 2211cs19
Name : Gourob Chatterjee
Roll No : 2211cs08
```

$$
Importing \space All \space Required \space Libraries
$$
"""

import spacy
import re
import sys
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from keras.layers import LSTM,Dense,Flatten
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow import keras
from progressbar import progressbar
import pandas as pd
import numpy as np

"""# Zip File Extraction

```
# Extracting the Positive Zip Folder and Negative Zip Folder to POS/NEG SubFolder 
```
"""

import shutil
pos_zip = "/content/pos.zip"
neg_zip = "/content/neg.zip"
shutil.unpack_archive(pos_zip, "/content/POS", "zip")
shutil.unpack_archive(neg_zip, "/content/NEG", "zip")

"""

```
Import OS Libarary and Read File
```

"""

import os
def read_file(file_location):
    with open(file_location, 'r', encoding='utf-8') as f:
        return f.readlines()

"""

```
Reading Text Data and Processing it Make it Operable
```

"""

def read_text(folder_locations, max_files_toread):
    textData = []
    textFileLocations = []
    if not isinstance(folder_locations, str):
        for location in folder_locations:
            textFileLocations.append([os.path.join(location, file_name) for file_name in os.listdir(location)][:max_files_toread])
    else:
        print("Folder locations should be in list or tuple format.\nExample: [Folder loc1, Folder loc2, Folder loc3]")
        return

    classNames = [0 for _ in folder_locations]
    currLen = 0

    for location_ind, text_file_location in enumerate(textFileLocations):
        for text_file in text_file_location:
            try:
                textData.append(read_file(text_file))
            except Exception as e:
                print(e, text_file)
        classNames[location_ind] = len(textData) - currLen
        currLen = len(textData)

    classLabels = []
    for index, no_of_files_inclass in enumerate(classNames):
        classLabels += [index for number in range(no_of_files_inclass)]
    return textData, classLabels

textData, classLabels = read_text(["/content/NEG/neg", "/content/POS/pos"], 5000)

"""

```
Printing textData 1 output (with labels)
```

"""

textData[1],classLabels[1]

textData[0]

"""

```
Eliminating all unnecessary HTML and other hyper Texts
```

"""

regex = re.compile(r'<[^>]+>')
def removeHyperTags(string):
    return regex.sub(' ', string)

"""

```
calling removeHyperText Function
```

"""

textData = [removeHyperTags(text[0]) for text in textData]

"""

```
Text After Processing all the removal of hypertexts
```

"""

textData[0]

"""#Tokenizing Texts

```
Function to Tokenize text
```
"""

def tokenize(texts):
    for text_ind,text in enumerate(texts):
        texts[text_ind]=text.lower()     
    nlp = spacy.load('en_core_web_sm') 
    tokenizedTexts = []
    for ind,text in enumerate(texts):
        print(ind,len(texts))
        doc = nlp(text) 
        tokens = [token.text for token in doc]  
        tokenizedTexts.append(tokens)   
    return tokenizedTexts

"""

```
Calling Tokenize Text Function over First Dataset
```

"""

tokenizedTexts = tokenize(textData)

"""# Finding Out Most Frequent Tokens In DataSet

```
Function to find Out most frequent tokens
```
"""

def maxFrequentTokens( textData, frequency=5 ):
    counter={}
    for text in textData:
        for token in text:
            if token in counter:
                counter[token]+=1
            else:
                counter[token]=1
    FrequentTokens=[]
    for i in counter.items():   
      if i[1]>frequency:
        FrequentTokens.append(i[0])
    return FrequentTokens

FrequentTokens = maxFrequentTokens(tokenizedTexts,frequency=300)

f" Most frequent Tokens length  {len(FrequentTokens)}"

tokenizedTexts[1][:10]

"""# Finding Out Padding Sequences"""

def padSeq(sequences):
    averageLen=0
    for text in sequences:
        averageLen+=len(text)
    averageLen=int(averageLen/len(tokenizedTexts))
    for text_ind,text in enumerate(sequences):
        if len(text)>=averageLen:
            sequences[text_ind]=text[:averageLen]
        else:
            for i in range(averageLen-len(text)):         
              sequences[text_ind].append('PAD')

padSeq(tokenizedTexts)

"""#Encoding Words to One-Hot-Encoding"""

def oneHotEncoding(tokenizedTexts):  
    token_to_number={x:to_categorical(ind,num_classes=len(FrequentTokens)+1,dtype='uint8') for ind,x in enumerate(FrequentTokens)}
    token_to_number['unk']=np.array([0 for x in range(len(FrequentTokens))]+[1])
    for text in tokenizedTexts:
      for token_ind,token in enumerate(text):
        if token in token_to_number:
          text[token_ind]=token_to_number[token]
        else:
          text[token_ind]=token_to_number['unk']   
oneHotEncoding(tokenizedTexts)

X_array = np.array(tokenizedTexts,dtype='uint8')

dataSet_1 = X_array

"""# Second Dataset (SemEval Tweet Dataset)"""

data_2 = pd.read_csv("/content/2013semeval_train.csv")

data_2.tweet

"""#unicode Cleaning"""

uniEscRegx = re.compile(r'\\u([0-9a-fA-F]{4})')
def convert_escape_sequence(match):
    return chr(int(match.group(1), 16))

result = uniEscRegx.sub(convert_escape_sequence, data_2.tweet[1])
def changeString(string):
    return uniEscRegx.sub(convert_escape_sequence,string)

print(result)

data_2.tweet = data_2.tweet.apply(changeString)

"""#Tokenizing Second Tweet DataSet"""

tokenizedTexts = tokenize( data_2.tweet )

"""#Finding Out Most Freuent Tokens"""

FrequentTokens = maxFrequentTokens(tokenizedTexts,frequency=200)
f" Most frequent Tokens length  {len(FrequentTokens)}"

"""#Conversion to One Hot Encoding after Padding Sequences"""

padSeq(tokenizedTexts)      
oneHotEncoding(tokenizedTexts)

X_array = np.array(tokenizedTexts,dtype='uint8')

dataSet_2 = X_array

dataSet_1.shape,dataSet_2.shape

"""\

```
# converting first dataset labels to numpy array
```
"""

dataSet_1_labels=np.array(classLabels)

"""

```
# converting second dataset labels to numpy array
```"""

uniqLabels={x:ind for ind,x in enumerate(data_2.label.unique())}

data_2.label = data_2.label.apply(lambda x:uniqLabels[x])

dataSet_2_labels = data_2.label.values

"""#Finalizing Our DataSet (Shaping Our Dataset)"""

dataSet_1.shape
dataSet_1_labels.shape
dataSet_2.shape
dataSet_2_labels.shape

"""# Creating Model Using RNN

```
Creating Model For First Dataset
```
"""

model_1_RNN=keras.Sequential([
    LSTM(256,input_shape=dataSet_1.shape[1:]),
    Dense(2,activation='sigmoid')
])

model_1_RNN.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

"""

```
# Creating Model For Second Dataset
```

"""

model_2_RNN=keras.Sequential([
    LSTM(256,input_shape=dataSet_2.shape[1:]),
    Dense(3,activation='sigmoid')
])

model_2_RNN.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

from sklearn.model_selection import train_test_split
print(len(dataSet_1_labels))

xTrain_1, xTest_1, yTrain_1, yTest_1 = train_test_split(dataSet_1, dataSet_1_labels, test_size=0.25, random_state=42)
xTrain_2, xTest_2, yTrain_2, yTest_2 = train_test_split(dataSet_2, dataSet_2_labels, test_size=0.25, random_state=42)

"""# Excuetion of Model 1"""

execModel_1 = model_1_RNN.fit(xTrain_1,yTrain_1,epochs=10)

"""# Excuetion of Model 2"""

execModel_2 = model_2_RNN.fit(xTrain_2,yTrain_2,epochs=10)

"""#Calculating Precision Accuracy and Recall for First Dataset"""

from sklearn.metrics import precision_recall_fscore_support
y_pred_1=model_1_RNN.predict(xTest_1)
scores=precision_recall_fscore_support(np.argmax(y_pred_1,axis=1),yTest_1,average='macro')
print(f"""\n\nRNN Model_1 For DataSet1
    Precision = {scores[0]}
    Recall    = {scores[1]}
    f1_score  = {scores[2]}
""")

"""# Calculating Precision Accuracy and Recall for Second Dataset"""

from sklearn.metrics import precision_recall_fscore_support
y_pred_2=model_2_RNN.predict(xTest_2)
scores=precision_recall_fscore_support(np.argmax(y_pred_2,axis=1),yTest_2,average='macro')
print(f"""\n\nRNN Model_2 For DataSet_2
    Precision = {scores[0]}
    Recall    = {scores[1]}
    f1_score  = {scores[2]}
""")

"""#Logs after Each Epocs"""

execModel_1.history

"""#Plots

```
plotting epocs Vs Loss For Model 1
```
"""

plt.plot([x for x in range(10)],execModel_1.history['loss'],c='blue')
plt.title("Epochs vs loss for dataset _1")
plt.x_label="Epochs"
plt.y_label="Loss"
plt.show()
plt.plot([x for x in range(10)],execModel_1.history['accuracy'],c='g')
plt.title("Epochs vs accuracy for dataset _1")
plt.x_label="Epochs"
plt.y_label="Loss"
plt.show()

"""

```
Plotting Epocs Vs Loss for Model 2
```

"""

plt.plot([x for x in range(10)],execModel_2.history['loss'],c='blue')
plt.title("Epochs vs loss for dataset _2")
plt.x_label="Epochs"
plt.y_label="Loss"
plt.show()
plt.plot([x for x in range(10)],execModel_2.history['accuracy'],c='green')
plt.title("Epochs vs accuracy for dataset _2")
plt.x_label="Epochs"
plt.y_label="Loss"
plt.show()

"""# Feed forward Neural Networks Architecture

My proposed feed-forward neural network (FFNN) architecture consists of two hidden layers connected by non-linear activation functions. The first hidden layer, which has 256 neurons, is coupled to the input layer. The second hidden layer, which includes 128 neurons, is connected to the first hidden layer. The output layer, whose size is determined by the number of classes in the problem, is then connected to the second hidden layer.

Here is a visual representation of the architecture:



''' Input Layer (Size depends on input data) --> Hidden Layer 1 (Size: 256) with Non-linearity ---> Hidden Layer 2 (Size: 128) with Non-linearity ---> Output Layer (Size depends on the number of classes) '''


There are several prominent options for non-linearity in this architecture, including the Rectified Linear Unit (ReLU), the hyperbolic tangent (tanh), and the Gaussian Error Linear Unit (GELU).

The binary cross-entropy loss function is frequently used for binary classification issues. The categorical cross-entropy loss function is frequently used for multi-class classification issues.


Feed-Forward There are various uses for neural networks:

    They are able to simulate intricate non-linear input–output interactions.
    They are relatively easy to comprehend and use.
    They can be trained well on sizable datasets using methods like backpropagation and stochastic gradient descent.
    They can be used to solve many different types of issues, like as classification, regression, and prediction.

However, because FFNNs do not account for the temporal correlations between inputs, they are only partially capable of handling sequential or time-series data. Additionally, if the dataset is too little or the model is too complicated, they are more likely to overfit.

Thanking You So Much
"""