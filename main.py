import copy
import core.djensemble 
from core.config import Config
import copy
import logging
import sqlite3
import sys
import baseline, stream_ensemble
from format.config_parser import parse_dj_configurations
from format.persist import save_in_database

#CONFIG_FILE = "input/config/config.json"
CONFIG_FILE = "input/config/config-baseline.json"
MAX_ITERATIONS = 1

def run_configuration(configuration, iteration, database_file):
    if configuration["label"] in ["best_of_all", "global", "average", "random"]:
        baseline.perform_experiment(configuration, iteration, database_file)
    else:
        stream_ensemble.perform_experiment(configuration, iteration, database_file)        

def perform_experiment(config: Config, query_dict: dict = None):
    config = config.data
    if "queries" in config.keys():
        if query_dict is None:
            query_dict = Config(config["queries"]).data["queries"]
        queries = query_dict#Config(config["queries"]).data["queries"]
    for query_key, query in queries.items():
        for dj_key, _ in config["djensemble"].items():
            if dj_key in config["skip_list"]:
                continue
            configuration = parse_dj_configurations(query, config, dj_key)
            for it in range(MAX_ITERATIONS):
                database_file = f"{query_key}.db"
                copy_configuration = copy.deepcopy(configuration)
                run_configuration(copy_configuration, it, database_file)

if __name__ == "__main__":        
    #import json
    #query_dict = json.loads(sys.argv[1])    
    #perform_experiment(Config(CONFIG_FILE), query_dict)
    perform_experiment(Config(CONFIG_FILE))