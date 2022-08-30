# -*- coding: utf-8 -*-

import random
import unittest

import numpy as np
from numpy import testing
from sklearn.datasets import make_regression
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor, XGBRFRegressor, XGBRanker
from lightgbm import LGBMRegressor, LGBMRanker

from src import sklearn_json as skljson


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.X, self.y = make_regression(n_samples=50, n_features=3, n_informative=3, random_state=0, shuffle=False)
        self.y_rank = np.argsort(np.argsort(self.y)).tolist()

        feature_hasher = FeatureHasher(n_features=3)
        features = []
        for i in range(0, 100):
            features.append({'a': random.randint(0, 2), 'b': random.randint(3, 5), 'c': random.randint(6, 8)})
        self.y_sparse = [random.random() for i in range(0, 100)]
        self.X_sparse = feature_hasher.transform(features)

    def check_model(self, model):
        # Given
        model.fit(self.X, self.y)

        # When
        serialized_model = skljson.to_dict(model)
        deserialized_model = skljson.from_dict(serialized_model)

        # Then
        expected_predictions = model.predict(self.X)
        actual_predictions = deserialized_model.predict(self.X)

        testing.assert_array_equal(expected_predictions, actual_predictions)

    def check_sparse_model(self, model):
        # Given
        model.fit(self.X_sparse, self.y_sparse)

        # When
        serialized_model = skljson.to_dict(model)
        deserialized_model = skljson.from_dict(serialized_model)

        # Then
        expected_predictions = model.predict(self.X_sparse)
        actual_predictions = deserialized_model.predict(self.X_sparse)

        testing.assert_array_equal(expected_predictions, actual_predictions)

    def test_linear_regression(self):
        self.check_model(LinearRegression())
        self.check_sparse_model(LinearRegression())

    def test_lasso_regression(self):
        self.check_model(Lasso(alpha=0.1))
        self.check_sparse_model(Lasso(alpha=0.1))

    def test_elasticnet_regression(self):
        self.check_model(ElasticNet(alpha=0.1))
        self.check_sparse_model(ElasticNet(alpha=0.1))

    def test_ridge_regression(self):
        self.check_model(Ridge(alpha=0.5))
        self.check_sparse_model(Ridge(alpha=0.5))

    def test_svr(self):
        self.check_model(SVR(gamma='scale', C=1.0, epsilon=0.2))
        self.check_sparse_model(SVR(gamma='scale', C=1.0, epsilon=0.2))

    def test_decision_tree_regression(self):
        self.check_model(DecisionTreeRegressor())
        self.check_sparse_model(DecisionTreeRegressor())

    def test_gradient_boosting_regression(self):
        self.check_model(GradientBoostingRegressor())
        self.check_sparse_model(GradientBoostingRegressor())

    def test_random_forest_regression(self):
        self.check_model(RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100))
        self.check_sparse_model(RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100))

    def test_mlp_regression(self):
        self.check_model(MLPRegressor(max_iter=10000))
        self.check_sparse_model(MLPRegressor(max_iter=10000))

    def check_ranking_model(self, model):
        # Given
        model.fit(self.X, self.y_rank, group=[10, len(self.y) - 10])

        # When
        serialized_model = skljson.to_dict(model)
        deserialized_model = skljson.from_dict(serialized_model)

        # Then
        expected_predictions = model.predict(self.X)
        actual_predictions = deserialized_model.predict(self.X)

        testing.assert_array_equal(expected_predictions, actual_predictions)

    def test_xgboost_ranker(self):
        self.check_ranking_model(XGBRanker())

    def test_xgboost_regressor(self):
        self.check_model(XGBRegressor())

    def test_xgboost_rf_regressor(self):
        self.check_model(XGBRFRegressor())

    def test_lightgbm_regressor(self):
        self.check_model(LGBMRegressor())

    def test_lightgbm_ranker(self):
        self.check_ranking_model(LGBMRanker(label_gain=[i for i in range(self.X.shape[0] + 1)]))
