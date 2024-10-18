
# Contents

- Instructions
- Configuration Files

# 

Python version: 3.9

1. Download repo
2. Create env
3. Install requirements
4. Dataset should be in `input/data`
5. If new models will be used, put in `input/models`
6. 


Para rodar `python main.py`

# Configuration Files

## config.json

Passa o config.json no main do projeto

```python
{   
    "queries": "input/config/queries/queries-2015.json", # O arquivo com a query que vai ser executada
    # Indice de qual experimento da lista djensemble que vai executar, se vazio, executa todos
    # ["E", "F"] executaria apenas o A, B, C, D.
    "skip_list": [], 
    "database_file": "exp.db", # Local de saída dos dados
    "global_configuration": { # Essas configurações sobrepõe o djesemble, se houve coincidência.
        "use_random_allocation": false, # Alocar modelos aleatório ao invés do djensemble
        "use_average_ensemble": false, # Ensemble de modelos
        "data_source": { # 
            "dataset": "input/data/CFSR-2015.nc",
            "target_attribute": "TMP_L100",
            "subregion": { # Indices da grade, para ter a liberdade de reduzir tamanho do DS
                "lat_min": 0,
                "lat_max": 141,
                "lon_min": 0,
                "lon_max": 153
            },
            "time_range": [0, 1460], # Indice das janelas de início e fim
            "compacting_factor": 1 # Gera uma visão resumida do dataset, se = 10 pula de 10 em 10 pontos do dataset
        },
        "models": {
            # Um dos dois podem ser vazios
            "convolutional_models_path": "input/models/cfsr/spatio-temporal/all-models/",
            "temporal_models_path": "input/models/cfsr/temporal/all-models/",
            "cost_estimation_function": { # Parâmetros da learning function
                "noise_level": 50,
                "always_update": false
            }                
        }    
    },    
    "djensemble" : { # Configurações de experimento, cada arquivo é uma execução
        "A": "input/config/configuration/A.json",
        "B": "input/config/configuration/B.json",
        "C": "input/config/configuration/C.json",
        "D": "input/config/configuration/D.json",
        "E": "input/config/configuration/E.json",
        "F": "input/config/configuration/F.json"
    }
}
```

There is a global-baseline config file.

Query
```python
{
    "queries":{
        # Define as regiões de uma grid
        # start e end são cordenadas de pixel start é o ponto superior esquedo x, y 
        # end é o ponto inferior direito
        "Q1-2013": {"start": [39, 2], "end": [58, 21]},
        "Q2-2013": {"start": [121, 10], "end": [140, 29]},
        "Q3-2013": {"start": [34, 46], "end": [53, 65]},
        "Q4-2013": {"start": [100, 48], "end": [119, 67]},
        "Q5-2013": {"start": [85, 88], "end": [104, 107]},
        "Q6-2013": {"start": [8, 109], "end": [27, 128]},
        "Q7-2013": {"start": [116, 110], "end": [135, 129]}
    }
}
```

## A.json

This configuration file is located at `input/config/configuration/A.json`
and its used for configurate the experiments.

```python
{
    "label": "A",
    "window_size": 10,
    "window_type": "tumbling",
    # Até que ponto do dataset você quer executar
    "time_start": 0, # Indice da primeira janela
    "time_end": 1460, # Indice da última janela
    "clustering":{
        "embedding_method": "parcorr6",
        "type": "stream",
        "cluster_query_window": true, # Escolher se vai clusterizar apenas a janela ou todo o frame
        "pre_clustering_window_size": 10 # A primeira clusterização feita, pode ter um tamanho maior.
    },
    "tiling": {
        "strategy": "yolo", # Can be "yolo" or "quadtree"
        "min_purity_rate": 0.80 # Percentual de séries do cluster majoritário.
    }
}
```
