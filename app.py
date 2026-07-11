from flask import Flask,request,render_template,jsonify
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.pipeline.prediction_pipeline import CustomData,PredictionPipeline
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        if request.is_json:
            input_data = request.json
        else:
            input_data = request.form

        data = CustomData(
            gender = input_data.get('gender'),
            race_ethnicity = input_data.get('race_ethnicity'),
            parental_level_of_education = input_data.get('parental_level_of_education'),
            lunch = input_data.get('lunch'),
            test_preparation_course = input_data.get('test_preparation_course'),
            reading_score = input_data.get('reading_score'),
            writing_score = input_data.get('writing_score')
        )
        pred_df = data.get_data_as_frame()
        print(pred_df)

        predict_pipeline = PredictionPipeline()
        pred = predict_pipeline.predict(pred_df)

        prediction_result = float(pred[0]) if isinstance(pred[0], (np.floating, float, np.integer, int)) else pred[0]

        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({'results': prediction_result})

        return render_template('home.html',results=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)