#import modules
import numpy as np
import sklearn
import sys
import csv
from sklearn import svm
from sklearn.metrics import mean_squared_error, accuracy_score

#function which returns numpy arrays given list from csv file
def get_vector_data(datafile):
    global class_or_reg
    X = []
    Y = []
    for data in datafile[1:]:
      vector_X = np.zeros(len(data)-1)
      for i in range(len(data)-1):
        vector_X[i] = float(data[i])
      X.append(vector_X)
    
      if class_or_reg == "reg": #Create different 'Y' for classification or regression 
        Y.append(float(data[-1]))
      else:
        if float(data[-1]) >= 30:
          Y.append(1)
        else:
          Y.append(0)

    return X, Y

#given model and test data, return accuracy (class) or mean squared error (reg)
def test_model(model, testdata):
    global class_or_reg
    print("Beginning testing...")
    X_test = testdata[0]
    Y_test = testdata[1]
    predictions = model.predict(X_test)

    if class_or_reg == "class":
      accuracy=accuracy_score(Y_test, predictions)
      print ("Accuracy: "+str(round(accuracy,3)))
      return accuracy

    else:
      mse = mean_squared_error(predictions, Y_test)
      print("Mean squared error of model: ", mse)
      return mse

#given train and test data, return the trained model and it's performance measure
def train_model(X_train,Y_train, X_test, Y_test):
    print("Creating model...")
    global class_or_reg
    if class_or_reg == "class":
      model = sklearn.svm.SVC(kernel="linear",gamma="auto")
      model.fit(X_train, Y_train)
      accuracy = test_model(model, [X_test, Y_test])
    else:
      model = sklearn.svm.SVR(kernel="linear",gamma="auto")
      model.fit(X_train, Y_train)
      mse = test_model(model, [X_test, Y_test])

    if class_or_reg == "class":
      return model, accuracy
    else:
      return model, mse


#retrieve system arguements
class_or_reg, data_train, data_test = sys.argv[1:]

#open csv files and cast to lists
with open(data_train, newline='') as file:
    reader = csv.reader(file)
    datasetfile_train = list(reader)

with open(data_test, newline='') as file:
    reader = csv.reader(file)
    datasetfile_test = list(reader)

#Convert train and test data to numpy arrays
X_train, Y_train = get_vector_data(datasetfile_train)
X_test, Y_test = get_vector_data(datasetfile_test)

#Define, train and retrieve performance measures from model
model, performance = train_model(X_train, Y_train, X_test, Y_test)






