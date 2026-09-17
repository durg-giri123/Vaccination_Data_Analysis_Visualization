import unittest
import pandas as pd
import numpy as np

class TestVaccinationPipeline(unittest.TestCase):
    def test_coverage_gap_calculation(self):
        df = pd.DataFrame({'coverage': [90, 95, 100, np.nan, 50]})
        df['coverage_gap'] = df['coverage'].apply(lambda x: 95 - x if pd.notnull(x) and x <= 95 else (0 if pd.notnull(x) else np.nan))
        self.assertEqual(df['coverage_gap'][0], 5)
        self.assertEqual(df['coverage_gap'][1], 0)
        self.assertEqual(df['coverage_gap'][2], 0)
        self.assertTrue(np.isnan(df['coverage_gap'][3]))
        self.assertEqual(df['coverage_gap'][4], 45)
        
    def test_target_achievement(self):
        df = pd.DataFrame({'coverage': [90, 95, 100]})
        df['target_achieved'] = (df['coverage'] >= 95).astype(int)
        self.assertEqual(df['target_achieved'][0], 0)
        self.assertEqual(df['target_achieved'][1], 1)
        self.assertEqual(df['target_achieved'][2], 1)

if __name__ == '__main__':
    unittest.main()
