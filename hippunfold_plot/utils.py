from importlib import resources
from pathlib import Path
import nibabel as nib
import numpy as np

def get_resource_path(file_name: str) -> str:
    """Get the path to a resource file."""
    return str(resources.files("hippunfold_plot") / 'resources'/ file_name )

def check_surf_map_is_label_gii(surf_map):
    if isinstance(surf_map,str):
        if surf_map[-9:] == 'label.gii':
            return True
    else:
        return False
            
def read_pointset_from_surf_mesh(surf_mesh):
    if isinstance(surf_mesh,str):
        if surf_mesh[-8:] == 'surf.gii':
            points = nib.load(surf_mesh).get_arrays_from_intent('NIFTI_INTENT_POINTSET')[0].data
        else: 
            raise TypeError("surf_mesh string not recognized as surf.gii")
    elif isinstance(surf_mesh,tuple):
        if len(surf_mesh) == 2:
            points = surf_mesh[0]
    return points

def read_data_from_surf_map(surf_map):
    if isinstance(surf_map,str):
        if surf_map[-4:] == '.gii':
            data = nib.load(surf_map).darrays[0].data
        else: 
            raise TypeError("surf_mesh string not recognized as metric gii")
    elif isinstance(surf_map,np.ndarray):
        data = surf_map
    return data

def get_data_limits(surf_map):
    data = read_data_from_surf_map(surf_map)
    return (data.min(),data.max())
    

    
def get_surf_limits(surf_mesh):
    points = read_pointset_from_surf_mesh(surf_mesh)
        
    # Calculate the ranges for each dimension
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()

    x_range = x_max - x_min
    y_range = y_max - y_min
    
    # Adjust the ranges to match the desired aspect ratio by cropping
    target_y_range = x_range 
    y_mid = (y_max + y_min) / 2
    y_min_cropped = y_mid - target_y_range / 2
    y_max_cropped = y_mid + target_y_range / 2
    x_min_cropped, x_max_cropped = x_min, x_max

    # Return the cropped limits
    xlim_kwargs = {'left': x_min_cropped, 'right': x_max_cropped}
    ylim_kwargs = {'bottom': y_min_cropped, 'top': y_max_cropped}

    return xlim_kwargs, ylim_kwargs
    

def get_legend_elements_from_label_gii(label_map):
    """ not used yet -- this uses colors from gifti metadata, but 
    the matplotlib colormap isn't overrided yet, just the legend.."""
    
    from matplotlib.patches import Patch
    
    # Load the GIFTI file
    label_gii = nib.load(label_map)
    
    # Extract the label table (LUT)
    label_table = label_gii.labeltable.labels
    
    # Create legend elements
    legend_elements = [
        Patch(
            facecolor=(label.red/255.0, label.green/255.0, label.blue/255.0, label.alpha/255.0),  # RGBA from LUT
            edgecolor="black",
            label=label.label  # The name of the label
        )
        for label in label_table if label.label  # Skip empty labels if any
    ]
    return legend_elements
