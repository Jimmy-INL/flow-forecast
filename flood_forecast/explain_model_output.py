from typing import Dict
import shap
import torch
from flood_forecast.preprocessing.pytorch_loaders import CSVTestLoader
from datetime import datetime
import numpy as np


def deep_explain_model_summary_plot(
    model,
    datetime_start: datetime = datetime(2014, 6, 1, 0),
    test_csv_path: str = None,
    hours_to_forecast: int = 336,
    dataset_params: Dict = {},
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_features = len(model.params['dataset_params']['relevant_cols'])  
    # If the test dataframe is none use default one supplied in params
    if test_csv_path is None:
        csv_test_loader = model.test_data
    else:
        csv_test_loader = CSVTestLoader(
            test_csv_path,
            hours_to_forecast,
            **dataset_params,
            interpolate=dataset_params["interpolate_param"]
        )
    background_data = csv_test_loader.original_df
    background_batches = csv_test_loader.convert_real_batches(
        csv_test_loader.df.columns, background_data
        )
    # TODO - better stratagy to choose background data
    background_tensor = torch.stack(background_batches[:-1]).float().to(device)
    model.model.eval()

    # background shape (L, N, M)
    # L - batch size, N - history length, M - feature size
    # to_explain = history.to(device).unsqueeze(0)
    deep_explainer = shap.DeepExplainer(model.model, background_tensor)
    shap_values = deep_explainer.shap_values(background_tensor)

    # summary plot shows overall feature ranking 
    # by average absolute shap values
    mean_shap_values = np.concatenate(shap_values).mean(axis=0)
    shap.summary_plot(
        mean_shap_values,
        to_explain.cpu().numpy().reshape(-1, num_features),
        feature_names=csv_test_loader.df.columns,
        plot_type="bar",
    )
    shap.summary_plot(
        mean_shap_values,
        to_explain.cpu().numpy().reshape(-1, num_features),
        feature_names=csv_test_loader.df.columns,
    )

def deep_explain_model_sample():
    # TODO
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # num_features = len(model.params['dataset_params']['relevant_cols'])
    
    # if type(datetime_start) == str:
    #     datetime_start = datetime.strptime(datetime_start, "%Y-%m-%d")
    # # If the test dataframe is none use default one supplied in params
    # if test_csv_path is None:
    #     csv_test_loader = model.test_data
    # else:
    #     csv_test_loader = CSVTestLoader(
    #         test_csv_path,
    #         hours_to_forecast,
    #         **dataset_params,
    #         interpolate=dataset_params["interpolate_param"]
    #     )
    # # history, forecast_total_df, forecast_start_idx = csv_test_loader.get_from_start_date(datetime_start)
    # background_data = csv_test_loader.original_df
    # background_batches = csv_test_loader.convert_real_batches(
    #     csv_test_loader.df.columns, background_data
    #     )
    # # TODO - better stratagy to choose background data
    # background_tensor = torch.stack(background_batches[:-1]).float().to(device)
    # model.model.eval()
    # force plot for a simgle sample (in matplotlib)
    # shap.force_plot(
    #     deep_explainer.expected_value[0],
    #     shap_values[0].reshape(-1, 3)[6, :],
    #     show=True,
    #     feature_names=csv_test_loader.df.columns,
    #     matplotlib=True,
    # )
    # # force plot for multiple time-steps
    # # can only be generated as html objects
    # # shap.force_plot(e.expected_value[0], shap_values[0].reshape(-1, 3), show=True, feature_names=csv_test_loader.df.columns)
    # # dependece plot shows feature value vs shap value
    # shap.dependence_plot(
    #     2,
    #     shap_values[0].reshape(-1, 3),
    #     to_explain.cpu().numpy().reshape(-1, 3),
    #     interaction_index=0,
    #     feature_names=csv_test_loader.df.columns,
    # )