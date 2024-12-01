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
![png](doc/example1_0.png)
![png](doc/example1_1.png)
    
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
    
![png](doc/example2_0.png)
![png](doc/example2_1.png)

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
    
![png](doc/example3_0.png)
![png](doc/example3_1.png)

## 🛠️ Functions

### `plot_hipp_surf`

```python
def plot_hipp_surf(surf_map: Union[str, list], 
                   density: str = '0p5mm', 
                   hemi: str = 'left', 
                   space: Optional[str] = None, 
                   figsize: Tuple[int, int] = (12, 8), 
                   dpi: int = 300, 
                   vmin: Optional[float] = None, 
                   vmax: Optional[float] = None, 
                   colorbar: bool = False, 
                   colorbar_shrink: float = 0.25, 
                   cmap: Optional[Union[str, plt.cm.ScalarMappable]] = None, 
                   view: str = 'dorsal', 
                   avg_method: str = 'median', 
                   bg_on_data: bool = True, 
                   alpha: float = 0.1, 
                   darkness: float = 2, 
                   **kwargs) -> plt.Figure:
    """
    This function plots a surface map of the hippocampus, which can be a label-hippdentate shape.gii, func.gii, or a Vx1 array 
    (where V is the number of vertices in the hippocampus and dentate). Any arguments that can be supplied to nilearn's plot_surf() 
    can also be applied here, overriding the defaults set below.    """
```

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
