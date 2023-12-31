import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import mysql.connector


app = Flask(__name__)
model = pickle.load(open('randomForest_model.pkl', 'rb'))


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['GET','post'])
def predict():
	conn=mysql.connector.connect(user="root",password="",host="localhost",port=3306,database="college")
	cursor=conn.cursor()
	GRE_Score = int(request.form['GRE Score'])
	TOEFL_Score = int(request.form['TOEFL Score'])
	University_Rating = int(request.form['University Rating'])
	SOP = float(request.form['SOP'])
	LOR = float(request.form['LOR'])
	CGPA = float(request.form['CGPA'])
	Research = int(request.form['Research'])
	
	final_features = pd.DataFrame([[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research,GRE_Score+TOEFL_Score,University_Rating+SOP+LOR+CGPA]])
	
	predict = model.predict(final_features)
	
	output = float(predict[0])
	print(output)
	sql_query=("INSERT INTO admission(GRE,TOEFL,UniversityRating,SOP,LOR,CGPA,Research,ChanceofAdmit) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
	#sql=("INSERT INTO admission(GRE,TOEFL,UniversityRating,SOP,LOR,CGPA,Research,ChanceofAdmit) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
	val=(GRE_Score,TOEFL_Score,University_Rating,SOP,LOR,CGPA,Research,output)
	cursor.execute(sql_query,val)
	conn.commit()
	conn.close()
	return render_template('index.html', prediction_text='Admission chances are {}'.format(output))
	
if __name__ == "__main__":
	app.run(debug=True)
