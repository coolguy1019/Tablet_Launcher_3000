import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import matplotlib.pylab as plt


data = pd.read_csv("openmouth_dataset.csv", header = None)

X = data.iloc[:,1:].values
y = data.iloc[:,0].values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.1)

model = RandomForestClassifier()

model.fit(X_train,y_train)

print("Accuracy:",model.score(X_test,y_test))


plt.scatter(model.predict(X),y)
plt.show()

pickle.dump(model,open("openmouth_model1.pkl","wb"))
