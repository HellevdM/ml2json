# -*- coding: utf-8 -*-

import os

import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, _gb_losses
from sklearn.neural_network import MLPRegressor
from sklearn.tree._tree import Tree
from sklearn.svm import SVR
from sklearn import dummy
from xgboost import XGBRegressor, XGBRFRegressor, XGBRanker
from lightgbm import LGBMRegressor, LGBMRanker, Booster as LGBMBooster

from . import csr


def serialize_linear_regressor(model):
    serialized_model = {
        'meta': 'linear-regression',
        'coef_': model.coef_.tolist(),
        'intercept_': model.intercept_.tolist(),
        'params': model.get_params()
    }

    return serialized_model


def deserialize_linear_regressor(model_dict):
    model = LinearRegression(**model_dict['params'])

    model.coef_ = np.array(model_dict['coef_'])
    model.intercept_ = np.array(model_dict['intercept_'])

    return model


def serialize_lasso_regressor(model):
    serialized_model = {
        'meta': 'lasso-regression',
        'coef_': model.coef_.tolist(),
        'params': model.get_params()
    }

    if isinstance(model.n_iter_, int):
        serialized_model['n_iter_'] = model.n_iter_
    else:
        serialized_model['n_iter_'] = model.n_iter_.tolist()

    if isinstance(model.n_iter_, float):
        serialized_model['intercept_'] = model.intercept_
    else:
        serialized_model['intercept_'] = model.intercept_.tolist()

    return serialized_model


def deserialize_lasso_regressor(model_dict):
    model = Lasso(model_dict['params'])

    model.coef_ = np.array(model_dict['coef_'])

    if isinstance(model_dict['n_iter_'], list):
        model.n_iter_ = np.array(model_dict['n_iter_'])
    else:
        model.n_iter_ = int(model_dict['n_iter_'])

    if isinstance(model_dict['intercept_'], list):
        model.intercept_ = np.array(model_dict['intercept_'])
    else:
        model.intercept_ = float(model_dict['intercept_'])

    return model


def serialize_elastic_regressor(model):
    serialized_model = {
        'meta': 'elasticnet-regression',
        'coef_': model.coef_.tolist(),
        'alpha': model.alpha,
        'params': model.get_params()
    }
    if isinstance(model.n_iter_, int):
        serialized_model['n_iter_'] = model.n_iter_
    else:
        serialized_model['n_iter_'] = model.n_iter_.tolist()
    if isinstance(model.intercept_, float):
        serialized_model['intercept_'] = model.intercept_
    else:
        serialized_model['intercept_'] = model.intercept_.tolist()

    return serialized_model


def deserialize_elastic_regressor(model_dict):
    model = ElasticNet(model_dict['params'])

    model.coef_ = np.array(model_dict['coef_'])
    model.alpha = np.array(model_dict['alpha'])

    if isinstance(model_dict['n_iter_'], list):
        model.n_iter_ = np.array(model_dict['n_iter_'])
    else:
        model.n_iter_ = int(model_dict['n_iter_'])
    if isinstance(model_dict['intercept_'], list):
        model.intercept_ = np.array(model_dict['intercept_'])
    else:
        model.intercept_ = float(model_dict['intercept_'])
    return model


def serialize_ridge_regressor(model):
    serialized_model = {
        'meta': 'ridge-regression',
        'coef_': model.coef_.tolist(),
        'params': model.get_params()
    }

    if model.n_iter_:
        serialized_model['n_iter_'] = model.n_iter_.tolist()

    if isinstance(model.n_iter_, float):
        serialized_model['intercept_'] = model.intercept_
    else:
        serialized_model['intercept_'] = model.intercept_.tolist()

    return serialized_model


def deserialize_ridge_regressor(model_dict):
    model = Ridge(model_dict['params'])

    model.coef_ = np.array(model_dict['coef_'])

    if 'n_iter_' in model_dict:
        model.n_iter_ = np.array(model_dict['n_iter_'])

    if isinstance(model_dict['intercept_'], list):
        model.intercept_ = np.array(model_dict['intercept_'])
    else:
        model.intercept_ = float(model_dict['intercept_'])

    return model


