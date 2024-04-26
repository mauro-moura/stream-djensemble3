import core
from format.persist import save_in_database
import single_model, stream_ensemble

def perform_experiment(configuration, iteration, database_file):
    if configuration["label"] == "best_of_all":
        single_model.perform_single_model_experiment(configuration, iteration, database_file)
    elif configuration["label"] in ["average", "random"]:
        database_file = database_file[:-3] + f"-{configuration['label']}.db"
        stream_ensemble.perform_experiment(configuration, iteration, database_file)
    elif configuration["label"] in ["global"]:
        database_file = database_file[:-3] + f"-{configuration['label']}.db"
        configuration["models"]["convolutional_models_path"] = "input/models/cfsr/spatio-temporal/general/"
        configuration["models"]["temporal_models_path"] = "/"
        stream_ensemble.perform_experiment(configuration, iteration, database_file)
    