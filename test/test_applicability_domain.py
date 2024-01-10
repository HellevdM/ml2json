import os
import unittest

import numpy as np
from sklearn.datasets import fetch_california_housing
from mlchemad.applicability_domains import (BoundingBoxApplicabilityDomain,
                                            ConvexHullApplicabilityDomain,
                                            PCABoundingBoxApplicabilityDomain,
                                            TopKatApplicabilityDomain,
                                            LeverageApplicabilityDomain,
                                            HotellingT2ApplicabilityDomain,
                                            KernelDensityApplicabilityDomain,
                                            IsolationForestApplicabilityDomain,
                                            CentroidDistanceApplicabilityDomain,
                                            KNNApplicabilityDomain,
                                            StandardizationApproachApplicabilityDomain)

from src import ml2json

class TestAPI(unittest.TestCase):

    def setUp(self):
        # take only the first 1000 samples
        self.X = fetch_california_housing()['data'][:1000]
        
    def check_applicability_domain(self, applicability_domain, model_name):
        for fit in [True, False]:
            if fit:
                applicability_domain.fit(self.X)
            expected_c = applicability_domain.contains(self.X)

            serialized_dict_model = ml2json.to_dict(applicability_domain)
            deserialized_dict_model = ml2json.from_dict(serialized_dict_model)

            ml2json.to_json(applicability_domain, model_name)
            deserialized_json_model = ml2json.from_json(model_name)
            os.remove(model_name)

            if fit:
                for deserialized_model in [deserialized_dict_model, deserialized_json_model]:
                    actual_c = deserialized_model.contains(self.X)

                    np.testing.assert_array_equal(expected_c, actual_c)
            
    def test_bounding_box_applicability_domain(self):
        model = BoundingBoxApplicabilityDomain()
        self.check_applicability_domain(model, 'bounding-box-ad.json')
        
        # check with extremum values per feature
        model = BoundingBoxApplicabilityDomain(
            range_=(list(self.X.min(axis=0)),
                    list(self.X.max(axis=0))))
        self.check_applicability_domain(model, 'bounding-box-ad.json')
        
        # check with percentiles is None
        model = BoundingBoxApplicabilityDomain(percentiles=None)
        self.check_applicability_domain(model, 'bounding-box-ad.json')
        
    def test_convex_hull_applicability_domain(self):
        model = ConvexHullApplicabilityDomain()
        self.check_applicability_domain(model, 'convex-hull-ad.json')
        
    def test_pca_bounding_box_applicability_domain(self):
        # TODO add robust scaler and maxabsscaler to ml2json
        model = PCABoundingBoxApplicabilityDomain(scaling='standard')
        self.check_applicability_domain(model, 'pca-bounding-box-ad.json')
        
    def test_topkat_applicability_domain(self):
        model = TopKatApplicabilityDomain()
        self.check_applicability_domain(model, 'topkat-ad.json')
        
    def test_leverage_applicability_domain(self):
        model = LeverageApplicabilityDomain()
        self.check_applicability_domain(model, 'leverage-ad.json')
        
    def test_hotelling_t2_applicability_domain(self):
        model = HotellingT2ApplicabilityDomain()
        self.check_applicability_domain(model, 'hotelling-t2-ad.json')

    def test_kernel_density_applicability_domain(self):
        model = KernelDensityApplicabilityDomain()
        self.check_applicability_domain(model, 'kernel-density-ad.json')
    
    def test_isolation_forest_applicability_domain(self):
        model = IsolationForestApplicabilityDomain()
        self.check_applicability_domain(model, 'isolation-forest-ad.json')
        
    def test_centroid_distance_applicability_domain(self):
        model = CentroidDistanceApplicabilityDomain()
        self.check_applicability_domain(model, 'centroid-distance-ad.json')
        
    def test_knn_applicability_domain(self):
        model = KNNApplicabilityDomain(scaling='standard')
        self.check_applicability_domain(model, 'knn-ad.json')
        
    def test_standardization_approach_applicability_domain(self):
        model = StandardizationApproachApplicabilityDomain()
        self.check_applicability_domain(model, 'standardization-approach-ad.json')