import argparse


import utils.data_utils as data_utils
import utils.model_utils as model_utils




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-max_automl_runtime', type=int, default=30)
    args = parser.parse_args()

    # Ingest data & split into train/test
    bike_df = data_utils.get_bike_data()
    bike_train, bike_prod = data_utils.get_train_test_split(bike_df)

    # Use AutoML to train an ML model - evaluate
    # using R2 metric
    model, model_uri, model_name = model_utils.run_model_train_pipeline(bike_train, args.max_automl_runtime)

    # Deploy the model (how??)


    # Set up model monitoring


    # 