def serialize_svr(model):
    serialized_model = {
        'meta': 'svr',
        'class_weight_': model.class_weight_.tolist(),
        'support_': model.support_.tolist(),
        '_n_support': model._n_support.tolist(),
        'intercept_': model.intercept_.tolist(),
        '_probA': model._probA.tolist(),
        '_probB': model._probB.tolist(),
        '_intercept_': model._intercept_.tolist(),
        'shape_fit_': model.shape_fit_,
        '_gamma': model._gamma,
        'params': model.get_params()
    }

    if isinstance(model.support_vectors_, sp.sparse.csr_matrix):
        serialized_model['support_vectors_'] = csr.serialize_csr_matrix(model.support_vectors_)
    elif isinstance(model.support_vectors_, np.ndarray):
        serialized_model['support_vectors_'] = model.support_vectors_.tolist()

    if isinstance(model.dual_coef_, sp.sparse.csr_matrix):
        serialized_model['dual_coef_'] = csr.serialize_csr_matrix(model.dual_coef_)
    elif isinstance(model.dual_coef_, np.ndarray):
        serialized_model['dual_coef_'] = model.dual_coef_.tolist()

    if isinstance(model._dual_coef_, sp.sparse.csr_matrix):
        serialized_model['_dual_coef_'] = csr.serialize_csr_matrix(model._dual_coef_)
    elif isinstance(model._dual_coef_, np.ndarray):
        serialized_model['_dual_coef_'] = model._dual_coef_.tolist()

    return serialized_model


def deserialize_svr(model_dict):
    model = SVR(**model_dict['params'])
    model.shape_fit_ = model_dict['shape_fit_']
    model._gamma = model_dict['_gamma']

    model.class_weight_ = np.array(model_dict['class_weight_']).astype(np.float64)
    model.support_ = np.array(model_dict['support_']).astype(np.int32)
    model._n_support = np.array(model_dict['_n_support']).astype(np.int32)
    model.intercept_ = np.array(model_dict['intercept_']).astype(np.float64)
    model._probA = np.array(model_dict['_probA']).astype(np.float64)
    model._probB = np.array(model_dict['_probB']).astype(np.float64)
    model._intercept_ = np.array(model_dict['_intercept_']).astype(np.float64)

    if 'meta' in model_dict['support_vectors_'] and model_dict['support_vectors_']['meta'] == 'csr':
        model.support_vectors_ = csr.deserialize_csr_matrix(model_dict['support_vectors_'])
        model._sparse = True
    else:
        model.support_vectors_ = np.array(model_dict['support_vectors_']).astype(np.float64)
        model._sparse = False

    if 'meta' in model_dict['dual_coef_'] and model_dict['dual_coef_']['meta'] == 'csr':
        model.dual_coef_ = csr.deserialize_csr_matrix(model_dict['dual_coef_'])
    else:
        model.dual_coef_ = np.array(model_dict['dual_coef_']).astype(np.float64)

    if 'meta' in model_dict['_dual_coef_'] and model_dict['_dual_coef_']['meta'] == 'csr':
        model._dual_coef_ = csr.deserialize_csr_matrix(model_dict['_dual_coef_'])
    else:
        model._dual_coef_ = np.array(model_dict['_dual_coef_']).astype(np.float64)

    return model


def serialize_tree(tree):
    serialized_tree = tree.__getstate__()
    # serialized_tree['nodes_dtype'] = serialized_tree['nodes'].dtype
    dtypes = serialized_tree['nodes'].dtype
    serialized_tree['nodes'] = serialized_tree['nodes'].tolist()
    serialized_tree['values'] = serialized_tree['values'].tolist()

    return serialized_tree, dtypes


