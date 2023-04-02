# -*- coding: utf-8 -*-
"""Technocolabs__Mini-Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CgBa0sdQnje7NQa9GhMQGMxvIZkX3OH7

# Problem Statement
The data scientists at BigMart have collected 2013 sales data for 1559 products across 10 stores in different cities. Also, certain attributes of each product and store have been defined. The aim of this data science project is to build a predictive model and find out the sales of each product at a particular store.

Using this model, BigMart will try to understand the properties of products and stores which play a key role in increasing sales.

The data has missing values as some stores do not report all the data due to technical glitches. Hence, it will be required to treat them accordingly.

#Hypothesis Generation

Using the BigMart data we have to build a predictive Model that will find out the sales of each product at a particular store.

#Importing libraries
"""

#Added libraries that help us work on the data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics

"""#Data Collection & Analysis"""

#Reading the csv file using pandas library
from google.colab import files
uploaded = files.upload()

#Shows the first five rows of the entire dataset
superMart.head()

#Shows number of rows and columns
superMart.shape

#Shows datatypes and nonull count
superMart.info()

"""#Handling Missing Values"""

#Shows the number of missing values in each column
#We recognize that there is are two columns with missing values
superMart.isnull().sum()

#For numerical values we use mean to fil the missing values
superMart['Item_Weight']=superMart['Item_Weight'].fillna(superMart['Item_Weight'].mean())
testData['Item_Weight']=testData['Item_Weight'].fillna(testData['Item_Weight'].mean())

#For textual values we use mode to fil the missing values
mode_value=superMart.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x: x.mode()[0]))
test_mode_value=testData.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x: x.mode()[0]))

print(mode_value)

missing_values=superMart['Outlet_Size'].isnull()
test_missing_values=testData['Outlet_Size'].isnull()

print(missing_values)

superMart.loc[missing_values,'Outlet_Size']=superMart.loc[missing_values,'Outlet_Type'].apply(lambda x:mode_value[x])

testData.loc[test_missing_values,'Outlet_Size']=testData.loc[test_missing_values,'Outlet_Type'].apply(lambda x:test_mode_value[x])

testData.isnull().sum()

"""#Exploratory Data Analysis

Univariate Analysis
"""

#Shows the numerical vlaues in the dataset
superMart.describe()

sns.set()

#Item Weight Distribution using Distplot
plt.figure(figsize=(6,6))
sns.displot(superMart['Item_Weight'])
plt.show()

#Item Visibility using Distplot
plt.figure(figsize=(6,6))
sns.displot(superMart['Item_Visibility'])
plt.show()

#Item MRP using Box Plot
plt.figure(figsize=(6,6))
sns.boxplot(superMart['Item_MRP'])
plt.show()

#Outlet Establishment Year using Countplot
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Establishment_Year',data=superMart)
plt.show()

#Item Outlet Sales using Distplot
plt.figure(figsize=(6,6))
sns.displot(superMart['Item_Outlet_Sales'])
plt.show()

#Outlet Location Type using Countplot
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Location_Type',data=superMart)
plt.show()

#Item Fat Content using Countplot
plt.figure(figsize=(10,6))
sns.countplot(x='Item_Fat_Content',data=superMart)
plt.show()

"""Bivariate Analysis"""

#Item Weight & Item Outlet Sales using Regplot
plt.figure(figsize=(10,6))
sns.regplot(x='Item_Weight',y='Item_Outlet_Sales',data=superMart)
plt.show()

#Outlet Identifier & Item Outlet Sales using Regplot
plt.figure(figsize=(10,6))
sns.boxplot(x='Outlet_Identifier',y='Item_Outlet_Sales',data=superMart)
plt.show()

"""#Feature Engineering"""

#Shows the count per category
superMart['Item_Fat_Content'].value_counts()

#Merging the categories that are same
superMart.replace({'Item_Fat_Content':{'low fat':'Low Fat','LF':'Low Fat','reg':'Regular'}},inplace=True)
testData.replace({'Item_Fat_Content':{'low fat':'Low Fat','LF':'Low Fat','reg':'Regular'}},inplace=True)

