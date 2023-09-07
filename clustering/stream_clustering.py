import numpy as np
import clustering.embedding as embedding
from sklearn.cluster import Birch
from sklearn.metrics import silhouette_score
import logging
import core.view as view

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StreamClustering():
    def __init__(self, embedding_method, 
                 clustering_algorithm = "birch", n_clusters=[6]):
        self._number_of_clusters = n_clusters[0]
        self.birch = Birch(branching_factor=35, n_clusters=self._number_of_clusters, threshold=30)
        self.embedding_method = embedding_method
        self.embedding_strategy = None
        self.clustering_frame = None

    def initialize_clustering(self, dataset: np.ndarray):
        self.ds_shape = dataset.shape
        self.embedding_strategy = embedding.create_embedding_strategy(
            dataset, self.embedding_method)
        return self.update_clustering(dataset)

    def update_clustering(self, dataset):
        self.emb_list = self.embedding_strategy.iterate(dataset)
        embedding.normalize_embedding_list(self.emb_list)
        self.clustering = self._cluster_using_birch(self.emb_list)        
        if len(set(self.clustering)) == 1:
            self.clustering[0] = 1 if self.clustering[0] == 0 else 0
        self.clustering = np.reshape(self.clustering, self.ds_shape[1:])

    def get_silhouette(self):
        # The number of labels must be different of the number of samples
        clustering_flattened = self.clustering.flatten()
        if len(set(clustering_flattened)) == len(clustering_flattened):
            self.clustering[0, 0] = self.clustering[0, 1]

        silhouette = silhouette_score(self.emb_list, self.clustering.flatten())
        return silhouette

    def save_clustering_image(self, file_dir, file_name):
        if file_dir[-1] != "/":
            file_dir += "/"
        view.save_figure_from_matrix(self.clustering, file_dir, file_name)

    @property
    def number_of_clusters(self):
        return self._number_of_clusters

    @property
    def embedding_time(self):
        self._check_clustering()
        return self._embedding_time

    @property
    def clustering_time(self):
        self._check_clustering()
        return self._clustering_time    

    def _cluster_using_birch(self, clustering_items: np.array):
        self.birch = self.birch.partial_fit(clustering_items)
        clustering = self.birch.predict(clustering_items)
        return clustering

    def get_clustering(self):
        try:
            assert(type(self.clustering) != type(None))
        except:
            raise("Clustering Strategy Error: Clustering strategy not initialized")
        return self.clustering
