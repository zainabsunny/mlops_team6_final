import datetime
import mlflow
import utils.data_utils as data_utils

from databricks import automl

def run_model_train_pipeline(train_df, timeout=5):

    summary = automl.regress(train_df, target_col="cnt", timeout_minutes=timeout)
    
    print("*******Summary of Databricks AutoML Results*******")
    print(summary)

    model_uri = summary.best_trial.model_path
    model_name = f"best-automl-model-{datetime.now().date()}"
    registered_model_version = mlflow.register_model(model_uri, model_name)

    model = mlflow.pyfunc.load_model(model_uri)

    return model, model_uri, model_name


def deploy_model(model):

    pass