import os
import sys
from dataclasses import dataclass

import optuna

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, root_mean_squared_error

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str = os.path.join('artifacts','model.pkl')
    n_trials:int = 100


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test,preprocessor):
        try:
            logging.info("Initiating model trainer")
            logging.info("Fetching the model list")
            model_configs = self.get_model_configs()

            logging.info("finding best results for all the models after using hyperparameter tuning")
            model_results  = self.finetuning(model_configs,X_train,y_train,X_test,y_test)

            logging.info("Finding the best model based on the best RMSE score")
            best_model_name = min(model_results,key=lambda x:model_results[x]["Best RMSE"])
            best_model = model_results[best_model_name]["Best Model"]

            pipeline = self.create_inference_pipeline(preprocessor,best_model)
            save_object(self.model_trainer_config.trained_model_file_path,pipeline)
            logging.info("Model trainer completed")

            return model_results[best_model_name]["Best RMSE"]

        except Exception as e:
            raise CustomException(e,sys)

    def build_params(self,trial,param_config):
        params = {}

        for param_name,config in param_config.items():
            suggest_method = getattr(
                trial,
                f"suggest_{config['suggest']}"
            )

            kwargs = {
                key:value
                for key,value in config.items()
                if key != "suggest"
            }

            params[param_name] = suggest_method(
                param_name,
                **kwargs
            )

        return params

    def create_inference_pipeline(self, preprocessor, model):
        return Pipeline(
            [
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

    def create_model(self,model_name,config,params):
        if model_name == "CatBoost":
            return config["model"](**params,verbose=0,random_state=42)
        if model_name == "XGBoost":
            return config["model"](**params,verbosity=0,random_state=42)
        if model_name in ["Decision Tree","Random Forest","AdaBoost"]:
            return config["model"](**params,random_state=42)

        return config["model"](**params)

    def finetuning(self,list_models,X_train,y_train,X_val,y_val):
        results = {}
        for model_name,config in list_models.items():
            logging.info(f"Tuning {model_name}")
            def objective(trial):
                params = self.build_params(trial,config["params"])
                model = self.create_model(model_name,config,params)
                model.fit(X_train,y_train)
                prediction = model.predict(X_val)

                return root_mean_squared_error(y_val,prediction)

            study = optuna.create_study(direction="minimize")
            study.optimize(objective,n_trials=self.model_trainer_config.n_trials,show_progress_bar=True)

            best_model = self.create_model(model_name,config,study.best_params)
            best_model.fit(X_train,y_train)
            prediction = best_model.predict(X_val)

            results[model_name] = {
                "Best Model":best_model,
                "Best RMSE":root_mean_squared_error(y_val,prediction),
                "Best R2":r2_score(y_val,prediction),
                "Best Parameters":study.best_params
            }

            logging.info(f"{model_name} tuning completed")
        return results

    def get_model_configs(self):
        model_configs = {
            "Linear Regression": {
                "model": LinearRegression,
                "params": {}
            },
            "Ridge": {
                "model": Ridge,
                "params": {
                    "alpha": {
                        "suggest": "float",
                        "low": 1e-4,
                        "high": 100,
                        "log": True
                    }
                }
            },
            "Lasso": {
                "model": Lasso,
                "params": {
                    "alpha": {
                        "suggest": "float",
                        "low": 1e-4,
                        "high": 10,
                        "log": True
                    }
                }
            },
            "ElasticNet": {
                "model": ElasticNet,
                "params": {
                    "alpha": {
                        "suggest": "float",
                        "low": 1e-4,
                        "high": 10,
                        "log": True
                    },
                    "l1_ratio": {
                        "suggest": "float",
                        "low": 0.0,
                        "high": 1.0
                    }
                }
            },
            "Decision Tree": {
                "model": DecisionTreeRegressor,
                "params": {
                    "criterion": {
                        "suggest": "categorical",
                        "choices": ["squared_error", "friedman_mse", "absolute_error"]
                    },
                    "max_depth": {
                        "suggest": "int",
                        "low": 2,
                        "high": 30
                    },
                    "min_samples_split": {
                        "suggest": "int",
                        "low": 2,
                        "high": 20
                    },
                    "min_samples_leaf": {
                        "suggest": "int",
                        "low": 1,
                        "high": 10
                    }
                }
            },
            "Random Forest": {
                "model": RandomForestRegressor,
                "params": {
                    "n_estimators": {
                        "suggest": "int",
                        "low": 100,
                        "high": 500
                    },
                    "max_depth": {
                        "suggest": "int",
                        "low": 3,
                        "high": 30
                    },
                    "min_samples_split": {
                        "suggest": "int",
                        "low": 2,
                        "high": 20
                    },
                    "min_samples_leaf": {
                        "suggest": "int",
                        "low": 1,
                        "high": 10
                    },
                    "max_features": {
                        "suggest": "categorical",
                        "choices": ["sqrt", "log2", None]
                    }
                }
            },
            "KNN": {
                "model": KNeighborsRegressor,
                "params": {
                    "n_neighbors": {
                        "suggest": "int",
                        "low": 2,
                        "high": 30
                    },
                    "weights": {
                        "suggest": "categorical",
                        "choices": ["uniform", "distance"]
                    },
                    "p": {
                        "suggest": "int",
                        "low": 1,
                        "high": 2
                    }
                }
            },
            "SVR": {
                "model": SVR,
                "params": {
                    "C": {
                        "suggest": "float",
                        "low": 1e-2,
                        "high": 100,
                        "log": True
                    },
                    "epsilon": {
                        "suggest": "float",
                        "low": 1e-3,
                        "high": 1.0,
                        "log": True
                    },
                    "kernel": {
                        "suggest": "categorical",
                        "choices": ["linear", "rbf", "poly"]
                    },
                    "gamma": {
                        "suggest": "categorical",
                        "choices": ["scale", "auto"]
                    }
                }
            },
            "AdaBoost": {
                "model": AdaBoostRegressor,
                "params": {
                    "n_estimators": {
                        "suggest": "int",
                        "low": 50,
                        "high": 500
                    },
                    "learning_rate": {
                        "suggest": "float",
                        "low": 1e-3,
                        "high": 1.0,
                        "log": True
                    },
                    "loss": {
                        "suggest": "categorical",
                        "choices": ["linear", "square", "exponential"]
                    }
                }
            },
            "XGBoost": {
                "model": XGBRegressor,
                "params": {
                    "n_estimators": {
                        "suggest": "int",
                        "low": 100,
                        "high": 500
                    },
                    "learning_rate": {
                        "suggest": "float",
                        "low": 1e-3,
                        "high": 0.3,
                        "log": True
                    },
                    "max_depth": {
                        "suggest": "int",
                        "low": 3,
                        "high": 12
                    },
                    "subsample": {
                        "suggest": "float",
                        "low": 0.5,
                        "high": 1.0
                    },
                    "colsample_bytree": {
                        "suggest": "float",
                        "low": 0.5,
                        "high": 1.0
                    },
                    "gamma": {
                        "suggest": "float",
                        "low": 0,
                        "high": 5
                    }
                }
            },
            "CatBoost": {
                "model": CatBoostRegressor,
                "params": {
                    "iterations": {
                        "suggest": "int",
                        "low": 100,
                        "high": 500
                    },
                    "learning_rate": {
                        "suggest": "float",
                        "low": 1e-3,
                        "high": 0.3,
                        "log": True
                    },
                    "depth": {
                        "suggest": "int",
                        "low": 4,
                        "high": 10
                    },
                    "l2_leaf_reg": {
                        "suggest": "float",
                        "low": 1,
                        "high": 10
                    }
                }
            }
        }
        return model_configs