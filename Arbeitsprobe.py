import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

#funktion zur korrekten formatierung "numerischer Strings"
def transform(strInput):
	if "," not in strInput:
		return strInput
	
	strInput = strInput[0:-3].replace(",", "")+strInput[-3:]
	strInput = strInput.replace(",",".")
	return strInput

#Excel-Datei wird eingelesen
data = pd.read_csv("Arbeitsprobe_Data_Engineer.csv", sep=';')

#Falls Spalte nicht "Numerisch" ist (hat Datentyp int64) wird der String
#richtig formatiert so dass er im Anschluss numerisch formatiert werden kann
for i in range(0,51):
	col = data.iloc[:, i]
	
	if col.dtype == object:
		
		col = data.iloc[:, i].apply(transform)
		col = pd.to_numeric(col)
		data.iloc[:, i] = col
		uniques = pd.unique(col)


#Entfern alle Fehlerhalten Reihen
data = data[data.notnull().all(1)]

#Numerisiert den Dataframe
data = data.apply(pd.to_numeric, errors='coerce')
#data.info()

#Trainings- und Testdaten erstellen
#Verschiedene Testgroessen, tendenziell wird der "Mean Absolut Error" 
#kleiner je groesser der Trainingsdatensatz ist
"""X_train, X_test, y_train, y_test = train_test_split(
data.drop('nachforderung', axis=1), data['nachforderung'], 
test_size=0.1, random_state=42)
#X_train, X_test, y_train, y_test = train_test_split(
data.drop('nachforderung', axis=1), data['nachforderung'], 
test_size=0.05, random_state=42)"""
X_train, X_test, y_train,y_test = train_test_split(
data.drop('nachforderung', axis=1),data['nachforderung'], 
test_size=0.01, random_state=42)

#Model trainieren
model = LinearRegression()
model.fit(X_train, y_train)

#Vorhersagen generieren
predictions = model.predict(X_test)

#Gibt einen Wert von ca. 340 zurueck. Das ist innerhalb des Limits von 1000€
mse = mean_absolute_error(y_test, predictions)
print("Mean Absolute Error:", mse)