def deserialize_tree(tree_dict, n_features, n_classes, n_outputs):
    tree_dict['nodes'] = [tuple(lst) for lst in tree_dict['nodes']]

    names = ['left_child', 'right_child', 'feature', 'threshold', 'impurity', 'n_node_samples', 'weighted_n_node_samples']
    tree_dict['nodes'] = np.array(tree_dict['nodes'], dtype=np.dtype({'names': names, 'formats': tree_dict['nodes_dtype']}))
    tree_dict['values'] = np.array(tree_dict['values'])

    tree = Tree(n_features, np.array([n_classes], dtype=np.intp), n_outputs)
    tree.__setstate__(tree_dict)

    return tree


def serialize_decision_tree_regressor(model):
    tree, dtypes = serialize_tree(model.tree_)
    serialized_model = {
        'meta': 'decision-tree-regression',
        'feature_importances_': model.feature_importances_.tolist(),
        'max_features_': model.max_features_,
        'n_features_in_': model.n_features_in_,
        'n_outputs_': model.n_outputs_,
        'tree_': tree
    }

    # serialized_model.

    tree_dtypes = []
    for i in range(0, len(dtypes)):
        tree_dtypes.append(dtypes[i].str)

    serialized_model['tree_']['nodes_dtype'] = tree_dtypes

    return serialized_model


def deserialize_decision_tree_regressor(model_dict):
    deserialized_decision_tree = DecisionTreeRegressor()

    deserialized_decision_tree.max_features_ = model_dict['max_features_']
    deserialized_decision_tree.n_features_in_ = model_dict['n_features_in_']
    deserialized_decision_tree.n_outputs_ = model_dict['n_outputs_']

    tree = deserialize_tree(model_dict['tree_'], model_dict['n_features_in_'], 1, model_dict['n_outputs_'])
    deserialized_decision_tree.tree_ = tree

    return deserialized_decision_tree


def serialize_dummy_regressor(model):
    model.constant = model.constant_.tolist()
    return model.__dict__


def serialize_gradient_boosting_regressor(model):

    serialized_model = {
        'meta': 'gb-regression',
        'max_features_': model.max_features_,
        'n_features_in_': model.n_features_in_,
        'train_score_': model.train_score_.tolist(),
        'params': model.get_params(),
        'estimators_shape': list(model.estimators_.shape),
        'estimators_': []
    }

    if  isinstance(model.init_, dummy.DummyRegressor):
        serialized_model['init_'] = serialize_dummy_regressor(model.init_)
        serialized_model['init_']['meta'] = 'dummy'
    elif isinstance(model.init_, str):
        serialized_model['init_'] = model.init_

    if isinstance(model._loss, _gb_losses.LeastSquaresError):
        serialized_model['_loss'] = 'ls'
    elif isinstance(model._loss, _gb_losses.LeastAbsoluteError):
        serialized_model['_loss'] = 'lad'
    elif isinstance(model._loss, _gb_losses.HuberLossFunction):
        serialized_model['_loss'] = 'huber'
    elif isinstance(model._loss, _gb_losses.QuantileLossFunction):
        serialized_model['_loss'] = 'quantile'

    if 'priors' in model.init_.__dict__:
        serialized_model['priors'] = model.init_.priors.tolist()

    for tree in model.estimators_.reshape((-1,)):
        serialized_model['estimators_'].append(serialize_decision_tree_regressor(tree))
    return serialized_model


def deserialize_gradient_boosting_regressor(model_dict):
    model = GradientBoostingRegressor(**model_dict['params'])
    trees = [deserialize_decision_tree_regressor(tree) for tree in model_dict['estimators_']]
    model.estimators_ = np.array(trees).reshape(model_dict['estimators_shape'])
    if 'init_' in model_dict and model_dict['init_']['meta'] == 'dummy':
        model.init_ = dummy.DummyRegressor()
        model.init_.__dict__ = model_dict['init_']
        model.init_.__dict__.pop('meta')


    model.train_score_ = np.array(model_dict['train_score_'])
    model.max_features_ = model_dict['max_features_']
    model.n_features_in_ = model_dict['n_features_in_']
    if model_dict['_loss'] == 'ls':
        model._loss = _gb_losses.LeastSquaresError()
    elif model_dict['_loss'] == 'lad':
        model._loss = _gb_losses.LeastAbsoluteError()
    elif model_dict['_loss'] == 'huber':
        model._loss = _gb_losses.HuberLossFunction(1)
    elif model_dict['_loss'] == 'quantile':
        model._loss = _gb_losses.QuantileLossFunction(1)

    if 'priors' in model_dict:
        model.init_.priors = np.array(model_dict['priors'])
    return model


