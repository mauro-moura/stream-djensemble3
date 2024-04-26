import core.djensemble 
from core.config import Config
import logging
import sqlite3
import core.utils as ut
import os, shutil
from format.persist import save_in_database

def perform_experiment(configuration, it_number, database_file_name):
    djensemble = core.djensemble.DJEnsemble(configuration)
    print(djensemble.get_parameters())
    djensemble.run()
    print(djensemble.get_statistics())
    print("---"*10)    
    save_in_database(configuration, it_number, djensemble, database_file_name)


def create_directory_with_single_model(model, dir, directory_sufix):
    files_list = ut.list_all_files_in_dir(dir, prefix=model)
    new_dir_name = f"tmp-{model}-{directory_sufix}/"
    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)

    for file in files_list:
        shutil.copy2(dir + file, new_dir_name + file)
    return new_dir_name
    

def perform_single_model_experiment(configuration, it_number, database_file):
    temporal_models_path = configuration["models"]["temporal_models_path"]
    convolutional_models_path = configuration["models"]["convolutional_models_path"]
    strategy = configuration["config"]
    temporal_models = ut.get_names_of_models_in_dir(temporal_models_path)
    convolutional_models = ut.get_names_of_models_in_dir(convolutional_models_path)

    for model in temporal_models:
        stem_file_name = ut.get_file_name_without_extension(database_file)
        temp_directory = create_directory_with_single_model(model, temporal_models_path, directory_sufix=stem_file_name)
        configuration["models"]["temporal_models_path"] = temp_directory
        configuration["models"]["convolutional_models_path"] = "/"                
        ut.create_directory_if_not_exists(f"{stem_file_name}/")        
        ut.create_directory_if_not_exists(f"output/{strategy}/")        
        database_file_name = f"output/{strategy}/{stem_file_name}-{strategy}.db"
        configuration["config"] = model
        perform_experiment(configuration, it_number, database_file_name=database_file_name)
        ut.remove_directory(temp_directory)

    for model in convolutional_models:
        stem_file_name = ut.get_file_name_without_extension(database_file)
        temp_directory = create_directory_with_single_model(model, convolutional_models_path, directory_sufix=stem_file_name)
        configuration["models"]["temporal_models_path"] = "/"
        configuration["models"]["convolutional_models_path"] = temp_directory
        ut.create_directory_if_not_exists(f"{stem_file_name}/")        
        ut.create_directory_if_not_exists(f"output/{strategy}/")        
        database_file_name = f"output/{strategy}/{stem_file_name}-{strategy}.db"
        configuration["config"] = model        
        perform_experiment(configuration, it_number, database_file_name=database_file_name)
        ut.remove_directory(temp_directory)