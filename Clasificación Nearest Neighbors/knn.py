#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Enero 2023

@author: Mateo Echavarria Sierra
"""

# K - Nearest Neighbors (K-NN)


# Cómo importar las librerías
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importar el data set
dataset = pd.read_csv('Social_Network_Ads.csv')

X = dataset.iloc[:, [2,3]].values
y = dataset.iloc[:, 4].values


# Dividir el data set en conjunto de entrenamiento y conjunto de testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)


# Escalado de variables
"""
Se hace el escalado de variables dado que se trabajaran con distancias
que ninguna variable tenga mayor relevancia a la otra y no se pierda
informacion recolectada
"""
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)


# Ajustar el clasificador en el Conjunto de Entrenamiento
from sklearn.neighbors import KNeighborsClassifier
"""
Escoger numeros impares es mejor dado que no pueden haber empates para escoger
a los k vecinos
"""
k = 9
classifier = KNeighborsClassifier(n_neighbors = k, metric = "minkowski", p = 2)
classifier.fit(X_train, y_train)

# Predicción de los resultados con el Conjunto de Testing
y_pred  = classifier.predict(X_test)

# Elaborar una matriz de confusión
"""
Confirmar la confirabilidad de nuestras predicciones en cuanto a falsos positivos
y falsos negativos 
"""
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Visualización de Publico Objetivo

only_yes = dataset.loc[dataset['Purchased'] == 1]

all_yes_salary = {}
for i in range(14):
    num = 10000*i
    aux = dataset[(dataset['EstimatedSalary'] < 10000 +  num) & (dataset['EstimatedSalary'] > 0 + num)]
    all_yes_salary[f'{(num + 10000)//1000}k']  = len(aux)

all_yes_age = {}
for i in range(20):
    num = 3*i
    aux = dataset[(dataset['Age'] < 3 +  num) & (dataset['Age'] > 0 + num)]
    all_yes_age[f'{(num + 3)}']  = len(aux)

plt.title("Cantidad de Clientes que compraron el producto segun su Salario")
plt.plot(all_yes_salary.keys(), all_yes_salary.values(), color = 'black',
         linestyle = 'dashed')
plt.scatter(all_yes_salary.keys(), all_yes_salary.values(), marker = 'o', s = 25, color = 'red')
plt.show()

plt.title("Cantidad de Clientes que compraron el producto segun su Edad")
plt.plot(all_yes_age.keys(), all_yes_age.values(), color = 'black',
         linestyle = 'dashed')
plt.scatter(all_yes_age.keys(), all_yes_age.values(), marker = 'o', s = 25, color = 'red')
plt.show()



# Representación gráfica de los resultados del algoritmo en el Conjunto de Entrenamiento
from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title(f'K-NN (Conjunto de Entrenamiento, k = {k})')
plt.xlabel('Edad')
plt.ylabel('Sueldo Estimado')
plt.legend()
plt.show()


# Representación gráfica de los resultados del algoritmo en el Conjunto de Testing
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title(f'K-NN (Conjunto de Test, k = {k})')
plt.xlabel('Edad')
plt.ylabel('Sueldo Estimado')
plt.legend()
plt.show()




