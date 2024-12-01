import unittest
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from hippunfold_plot.plotting import plot_hipp_surf
from hippunfold_plot.utils import get_resource_path

class TestPlotHippSurf(unittest.TestCase):

    def setUp(self):
        # Get a valid file path from resources
        self.label_gii = get_resource_path('tpl-avg_label-hippdentate_density-1mm_subfields.label.gii')
        self.density = '1mm'

        # Load the GIFTI file to get the number of vertices
        gii = nib.load(self.label_gii)
        num_vertices = gii.darrays[0].data.shape[0]

        # Create a random numpy array with the same number of vertices
        self.random_surf_map = np.random.rand(num_vertices, 1)


    def test_invalid_density(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map=self.label_gii, density='invalid_density')

    def test_invalid_hemi(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map=self.label_gii, hemi='invalid_hemi')

    def test_invalid_space(self):
        with self.assertRaises(ValueError):
            plot_hipp_surf(surf_map=self.label_gii, space='invalid_space')

    def test_plot_creation_with_file(self):
        fig = plot_hipp_surf(surf_map=self.label_gii, density=self.density)
        self.assertIsInstance(fig, plt.Figure)

    def test_plot_creation_with_numpy_array(self):
        fig = plot_hipp_surf(surf_map=self.random_surf_map, density=self.density)
        self.assertIsInstance(fig, plt.Figure)

    def test_colorbar_with_file(self):
        fig = plot_hipp_surf(surf_map=self.label_gii, density=self.density, colorbar=True)
        self.assertIsInstance(fig, plt.Figure)

    def test_colorbar_with_numpy_array(self):
        fig = plot_hipp_surf(surf_map=self.random_surf_map, density=self.density, colorbar=True)
        self.assertIsInstance(fig, plt.Figure)

    def test_default_parameters_with_file(self):
        fig = plot_hipp_surf(surf_map=self.label_gii, density=self.density)
        self.assertIsInstance(fig, plt.Figure)

    def test_default_parameters_with_numpy_array(self):
        fig = plot_hipp_surf(surf_map=self.random_surf_map, density=self.density)
        self.assertIsInstance(fig, plt.Figure)

    def test_custom_parameters_with_file(self):
        fig = plot_hipp_surf(surf_map=self.label_gii, density='1mm', hemi='right', space='canonical', figsize=(10, 6), dpi=200, vmin=0, vmax=1, colorbar=True, colorbar_shrink=0.5, cmap='viridis', view='ventral', avg_method='mean', bg_on_data=False, alpha=0.5, darkness=1)
        self.assertIsInstance(fig, plt.Figure)

    def test_custom_parameters_with_numpy_array(self):
        fig = plot_hipp_surf(surf_map=self.random_surf_map, density='1mm', hemi='right', space='canonical', figsize=(10, 6), dpi=200, vmin=0, vmax=1, colorbar=True, colorbar_shrink=0.5, cmap='viridis', view='ventral', avg_method='mean', bg_on_data=False, alpha=0.5, darkness=1)
        self.assertIsInstance(fig, plt.Figure)

if __name__ == '__main__':
    unittest.main()

