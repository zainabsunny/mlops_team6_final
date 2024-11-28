# Databricks notebook source
# MAGIC %pip install ucimlrepo
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import mlflow
import datetime
import utils.data_utils as data_utils
import utils.model_utils as model_utils

# COMMAND ----------

# Ingest data & split into train/test
bike_df = data_utils.get_bike_data()
bike_train, bike_prod = data_utils.get_train_test_split(bike_df)

# COMMAND ----------

EXP_DIR = "/Users/forbug@uchicago.edu/databricks_automl"
EXP_NAME = f"mlops_final_{datetime.datetime.today()}"
EXP_PATH = f"{EXP_DIR}/{EXP_NAME}"

# COMMAND ----------

# Use AutoML to train an ML model - evaluate
# using R2 metric
model, model_uri, model_name = model_utils.run_model_train_pipeline(bike_train, 5, experiment_name=EXP_NAME)

# COMMAND ----------

mlflow.set_experiment(EXP_PATH)

# COMMAND ----------

# Run inference on the original test set
predictions, mse, r2 = model_utils.run_inference(model, bike_prod, run_name='original_test_run')

# COMMAND ----------

# Change the test dataset (2 features)
adjusted_bike_prod = data_utils.update_feature_data(bike_prod)

# COMMAND ----------

# Run inference on the changed test set
preds_changed, mse_changed, r2_changed = model_utils.run_inference(model, adjusted_bike_prod, run_name='changed_test_run')
