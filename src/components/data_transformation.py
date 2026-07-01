import sys
from dataclasses import dataclass
import os

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.utils import save_object

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_cols = ['writing score','reading score']
            categorical_cols = ['gender','race/ethnicity','parental level of education','lunch','test preparation course']

            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('onehot',OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            logging.info("Created data transformer object")

            preprocessor = ColumnTransformer(
                [
                    ('num',num_pipeline,numerical_cols),
                    ('cat',cat_pipeline,categorical_cols)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info("Read train and test data")
            logging.info("Obtaining preprocessing object")
            preprocessor = self.get_data_transformer_object()
            target_feature = 'math score'

            input_features_train = train_data.drop(columns=[target_feature])
            target_feature_train = train_data[target_feature]

            input_features_test = test_data.drop(columns=[target_feature])
            target_feature_test = test_data[target_feature]

            logging.info("Fitting data using preprocessing object")
            input_features_train = preprocessor.fit_transform(input_features_train)
            input_features_test = preprocessor.transform(input_features_test)

            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessor
            )

            return (input_features_train,target_feature_train,input_features_test,target_feature_test,preprocessor)
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    obj = DataTransformation()
    obj.initiate_data_transformation(
        'artifacts/train.csv',
        'artifacts/test.csv'
    )