# 🧠 hippunfold_surf

This package provides plotting functions for hippocampal surface maps from HippUnfold (https://github.com/khanlab/hippunfold), 
wrapping the Nilearn (https://nilearn.github.io) plotting functions (matplotlib engine) to achieve this. 

Note: these plotting functions are distinct from those in HippoMaps (https://github.com/MICA-MNI/hippomaps), which use 
VTK wrappers and have a number of limitations therein. 

This package is new and still under active development so suggestions and pull-requests are welcome!


## 📦 Installation

To install the package, simply run:

```sh
pip install hippunfold_plot
```

## 🚀 Usage

Here are some examples of how to use the `plot_hipp_surf` function to visualize hippocampal surface maps.

### Example 1: Plot Both Hemispheres

```python
from hippunfold_plot.plotting import plot_hipp_surf
from hippunfold_plot.utils import get_resource_path

#get subfields for demonstrating plotting
label_gii = get_resource_path('tpl-avg_label-hippdentate_density-{density}_subfields.label.gii')
density = '1mm'

# Plot dorsal view
fig = plot_hipp_surf(label_gii.format(density=density), hemi=None, density=density, view='dorsal')

# Plot ventral view
fig = plot_hipp_surf(label_gii.format(density=density), hemi=None, density=density, view='ventral')

```
![png](docs/example1_0.png)
![png](docs/example1_1.png)
    
### Example 2: Plot Left and Right Hemispheres Separately

```python
from hippunfold_plot.plotting import plot_hipp_surf
from hippunfold_plot.utils import get_resource_path

#get subfields for demonstrating plotting
label_gii = get_resource_path('tpl-avg_label-hippdentate_density-{density}_subfields.label.gii')
density = '1mm'

# Plot left hemisphere
fig = plot_hipp_surf(label_gii.format(density=density), hemi='left', density=density, view='dorsal')

# Plot right hemisphere
fig = plot_hipp_surf(label_gii.format(density=density), hemi='right', density=density, view='dorsal')

```
    
![png](docs/example2_0.png)
![png](docs/example2_1.png)

### Example 3: Plot unfolded and canonical space separately

```python
from hippunfold_plot.plotting import plot_hipp_surf
from hippunfold_plot.utils import get_resource_path

#get subfields for demonstrating plotting
label_gii = get_resource_path('tpl-avg_label-hippdentate_density-{density}_subfields.label.gii')
density = '1mm'

# Plot left hemisphere in unfolded space
fig = plot_hipp_surf(label_gii.format(density=density), space='unfold', density=density, view='dorsal')

# Plot left hemisphere in canonical space
fig = plot_hipp_surf(label_gii.format(density=density), space='canonical', density=density, view='dorsal')
```
    
![png](docs/example3_0.png)
![png](docs/example3_1.png)

## 🛠️ Functions

### `plot_hipp_surf`

Plot hippocampal surface map.

This function plots a surface map of the hippocampus, which can be a label-hippdentate shape.gii, func.gii, or a Vx1 array
(where V is the number of vertices in the hippocampus and dentate). Any arguments that can be supplied to nilearn's plot_surf()
can also be applied here, overriding the defaults set below.

###### Parameters
 - **surf_map** (str or array-like):
   The surface map to plot. This can be a file path to a .gii file or a Vx1 array.
 - **density** (str, optional):
   The density of the surface map. Can be 'unfoldiso', '0p5mm', '1mm', or '2mm'. Default is '0p5mm'.
 - **hemi** (str, optional):
   The hemisphere to plot. Can be 'left', 'right', or None (in which case both are plotted). Default is 'left'.
 - **space** (str, optional):
   The space of the surface map. Can be 'canonical', 'unfold', or None (in which case both are plotted). Default is None.
 - **figsize** (tuple, optional):
   The size of the figure. Default is (12, 8).
 - **dpi** (int, optional):
   The resolution of the figure in dots per inch. Default is 300.
 - **vmin** (float, optional):
   The minimum value for the color scale. Default is None.
 - **vmax** (float, optional):
   The maximum value for the color scale. Default is None.
 - **colorbar** (bool, optional):
   Whether to display a colorbar. Default is False.
 - **colorbar_shrink** (float, optional):
   The shrink factor for the colorbar. Default is 0.25.
 - **cmap** (str or colormap, optional):
   The colormap to use. Default is None.
 - **view** (str, optional):
   The view of the surface plot. Default is 'dorsal'.
 - **avg_method** (str, optional):
   The method to average the data. Default is 'median'.
 - **bg_on_data** (bool, optional):
   Whether to display the background on the data. Default is True.
 - **alpha** (float, optional):
   The alpha transparency level. Default is 0.1.
 - **darkness** (float, optional):
   The darkness level of the background. Default is 2.
 - **axes** (matplotlib.axes.Axes or list of matplotlib.axes.Axes, optional):
   Axes to plot on. If None, new axes will be created. If a single axis is provided, it will be used for a single plot.
   If multiple plots are to be made, a list of axes should be provided.
 - **figure** (matplotlib.figure.Figure, optional):
   The figure to plot on. If None, a new figure will be created.
 - ****kwargs** (dict):
   Additional arguments to pass to nilearn's plot_surf().

###### Returns
 - **figure** (matplotlib.figure.Figure):
   The figure object.

###### Notes
By default, this function will plot one hemisphere (left by default) in both canonical and unfolded space.
Both surfaces can be plotted with hemi=None, but the same surf_map will be plotted on both.
## 🧪 Testing

To run the tests, including unit tests and docstring tests, use the following command:

```sh
python -m unittest discover -s . -p "test_*.py"
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Contributing

We welcome contributions! Please see our [CONTRIBUTING](CONTRIBUTING.md) guidelines for more details.

## 📞 Contact

If you have any questions or feedback, feel free to reach out or post an issue!

---

Happy plotting! 🎉