def serialize_random_forest_regressor(model):

    serialized_model = {
        'meta': 'rf-regression',
        'estimators_': [serialize_decision_tree_regressor(decision_tree) for decision_tree in model.estimators_],
        'n_features_in_': model.n_features_in_,
        'n_outputs_': model.n_outputs_,
        'params': model.get_params()
    }

    if 'oob_score_' in model.__dict__:
        serialized_model['oob_score_'] = model.oob_score_
    if 'oob_decision_function_' in model.__dict__:
        serialized_model['oob_prediction_'] = model.oob_prediction_.tolist()
    if 'feature_names_in' in model.__dict__:
        serialized_model['feature_names_in'] = model.feature_names_in.tolist(),

    return serialized_model


def deserialize_random_forest_regressor(model_dict):
    model = RandomForestRegressor(**model_dict['params'])
    estimators = [deserialize_decision_tree_regressor(decision_tree) for decision_tree in model_dict['estimators_']]
    model.estimators_ = np.array(estimators)

    model.n_features_in_ = model_dict['n_features_in_']
    model.n_outputs_ = model_dict['n_outputs_']
    # model.max_depth = model_dict['max_depth']
    # model.min_samples_split = model_dict['min_samples_split']
    # model.min_samples_leaf = model_dict['min_samples_leaf']
    # model.min_weight_fraction_leaf = model_dict['min_weight_fraction_leaf']
    # model.max_features = model_dict['max_features']
    # model.max_leaf_nodes = model_dict['max_leaf_nodes']
    # model.min_impurity_decrease = model_dict['min_impurity_decrease']
    # model.min_impurity_split = model_dict['min_impurity_split']

    if 'oob_score_' in model_dict:
        model.oob_score_ = model_dict['oob_score_']
    if 'oob_prediction_' in model_dict:
        model.oob_prediction_ =np.array(model_dict['oob_prediction_'])

    return model


def serialize_mlp_regressor(model):
    serialized_model = {
        'meta': 'mlp-regression',
        'coefs_': model.coefs_,
        'loss_': model.loss_,
        'intercepts_': model.intercepts_,
        'n_iter_': model.n_iter_,
        'n_layers_': model.n_layers_,
        'n_outputs_': model.n_outputs_,
        'out_activation_': model.out_activation_,
        'params': model.get_params()
    }

    return serialized_model


def deserialize_mlp_regressor(model_dict):
    model = MLPRegressor(**model_dict['params'])

    model.coefs_ = model_dict['coefs_']
    model.loss_ = model_dict['loss_']
    model.intercepts_ = model_dict['intercepts_']
    model.n_iter_ = model_dict['n_iter_']
    model.n_layers_ = model_dict['n_layers_']
    model.n_outputs_ = model_dict['n_outputs_']
    model.out_activation_ = model_dict['out_activation_']

    return model


def serialize_xgboost_ranker(model):
    serialized_model = {
        'meta': 'xgboost-ranker',
        'params': model.get_params()
    }

    model.save_model('model.json')
    with open('model.json', 'r') as fh:
        serialized_model['advanced-params'] = fh.read()
    os.remove('model.json')

    return serialized_model


def deserialize_xgboost_ranker(model_dict):
    model = XGBRanker(**model_dict['params'])

    with open('model.json', 'w') as fh:
        fh.write(model_dict['advanced-params'])
    model.load_model('model.json')
    os.remove('model.json')

    return model

def serialize_xgboost_regressor(model):
    serialized_model = {
        'meta': 'xgboost-regressor',
        'params': model.get_params()
    }

    model.save_model('model.json')
    with open('model.json', 'r') as fh:
        serialized_model['advanced-params'] = fh.read()
    os.remove('model.json')

    return serialized_model


