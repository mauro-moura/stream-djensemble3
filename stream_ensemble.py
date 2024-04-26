import core
from format.persist import save_in_database

def perform_experiment(configuration, iteration, database_file):
    djensemble = core.djensemble.DJEnsemble(configuration)
    print(djensemble.get_parameters())
    djensemble.run()
    print(djensemble.get_statistics())
    print("---"*10)
    save_in_database(configuration, iteration, djensemble, database_file)