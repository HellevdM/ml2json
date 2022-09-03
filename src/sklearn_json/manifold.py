# -*- coding: utf-8 -*-

import numpy as np
from sklearn.manifold import (Isomap, LocallyLinearEmbedding,
                              MDS, SpectralEmbedding, TSNE)
from sklearn.utils import check_random_state

from .decomposition import serialize_kernel_pca, deserialize_kernel_pca
from .neighbors import serialize_nearest_neighbors, deserialize_nearest_neighbors
from .utils.random_state import serialize_random_state, deserialize_random_state


def serialize_tsne(model):
    serialized_model = {
        'meta': 'tsne',
        'embedding_': model.embedding_.tolist(),
        'kl_divergence_': model.kl_divergence_,
        'n_features_in_': model.n_features_in_,
        'n_iter_': model.n_iter_,
        '_init': model._init,
        '_learning_rate': model._learning_rate,
        'params': model.get_params()
    }

    if 'feature_names_in_' in model.__dict__:
        serialized_model['feature_names_in_'] = model.feature_names_in_.tolist()

    return serialized_model


def deserialize_tsne(model_dict):
    model = TSNE(**model_dict['params'])

    model.embedding_ = np.array(model_dict['embedding_'])
    model.kl_divergence_ = model_dict['kl_divergence_']
    model.n_features_in_ = model_dict['n_features_in_']
    model.n_iter_ = model_dict['n_iter_']
    model._init = model_dict['_init']
    model._learning_rate = model_dict['_learning_rate']

    if 'feature_names_in_' in model_dict.keys():
        model.feature_names_in_ = np.array(model_dict['feature_names_in_'])

    return model

