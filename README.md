# 🎓 Student Math Score Predictor

An end-to-end Machine Learning web application that predicts a student's
Mathematics score based on demographic information, academic background,
and Reading and Writing scores.

The project covers the complete ML lifecycle, from exploratory data
analysis and preprocessing to model comparison, hyperparameter
optimization, API development, frontend integration, and cloud
deployment.

## 🌐 Live Application

**Live Demo:** https://ml-project-2-hlx8.onrender.com

> The backend is hosted on Render's free tier, so the first prediction
> may take some time if the server has been inactive.

## 📌 Project Overview

The model predicts a student's Mathematics score using:

-   Gender
-   Race / Ethnicity
-   Parental Level of Education
-   Lunch Program
-   Test Preparation Course
-   Reading Score
-   Writing Score

This project was built as a complete production-style Machine Learning
workflow rather than only a model-training notebook.

## ✨ Features

-   Exploratory Data Analysis
-   Automated data preprocessing
-   Numerical and categorical preprocessing pipelines
-   Missing value handling
-   Feature scaling and one-hot encoding
-   Multiple regression model comparison
-   Hyperparameter optimization using Optuna
-   Model serialization and reusable prediction pipeline
-   Flask REST API
-   React frontend built with Vite
-   Client-side input validation
-   Responsive prediction interface
-   Separate frontend and backend deployment

## 🧠 Machine Learning Pipeline

### Numerical Features

-   Reading Score
-   Writing Score

Processing:

-   Missing values handled using `SimpleImputer`
-   Features scaled using `StandardScaler`

### Categorical Features

-   Gender
-   Race / Ethnicity
-   Parental Level of Education
-   Lunch
-   Test Preparation Course

Processing:

-   Missing values handled using `SimpleImputer`
-   Categories encoded using `OneHotEncoder`

The preprocessing workflow was built using Scikit-learn's `Pipeline` and
`ColumnTransformer`.

## 🤖 Models Evaluated

-   Linear Regression
-   Ridge Regression
-   Lasso Regression
-   ElasticNet
-   K-Nearest Neighbors Regressor
-   Decision Tree Regressor
-   Random Forest Regressor
-   AdaBoost Regressor
-   Support Vector Regression
-   XGBoost Regressor
-   CatBoost Regressor

### Best Model

After model comparison and hyperparameter optimization using **Optuna**,
Support Vector Regression (SVR) produced the best performance.

Best hyperparameters obtained during experimentation:

``` python
{
    "C": 0.5173957150270933,
    "epsilon": 0.9481699343853931,
    "kernel": "linear",
    "gamma": "scale"
}
```

Performance achieved during experimentation:

-   **Test RMSE:** approximately `5.35`
-   **R² Score:** approximately `0.85`

## 🔄 Application Workflow

``` text
User Input
    ↓
React Frontend
    ↓
Flask REST API
    ↓
Prediction Pipeline
    ↓
Saved Preprocessor
    ↓
Trained SVR Model
    ↓
Predicted Math Score
    ↓
Result Displayed in React UI
```

## 💻 Tech Stack

### Machine Learning

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   Optuna
-   XGBoost
-   CatBoost

### Backend

-   Flask
-   Flask-CORS
-   Gunicorn

### Frontend

-   React
-   Vite
-   JavaScript
-   CSS

### Deployment

-   Render
-   GitHub

## 🚀 Running the Project Locally

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd ml_project
```

### 2. Create and activate a Python virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install backend dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start the Flask backend

``` bash
flask --app app.py --debug run
```

### 5. Install frontend dependencies

Open another terminal:

``` bash
cd frontend
npm install
```

### 6. Start the React development server

``` bash
npm run dev
```

Open the local URL provided by Vite in your browser.

## 📡 API Endpoint

### Predict Math Score

``` http
POST /predict
```

Example request:

``` json
{
    "gender": "female",
    "race_ethnicity": "group B",
    "parental_level_of_education": "some college",
    "lunch": "standard",
    "test_preparation_course": "none",
    "reading_score": "70",
    "writing_score": "70"
}
```

Example response:

``` json
{
    "results": 67.5
}
```

## 📚 What I Learned

Through this project, I worked with:

-   End-to-end Machine Learning project architecture
-   Exploratory Data Analysis
-   Feature preprocessing pipelines
-   Model comparison and evaluation
-   Hyperparameter optimization using Optuna
-   Model serialization
-   Custom prediction pipelines
-   Flask API development
-   React frontend development
-   Frontend and backend integration
-   CORS and API communication
-   Dependency management
-   Production deployment using Gunicorn and Render

## 🔮 Future Improvements

-   Automated testing
-   Dockerization
-   CI/CD workflows
-   Model monitoring
-   Prediction logging
-   Improved error handling
-   Model explainability using SHAP
-   Automated retraining pipelines


Built as an end-to-end Machine Learning project demonstrating the
complete journey from raw data to a deployed web application.
