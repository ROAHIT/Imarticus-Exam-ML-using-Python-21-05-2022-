# -*- coding: utf-8 -*-
"""Imarticus Exam -1 (Solution).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vZL21YVJJuZwZ3sZxatY34r4ga4Hxi-2
"""

# Import drive

from google.colab import drive
drive.mount('/content/drive')

# importing the dataset

import pandas as pd

df=pd.read_csv('/content/drive/MyDrive/Imarticus Datasets/Paper1/bank.csv')

"""Q1. The primary analysis of several categorical
features.
"""

df.head()

df.info()

df.shape

df.columns

df.describe()

df

# histogram

import matplotlib.pyplot as plt

df.hist()
plt.show()

# Build a function to show categorical values disribution

def bar(col):
    # temp df 
    temp= pd.DataFrame()
    # count categorical values
    temp['No_deposit'] = df[df['y'] == 'no'][col].value_counts()
    temp['Yes_deposit'] = df[df['y'] == 'yes'][col].value_counts()
    temp.plot(kind='bar')
    plt.xlabel(f'{col}')
    plt.ylabel('Number of clients')
    plt.title('Distribution of {} and deposit'.format(col))
    plt.show();

bar('job')
bar('marital')
bar('education')
bar('contact')
bar('loan')
bar('housing')

"""Primary analysis of several categorical features reveals:

1. Deposit is mostly opened by Administrative staff and technical specialists
2. Response of the single is better than married.
3. The difference is a between consumers who already use the services of banks and received a loan.
4. Home ownership does not affect greatly the performance.
"""

# Heatmap

import seaborn as sns

sns.heatmap(df.select_dtypes(['float64','int64']).corr(),annot=True)
plt.show()

"""Q2. Exploratory Data Analysis

a. Missing Value Analysis
"""

# cheaking for missing values

df.isna().sum().sort_values(ascending=False)

"""Missing values treatment :

There are no missing values in the dataset

b. Label Encoding wherever required
"""

df.y=df.y.replace({'yes':1,'no':0})

df.head()

# Replacing values with binary ()
df.contact = df.contact.replace({'cellular': 1, 'telephone': 0}) 
df.loan = df.loan.replace({'yes': 1, 'unknown': 0, 'no' : 0})
df.housing = df.housing.replace({'yes': 1, 'unknown': 0, 'no' : 0})
df.default = df.default.replace({'no': 1, 'unknown': 0, 'yes': 0})
df.pdays = df.pdays.replace(999, 0) # replace with 0 if not contact 
df.previous = df.previous.apply(lambda x: 1 if x > 0 else 0) # binary has contact or not
df.marital = df.marital.replace({'married': 1, 'unknown': 0, 'divorced': 1,'single':0})
df.education = df.education.replace({'basic.4y':1, 'high.school':1, 'basic.6y':1, 'basic.9y':1,'professional.course':1, 'unknown':0, 'university.degree':1,'illiterate':0})


# binary if were was an outcome of marketing campane
df.poutcome = df.poutcome.replace({'nonexistent':0, 'failure':0, 'success':1})

df.info()

# creating dummies

df=pd.get_dummies(df)

df.info()

df.head()

# dropping the dummies

df.drop_duplicates(inplace=True)

"""c. Selecting important features"""

x=df.drop(['y'],axis=1)
y=df['y']

## Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)

# scalling

from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

x_train=sc.fit_transform(x_train)
x_test=sc.fit_transform(x_test)

# fitting Random Forest Classification to the training set

from sklearn.ensemble import RandomForestClassifier

classifier= RandomForestClassifier(n_estimators= 20, criterion= 'entropy', random_state= 0)

classifier.fit(x_train,y_train)

# predicting the test set results

y_pred= classifier.predict(x_test)

# measuring the accuracy of model

from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

accuracy_score(y_test,y_pred)

confusion_matrix(y_test,y_pred)

print(classification_report(y_test,y_pred))

# import roc_curve to compute reciver operating characteristics

from sklearn.metrics import roc_curve

# import roc_auc_score to calcutate area under roc curve

from sklearn.metrics import roc_auc_score

# visualizing the roc-auc curve

y_proba=classifier.predict_proba(x_test)

#we take the predicted values of class 1

y_predicted = y_proba[:,1]

# we cheak to see if the right values have been considered from the predicted values

print(y_predicted)

# using roc_curve() to generate fpr & tpr values

fpr,tpr,threshold = roc_curve(y_test,y_predicted)

# passing the fpr & tpr values to auc() to calculate the area under curve

from sklearn.metrics import auc

roc_auc=auc(fpr,tpr)
print("Area under the curve for first model:",roc_auc)

#plotting the roc curve

import matplotlib.pyplot as plt


plt.figure()
plt.plot(fpr,tpr,color='orange',lw=2,label='ROC curve (area under the curve =%0.2f'%roc_auc)

plt.plot([0,1],[0,1],color='darkgrey',lw=2,linestyle='--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.xlabel('False Positive Rate (1-Specificity)')
plt.ylabel('True positive Rate (Sensitivity)')

"""e. Standardize the data using the anyone of the scalers
provided by sklearn
"""

## Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)

#scaling
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)

