import unittest
import matplotlib.pyplot as plt
from plotting import plot_hipp_surf

class TestPlotHippSurf(unittest.TestCase):

    def test_invalid_density(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map='dummy_path', density='invalid_density')

    def test_invalid_hemi(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map='dummy_path', hemi='invalid_hemi')

    def test_invalid_space(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map='dummy_path', space='invalid_space')

    def test_plot_creation(self):
        fig = plot_hipp_surf(surf_map='dummy_path')
        self.assertIsInstance(fig, plt.Figure)

    def test_colorbar(self):
        fig = plot_hipp_surf(surf_map='dummy_path', colorbar=True)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 6)  # 5 plots + 1 colorbar

    def test_default_parameters(self):
        fig = plot_hipp_surf(surf_map='dummy_path')
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 5)  # 5 plots

    def test_custom_parameters(self):
        fig = plot_hipp_surf(surf_map='dummy_path', density='1mm', hemi='right', space='canonical', figsize=(10, 6), dpi=200, vmin=0, vmax=1, colorbar=True, colorbar_shrink=0.5, cmap='viridis', view='ventral', avg_method='mean', bg_on_data=False, alpha=0.5, darkness=1)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 6)  # 5 plots + 1 colorbar

if __name__ == '__main__':
    unittest.main()