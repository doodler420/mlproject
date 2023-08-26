# -*- coding: utf-8 -*-
"""Project_ML_admissiom_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C2SuHDoG2KeQ5v4ErZe8GUEnmn7gkNsn
"""

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

data = pd.read_csv('Admission_Predict_Ver1.1.csv')
data=data.drop(columns=['Serial No.'])
data.head(10)

data.columns

# checking for missing data
data.isnull().sum()

data.info()

# rename some columns
Data=data.rename(columns={'GRE Score':'GRE','TOEFL Score':'TOEFL','University Rating':'university_Rating','Chance of Admit ':'Chance_of_Admit'},inplace=True)
data.describe()

# visualize the target variable
plt.figure(figsize=(20,8))
sb.set_style('darkgrid')
plt.subplot(1,2,1)
plt.title('number of orders Distribution Plot')
sb.distplot(data.Chance_of_Admit )

plt.subplot(1,2,2)
plt.title('number of orders Spread')
sb.boxplot(y=data.Chance_of_Admit)

plt.show()

sb.barplot(data.university_Rating,data.Chance_of_Admit)

sb.scatterplot(data.GRE,data.Chance_of_Admit)

sb.scatterplot(data.TOEFL,data.Chance_of_Admit)

sb.scatterplot(data.CGPA,data.Chance_of_Admit)

#From the above scatter plots, you notice taht as the GRE,CGPA and TOEFL increase the change of getting the admission 
#increase too, there is a linear relationship between them.

# looking for relevant independent variable

plt.figure(figsize=(10,5))
cr = data.corr()
sb.heatmap(cr, annot=True, linewidths=0.05, fmt= '.2f',cmap="magma")
plt.show()

(data.corr()**2)["Chance_of_Admit"].sort_values(ascending = False)[1:]

#The top 4 independent variable correlated to the target variable are CGPA,GRE,TOEFL and University Ranting.

# Performing some transformation 
data['Chance_of_Admit']=data['Chance_of_Admit']**2

# remove some outliers
## Deleting those some outliers. 
# previous_data = data.copy()
data = data[data.Chance_of_Admit >0.40]
data.reset_index(drop = True, inplace = True)

plt.figure(figsize=(20,8))
sb.set_style('darkgrid')
plt.subplot(1,2,1)
plt.title('number of orders Distribution Plot')
sb.distplot(data.Chance_of_Admit)

plt.subplot(1,2,2)
plt.title('number of orders Spread')
sb.boxplot(y=data.Chance_of_Admit)

plt.show()

plt.figure(figsize=(20,8))
sb.set_style('darkgrid')
plt.subplot(1,2,1)
plt.title('charges Distribution Plot')
sb.regplot(x=data.CGPA, y=data.Chance_of_Admit)

plt.subplot(1,2,2)
plt.title('charges Spread')
sb.residplot(data.CGPA, data.Chance_of_Admit)

plt.show()

plt.figure(figsize=(20,8))
sb.set_style('darkgrid')
plt.subplot(1,2,1)
plt.title('charges Distribution Plot')
sb.regplot(x=data.GRE, y=data.Chance_of_Admit)

plt.subplot(1,2,2)
plt.title('charges Spread')
sb.residplot(data.GRE, data.Chance_of_Admit)

plt.show()

#From the above plot, we can see that there is not heterosedasticity between the target var and some independents variable.

data.columns

# data=data.drop(columns=['SOP','LOR ','Research'],axis=1)
x = data.iloc[:, :-1].values
y = data.iloc[:, 7].values

#split dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)

# # Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# using pca
from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_
print(explained_variance)

# Fitting linear regression Regression to the dataset
from sklearn.linear_model import LinearRegression
Lin_regressor = LinearRegression(normalize=True)
Lin_regressor.fit(X_train, y_train)
y_pred=Lin_regressor.predict(X_test)
y_train_pred=Lin_regressor.predict(X_train)

#the accuracy.std() is low which means our variance is low whats is good

from sklearn.metrics import mean_squared_error
from math import sqrt
print("RMSE score on the test set:",sqrt(mean_squared_error(y_test, y_pred)))
print("RMSE score on the training set:",sqrt(mean_squared_error(y_train, y_train_pred)))
from sklearn.metrics import r2_score
print("R2 score on the test set:",r2_score(y_test, y_pred)*100)
print("R2 score on the training set:",r2_score(y_train, y_train_pred)*100)

from sklearn.ensemble import RandomForestRegressor
RDF_regressor = RandomForestRegressor(n_estimators = 30, random_state = 0)
RDF_regressor.fit(X_train, y_train)
y_pred2=RDF_regressor.predict(X_test)
y_train_pred2=RDF_regressor.predict(X_train)
print("RMSE score on the test set:",sqrt(mean_squared_error(y_test, y_pred2)))
print("RMSE score on the training set:",sqrt(mean_squared_error(y_train, y_train_pred2)))

print("R2 score on the test set:",r2_score(y_test, y_pred2)*100)
print("R2 score on the training set:",r2_score(y_train, y_train_pred2)*100)

#The linear regression perform better !, the rmse difference between the test set and the training set of the linear regression is very small compared to the one of random forest regression.

# cross validation
# Applying k-Fold Cross Validation USED TO JUST IMPROVE THE MODEL PERFORMANCE(ACCURACY)
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = Lin_regressor, X = X_train, y = y_train, cv = 5)
print(accuracies.mean(),accuracies.std())

plt.figure(figsize=(10,4))
sb.set_style('darkgrid')
plt.scatter(y_test,y_pred)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Visualizing the model performance')
plt.grid()