"""Q3. Build the following Supervised Learning models:

a. Logistic Regression
"""

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(x_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(x_test)

accuracy_score(y_test,y_pred)

r1=metrics.accuracy_score(y_test,y_pred)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

print(classification_report(y_test,y_pred))

"""b. AdaBoost"""

from sklearn.ensemble import AdaBoostClassifier

# build the model
adaboost = AdaBoostClassifier(random_state=10)
# fit the model
adaboost.fit(x_train, y_train)

# predict the values
y_pred_adaboost  = adaboost.predict(x_test)

# compute the confusion matrix
cm = confusion_matrix(y_test, y_pred_adaboost)

# label the confusion matrix  
conf_matrix = pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],
                           index=['Actual:0','Actual:1'])

# set sizeof the plot
plt.figure(figsize = (8,5))

# plot a heatmap

sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu", cbar=False)
plt.show()

# True Negatives are denoted by 'TN'
# Actual 'O' values which are classified correctly
TN = cm[0,0]

# True Positives are denoted by 'TP'
# Actual '1' values which are classified correctly
TP = cm[1,1]

# False Negatives are denoted by 'FN'
# Actual '1' values which are classified wrongly as '0'
FN = cm[1,0]

# False Positives are denoted by 'FP'
# Actual 'O' values which are classified wrongly as '1'
FP = cm[0,1]

# accuracy measures by classification_report()
result = classification_report(y_test, y_pred_adaboost)

# print the result
print(result)

r2=accuracy_score(y_test,y_pred_adaboost)

from sklearn import metrics
# set the figure size
plt.rcParams['figure.figsize']=(8,5)

fpr, tpr, thresholds = roc_curve(y_test, y_pred_adaboost)

# plot the ROC curve
plt.plot(fpr,tpr)

# set limits for x and y axes
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])

# plot the straight line showing worst prediction for the model
plt.plot([0, 1], [0, 1],'r--')

# add the AUC score
plt.text(x = 0.05, y = 0.8, s =('AUC Score:', round(metrics.roc_auc_score(y_test, y_pred_adaboost),4)))

# name the plot, and both axes
plt.xlabel('False positive rate (1-Specificity)')
plt.ylabel('True positive rate (Sensitivity)')

# plot the grid
plt.grid(True)

# create the result table for all accuracy scores
# Accuracy measures considered for model comparision are 'Model', 'AUC Score', 'Precision Score', 'Recall Score','Accuracy Score','Kappa Score', 'f1 - score'

# create a list of column names
cols = ['Model', 'AUC Score', 'Precision Score', 'Recall Score','Accuracy Score','f1-score']

# creating an empty dataframe of the colums
result_tabulation = pd.DataFrame(columns = cols)

# compiling the required information
adaboost_metrics = pd.Series({'Model': "AdaBoost",
                     'AUC Score' : metrics.roc_auc_score(y_test, y_pred_adaboost),
                 'Precision Score': metrics.precision_score(y_test, y_pred_adaboost),
                 'Recall Score': metrics.recall_score(y_test, y_pred_adaboost),
                 'Accuracy Score': metrics.accuracy_score(y_test, y_pred_adaboost),
                  'f1-score':metrics.f1_score(y_test, y_pred_adaboost)})



# appending our result table
result_tabulation= result_tabulation.append(adaboost_metrics , ignore_index = True)

# view the result table
result_tabulation

"""c. Naïve Bayes

**1. Build the model**
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.multiclass import OneVsRestClassifier
# build the model
gnb = GaussianNB()

# define the ovr strategy
GNB = OneVsRestClassifier(gnb)

# fit the model
GNB.fit(x_train, y_train)

"""**2. Predict the values**"""

# predict the values
y_pred_GNB = GNB.predict(x_test)

"""**3. Compute accuracy measures**"""

from sklearn.metrics import confusion_matrix
# compute the confusion matrix
cm = confusion_matrix(y_test, y_pred_GNB)

# label the confusion matrix  
conf_matrix = pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
# set sizeof the plot
plt.figure(figsize = (8,5))

# plot a heatmap
# cmap: colour code used for plotting
# annot: prints the correlation values in the chart
# annot_kws: sets the font size of the annotation
# cbar=False: Whether to draw a colorbar
# fmt: string formatting code to use when adding annotations
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu", cbar=False)
plt.show()

from sklearn.metrics import classification_report
# accuracy measures by classification_report()
result = classification_report(y_test,y_pred_GNB)

# print the result
print(result)

r3=accuracy_score(y_test,y_pred_GNB)

"""**4. Tabulate the results**"""

from sklearn import metrics
# create the result table for all accuracy scores
# Accuracy measures considered for model comparision are 'Model', 'AUC Score', 'Precision Score', 'Recall Score','Accuracy Score','Kappa Score', 'f1 - score'

# create a list of column names
cols = ['Model', 'Precision Score', 'Recall Score','Accuracy Score','f1-score']

# creating an empty dataframe of the colums
result_tabulation = pd.DataFrame(columns = cols)

# compiling the required information
Naive_bayes = pd.Series({'Model': "Naive Bayes",
                 'Precision Score': metrics.precision_score(y_test, y_pred_GNB,average="macro"),
                 'Recall Score': metrics.recall_score(y_test, y_pred_GNB ,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test, y_pred_GNB),
                  'f1-score':metrics.f1_score(y_test, y_pred_GNB,average = "macro")})



# appending our result table
result_tabulation = result_tabulation.append(Naive_bayes , ignore_index = True)

# view the result table
result_tabulation

"""d. KNN"""

# instantiate the 'KNeighborsClassifier'
# n_neighnors: number of neighbors to consider
# default metric is minkowski, and with p=2 it is equivalent to the euclidean metric
from sklearn.neighbors import KNeighborsClassifier
knn_classification = KNeighborsClassifier(n_neighbors = 3)

# fit the model using fit() on train data
knn_model = knn_classification.fit(x_train, y_train)

"""#### Build a confusion matrix."""

