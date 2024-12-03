from importlib import resources
from pathlib import Path
import nibabel as nib
import numpy as np
from typing import Union, Tuple, List


def get_resource_path(file_name: str) -> str:
    """Get the path to a resource file.

    Parameters
    ----------
    file_name : str
        The name of the resource file.

    Returns
    -------
    str
        The path to the resource file.

    Examples
    --------
    >>> get_resource_path('example.txt')
    'path/to/resources/example.txt'
    """
    return str(resources.files("hippunfold_plot") / "resources" / file_name)


def check_surf_map_is_label_gii(surf_map: Union[str, np.ndarray]) -> bool:
    """Check if the surface map is a label GIFTI file.

    Parameters
    ----------
    surf_map : str or np.ndarray
        The surface map to check.

    Returns
    -------
    bool
        True if the surface map is a label GIFTI file, False otherwise.

    Examples
    --------
    >>> check_surf_map_is_label_gii('example.label.gii')
    True
    >>> check_surf_map_is_label_gii('example.func.gii')
    False
    """
    if isinstance(surf_map, str):
        return surf_map.endswith("label.gii")
    return False


def read_pointset_from_surf_mesh(
    surf_mesh: Union[str, Tuple[np.ndarray, np.ndarray]]
) -> np.ndarray:
    """Read pointset from a surface mesh.

    Parameters
    ----------
    surf_mesh : str or tuple
        The surface mesh to read from. Can be a file path to a .gii file or a tuple of arrays.

    Returns
    -------
    np.ndarray
        The pointset data.

    Examples
    --------
    >>> points = read_pointset_from_surf_mesh('example.surf.gii')
    >>> points.shape
    (1000, 3)
    """
    if isinstance(surf_mesh, str):
        if surf_mesh.endswith("surf.gii"):
            points = (
                nib.load(surf_mesh)
                .get_arrays_from_intent("NIFTI_INTENT_POINTSET")[0]
                .data
            )
        else:
            raise TypeError("surf_mesh string not recognized as surf.gii")
    elif isinstance(surf_mesh, tuple):
        if len(surf_mesh) == 2:
            points = surf_mesh[0]
    return points


def read_data_from_surf_map(surf_map: Union[str, np.ndarray]) -> np.ndarray:
    """Read data from a surface map.

    Parameters
    ----------
    surf_map : str or np.ndarray
        The surface map to read from. Can be a file path to a .gii file or a numpy array.

    Returns
    -------
    np.ndarray
        The data from the surface map.

    Examples
    --------
    >>> data = read_data_from_surf_map('example.func.gii')
    >>> data.shape
    (1000,)
    """
    if isinstance(surf_map, str):
        if surf_map.endswith(".gii"):
            data = nib.load(surf_map).darrays[0].data
        else:
            raise TypeError("surf_map string not recognized as metric gii")
    elif isinstance(surf_map, np.ndarray):
        data = surf_map
    return data


def get_data_limits(surf_map: Union[str, np.ndarray]) -> Tuple[float, float]:
    """Get the data limits from a surface map.

    Parameters
    ----------
    surf_map : str or np.ndarray
        The surface map to get data limits from.

    Returns
    -------
    tuple
        The minimum and maximum values of the data.

    Examples
    --------
    >>> get_data_limits('example.func.gii')
    (0.0, 1.0)
    """
    data = read_data_from_surf_map(surf_map)
    return data.min(), data.max()


def get_surf_limits(
    surf_mesh: Union[str, Tuple[np.ndarray, np.ndarray]]
) -> Tuple[dict, dict]:
    """Get the surface limits from a surface mesh.

    Parameters
    ----------
    surf_mesh : str or tuple
        The surface mesh to get limits from. Can be a file path to a .gii file or a tuple of arrays.

    Returns
    -------
    tuple
        The x and y limits as dictionaries.

    Examples
    --------
    >>> xlim, ylim = get_surf_limits('example.surf.gii')
    >>> xlim
    {'left': -50.0, 'right': 50.0}
    >>> ylim
    {'bottom': -50.0, 'top': 50.0}
    """
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
    xlim_kwargs = {"left": x_min_cropped, "right": x_max_cropped}
    ylim_kwargs = {"bottom": y_min_cropped, "top": y_max_cropped}

    return xlim_kwargs, ylim_kwargs


def get_legend_elements_from_label_gii(label_map: str) -> List:
    """Get legend elements from a label GIFTI file.

    Parameters
    ----------
    label_map : str
        The path to the label GIFTI file.

    Returns
    -------
    list
        A list of legend elements.

    Examples
    --------
    >>> legend_elements = get_legend_elements_from_label_gii('example.label.gii')
    >>> isinstance(legend_elements, list)
    True
    """
    from matplotlib.patches import Patch

    # Load the GIFTI file
    label_gii = nib.load(label_map)

    # Extract the label table (LUT)
    label_table = label_gii.labeltable.labels

    # Create legend elements
    legend_elements = [
        Patch(
            facecolor=(
                label.red / 255.0,
                label.green / 255.0,
                label.blue / 255.0,
                label.alpha / 255.0,
            ),  # RGBA from LUT
            edgecolor="black",
            label=label.label,  # The name of the label
        )
        for label in label_table
        if label.label  # Skip empty labels if any
    ]
    return legend_elements