#Checking after merging
superMart['Item_Fat_Content'].value_counts()

"""#Encoding

Label encoding
"""

superMart.info()

#Assigning vairable
encoder = LabelEncoder()

#Converting textual values to numerical values
superMart['Item_Identifier']=encoder.fit_transform(superMart['Item_Identifier'])
testData['Item_Identifier']=encoder.fit_transform(testData['Item_Identifier'])

superMart['Item_Fat_Content']=encoder.fit_transform(superMart['Item_Fat_Content'])
testData['Item_Fat_Content']=encoder.fit_transform(testData['Item_Fat_Content'])

superMart['Item_Type']=encoder.fit_transform(superMart['Item_Type'])
testData['Item_Type']=encoder.fit_transform(testData['Item_Type'])

superMart['Outlet_Identifier']=encoder.fit_transform(superMart['Outlet_Identifier'])
testData['Outlet_Identifier']=encoder.fit_transform(testData['Outlet_Identifier'])

superMart['Outlet_Size']=encoder.fit_transform(superMart['Outlet_Size'])
testData['Outlet_Size']=encoder.fit_transform(testData['Outlet_Size'])

superMart['Outlet_Location_Type']=encoder.fit_transform(superMart['Outlet_Location_Type'])
testData['Outlet_Location_Type']=encoder.fit_transform(testData['Outlet_Location_Type'])

superMart['Outlet_Type']=encoder.fit_transform(superMart['Outlet_Type'])
testData['Outlet_Type']=encoder.fit_transform(testData['Outlet_Type'])

superMart.head()

"""#Splitting Data into X and Y variables"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,accuracy_score,classification_report,confusion_matrix

#Splitting the data into target and features
x=superMart.drop(columns='Item_Outlet_Sales',axis=1)
y=superMart['Item_Outlet_Sales']

#Variables for modeling
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

print(x.shape,x_train.shape,x_test.shape)

"""#Machine Learning Training Models

**Linear Regression Model**
"""

from sklearn.linear_model import LinearRegression

LR=LinearRegression()

LR.fit(x_train,y_train)

predicted=LR.predict(x_test)

from sklearn.metrics import r2_score

LRScore=r2_score(y_test,predicted)

print("LR Score: ",LRScore)

"""**ADA Boost Regression**"""

from sklearn.ensemble import AdaBoostRegressor

abr=AdaBoostRegressor(n_estimators=70)

abr.fit(x_train,y_train)

predicted=abr.predict(x_test)

from sklearn.metrics import r2_score

ADAScore=r2_score(y_test,predicted)

print("ADA SCORE",ADAScore)

"""**Random Forest Model**"""

from sklearn.ensemble import RandomForestRegressor

rfg=RandomForestRegressor()

rfg.fit(x_train,y_train)

predicted=rfg.predict(x_test)

from sklearn.metrics import r2_score

RFRScore=r2_score(y_test,predicted)

print("RFR SCORE: ",RFRScore)

"""**XGBoost Model**"""

from xgboost import XGBRegressor

xgb=XGBRegressor()

xgb.fit(x_train,y_train)

predicted=xgb.predict(x_test)

from sklearn.metrics import r2_score

XGBScore=r2_score(y_test,predicted)

print("XGB SCORE: ",XGBScore)

"""#Summary

First we studied the Big Mart Sales Data and tried to understand all the features of the data. After which we performed Exploratory Data Analysis(Univariate & Bivariate Analysis) by plotting graphs and building relations. After which we treated the missing values and applied Feature Engieening as well. Then we moved our awy towards encoding and converted textual data to numerical data so that we can apply train our machine learning models. Which in turn helped us to predict the Outlet_Sales.

#Results

From the different Machine Learning Models we applied, we found the following results: 

- LR Score:  0.48
- ADA Score: 0.52
- RFR SCORE:  0.52
- XGB SCORE:  0.57

The results show us that XGBBoost performed the best out of all the models.

#Results
"""

#Plotting the results (Original VS Predicted)
predictedData=pd.DataFrame({'Original': y_test, 'Predicted': predicted})
sns.relplot(x='Original', y='Predicted',data=predictedData,)