from matplotlib.colors import ListedColormap
y_pred = knn_model.predict(x_test)
cm = confusion_matrix(y_test, y_pred)

conf_matrix = pd.DataFrame(data = cm,columns = ['Predicted:0','Predicted:1'],\
                               index = ['Actual:0','Actual:1'])

sns.heatmap(conf_matrix, annot = True, fmt = 'd', cmap = ListedColormap(['lightskyblue']), cbar = False,linewidths = 0.1, annot_kws = {'size':25})


plt.xticks(fontsize = 20)


plt.yticks(fontsize = 20)

# display the plot
plt.show()

"""**Calculate performance measures on the test set.**"""

test_pred = knn_model.predict(x_test)



test_report = classification_report(y_test, test_pred)

# print the performace measures
print(test_report)

r4=accuracy_score(y_test,test_pred)

"""e. SVM"""

# SVM Classifier
#fiting svm to the training set
from sklearn.svm import SVC
classifier=SVC(kernel='rbf',probability= True, random_state=0)
classifier.fit(x_train,y_train)

#predicting the test set results
y_pred=classifier.predict(x_test)

#to measure the accuracy of model
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
accuracy_score(y_test,y_pred)

r5=accuracy_score(y_test,y_pred)

#making confusion matrix
confusion_matrix(y_test,y_pred)

#classification report
z=classification_report(y_test,y_pred)
print(z)

"""Q4. Tabulation of the performance metrics of all the above models."""

from sklearn import metrics
# create the result table for all accuracy scores
# Accuracy measures considered for model comparision are 'Model', 'AUC Score', 'Precision Score', 'Recall Score','Accuracy Score','Kappa Score', 'f1 - score'

# create a list of column names
cols = ['Model', 'Precision Score', 'Recall Score','Accuracy Score','f1-score']

# creating an empty dataframe of the colums
result_tabulation = pd.DataFrame(columns = cols)

# compiling the required information

Logistic_Regression = pd.Series({'Model': "Logistic_Regression",
                 'Precision Score': metrics.precision_score(y_test,y_pred,average="macro"),
                 'Recall Score': metrics.recall_score(y_test,y_pred,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test,y_pred),
                  'f1-score':metrics.f1_score(y_test,y_pred,average = "macro")})

adaboost = pd.Series({'Model': "adaboost",
                 'Precision Score': metrics.precision_score(y_test,y_pred_adaboost,average="macro"),
                 'Recall Score': metrics.recall_score(y_test,y_pred_adaboost,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test,y_pred_adaboost),
                  'f1-score':metrics.f1_score(y_test,y_pred_adaboost,average = "macro")})




Naive_bayes = pd.Series({'Model': "Naive Bayes",
                 'Precision Score': metrics.precision_score(y_test, y_pred_GNB,average="macro"),
                 'Recall Score': metrics.recall_score(y_test, y_pred_GNB ,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test, y_pred_GNB),
                  'f1-score':metrics.f1_score(y_test, y_pred_GNB,average = "macro")})
KNN = pd.Series({'Model': "KNN",
                 'Precision Score': metrics.precision_score(y_test,test_pred,average="macro"),
                 'Recall Score': metrics.recall_score(y_test,test_pred,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test,test_pred),
                  'f1-score':metrics.f1_score(y_test,test_pred,average = "macro")})
SVM = pd.Series({'Model': "SVM",
                 'Precision Score': metrics.precision_score(y_test,y_pred,average="macro"),
                 'Recall Score': metrics.recall_score(y_test,y_pred,average="macro"),
                 'Accuracy Score': metrics.accuracy_score(y_test,y_pred),
                  'f1-score':metrics.f1_score(y_test,y_pred,average = "macro")})



# appending our result table
result_tabulation = result_tabulation.append(Logistic_Regression,ignore_index=True)
result_tabulation = result_tabulation.append(adaboost,ignore_index=True)
result_tabulation = result_tabulation.append(Naive_bayes,ignore_index=True)
result_tabulation = result_tabulation.append(KNN,ignore_index=True)
result_tabulation = result_tabulation.append(SVM,ignore_index=True)
# view the result table
result_tabulation

