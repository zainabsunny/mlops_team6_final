import datetime
import mlflow
import utils.data_utils as data_utils

from databricks import automl
from sklearn.metrics import mean_squared_error, r2_score

def run_model_train_pipeline(train_df, timeout=5):

    summary = automl.regress(train_df, target_col="cnt", timeout_minutes=timeout)
    
    print("*******Summary of Databricks AutoML Results*******")
    print(summary)

    model_uri = summary.best_trial.model_path
    model_name = f"best-automl-model-{datetime.datetime.now().date()}"
    registered_model_version = mlflow.register_model(model_uri, model_name)

    model = mlflow.pyfunc.load_model(model_uri)

    return model, model_uri, model_name
    

def run_inference(model, test_df, run_name):
    X_test, y_test = data_utils.get_x_y_split(test_df)

    with mlflow.start_run(run_name=run_name):
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        # mlflow.log_param('n_estimators', n_estimators)
        mlflow.log_metric('mse', mse)
        mlflow.log_metric('r2', r2)

    return predictions, mse, r2