def deserialize_xgboost_regressor(model_dict):
    model = XGBRegressor(**model_dict['params'])

    with open('model.json', 'w') as fh:
        fh.write(model_dict['advanced-params'])
    model.load_model('model.json')
    os.remove('model.json')

    return model

def serialize_xgboost_rf_regressor(model):
    serialized_model = {
        'meta': 'xgboost-rf-regressor',
        'params': model.get_params()
    }

    model.save_model('model.json')
    with open('model.json', 'r') as fh:
        serialized_model['advanced-params'] = fh.read()
    os.remove('model.json')

    return serialized_model


def deserialize_xgboost_rf_regressor(model_dict):
    model = XGBRFRegressor(**model_dict['params'])

    with open('model.json', 'w') as fh:
        fh.write(model_dict['advanced-params'])
    model.load_model('model.json')
    os.remove('model.json')

    return model


def serialize_lightgbm_regressor(model):
    serialized_model = {
        'meta': 'lightgbm-regressor',
        'params': model.get_params(),
        'booster': model.booster_.model_to_string(),
        'fitted_': model.fitted_,
        '_evals_result': model._evals_result,
        '_best_score': model._best_score,
        '_best_iteration': model._best_iteration,
        '_other_params': model._other_params,
        '_objective': model._objective,
        'class_weight': model.class_weight,
        '_class_weight': model._class_weight,
        '_class_map': model._class_map,
        '_n_features': model._n_features,
        '_n_features_in': model._n_features_in,
        '_classes': model._classes,
        '_n_classes': model._n_classes
    }

    return serialized_model


def deserialize_lightgbm_regressor(model_dict):
    params = model_dict['params']
    params['_Booster'] = LGBMBooster(model_str=model_dict['booster'])
    params['fitted_'] = model_dict['fitted_']
    params['_evals_result'] = model_dict['_evals_result']
    params['_best_score'] = model_dict['_best_score']
    params['_best_iteration'] = model_dict['_best_iteration']
    params['_other_params'] = model_dict['_other_params']
    params['_objective'] = model_dict['_objective']
    params['class_weight'] = model_dict['class_weight']
    params['_class_weight'] = model_dict['_class_weight']
    params['_class_map'] = model_dict['_class_map']
    params['_n_features'] = model_dict['_n_features']
    params['_n_features_in'] = model_dict['_n_features_in']
    params['_classes'] = model_dict['_classes']
    params['_n_classes'] = model_dict['_n_classes']
    model = LGBMRegressor().set_params(**params)

    return model


def serialize_lightgbm_ranker(model):
    serialized_model = {
        'meta': 'lightgbm-ranker',
        'params': model.get_params(),
        'booster': model.booster_.model_to_string(),
        'fitted_': model.fitted_,
        '_evals_result': model._evals_result,
        '_best_score': model._best_score,
        '_best_iteration': model._best_iteration,
        '_other_params': model._other_params,
        '_objective': model._objective,
        'class_weight': model.class_weight,
        '_class_weight': model._class_weight,
        '_class_map': model._class_map,
        '_n_features': model._n_features,
        '_n_features_in': model._n_features_in,
        '_classes': model._classes,
        '_n_classes': model._n_classes
    }

    return serialized_model


def deserialize_lightgbm_ranker(model_dict):
    params = model_dict['params']
    params['_Booster'] = LGBMBooster(model_str=model_dict['booster'])
    params['fitted_'] = model_dict['fitted_']
    params['_evals_result'] = model_dict['_evals_result']
    params['_best_score'] = model_dict['_best_score']
    params['_best_iteration'] = model_dict['_best_iteration']
    params['_other_params'] = model_dict['_other_params']
    params['_objective'] = model_dict['_objective']
    params['class_weight'] = model_dict['class_weight']
    params['_class_weight'] = model_dict['_class_weight']
    params['_class_map'] = model_dict['_class_map']
    params['_n_features'] = model_dict['_n_features']
    params['_n_features_in'] = model_dict['_n_features_in']
    params['_classes'] = model_dict['_classes']
    params['_n_classes'] = model_dict['_n_classes']
    model = LGBMRanker().set_params(**params)

    return model
