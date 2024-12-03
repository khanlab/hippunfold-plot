import matplotlib.pyplot as plt
from nilearn.plotting import plot_surf
from hippunfold_plot.utils import (
    get_surf_limits,
    get_data_limits,
    get_resource_path,
    check_surf_map_is_label_gii,
    get_legend_elements_from_label_gii,
)
from typing import Union, Tuple, Optional, List
import numpy as np


def plot_hipp_surf(
    surf_map: Union[str, list],
    density: str = "0p5mm",
    hemi: str = "left",
    space: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8),
    dpi: int = 300,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    colorbar: bool = False,
    colorbar_shrink: float = 0.25,
    cmap: Optional[Union[str, plt.cm.ScalarMappable]] = None,
    view: str = "dorsal",
    avg_method: str = "median",
    bg_on_data: bool = True,
    alpha: float = 0.1,
    darkness: float = 2,
    axes: Optional[Union[plt.Axes, List[plt.Axes]]] = None,
    figure: Optional[plt.Figure] = None,
    **kwargs,
) -> plt.Figure:
    """Plot hippocampal surface map.

    This function plots a surface map of the hippocampus, which can be a label-hippdentate shape.gii, func.gii, or a Vx1 array
    (where V is the number of vertices in the hippocampus and dentate). Any arguments that can be supplied to nilearn's plot_surf()
    can also be applied here, overriding the defaults set below.

    Parameters
    ----------
    surf_map : str or array-like
        The surface map to plot. This can be a file path to a .gii file or a Vx1 array.
    density : str, optional
        The density of the surface map. Can be 'unfoldiso', '0p5mm', '1mm', or '2mm'. Default is '0p5mm'.
    hemi : str, optional
        The hemisphere to plot. Can be 'left', 'right', or None (in which case both are plotted). Default is 'left'.
    space : str, optional
        The space of the surface map. Can be 'canonical', 'unfold', or None (in which case both are plotted). Default is None.
    figsize : tuple, optional
        The size of the figure. Default is (12, 8).
    dpi : int, optional
        The resolution of the figure in dots per inch. Default is 300.
    vmin : float, optional
        The minimum value for the color scale. Default is None.
    vmax : float, optional
        The maximum value for the color scale. Default is None.
    colorbar : bool, optional
        Whether to display a colorbar. Default is False.
    colorbar_shrink : float, optional
        The shrink factor for the colorbar. Default is 0.25.
    cmap : str or colormap, optional
        The colormap to use. Default is None.
    view : str, optional
        The view of the surface plot. Default is 'dorsal'.
    avg_method : str, optional
        The method to average the data. Default is 'median'.
    bg_on_data : bool, optional
        Whether to display the background on the data. Default is True.
    alpha : float, optional
        The alpha transparency level. Default is 0.1.
    darkness : float, optional
        The darkness level of the background. Default is 2.
    axes : matplotlib.axes.Axes or list of matplotlib.axes.Axes, optional
        Axes to plot on. If None, new axes will be created. If a single axis is provided, it will be used for a single plot.
        If multiple plots are to be made, a list of axes should be provided.
    figure : matplotlib.figure.Figure, optional
        The figure to plot on. If None, a new figure will be created.
    **kwargs : dict
        Additional arguments to pass to nilearn's plot_surf().

    Returns
    -------
    figure : matplotlib.figure.Figure
        The figure object.

    Notes
    -----
    By default, this function will plot one hemisphere (left by default) in both canonical and unfolded space.
    Both surfaces can be plotted with hemi=None, but the same surf_map will be plotted on both.

    """
    # Validate inputs
    valid_densities = ["unfoldiso", "0p5mm", "1mm", "2mm"]
    valid_spaces = ["canonical", "unfold", None]
    if density not in valid_densities:
        raise ValueError(
            f"Invalid value for 'density'. Expected one of {valid_densities}."
        )
    if hemi not in ["left", "right", None]:
        raise ValueError("Invalid value for 'hemi'. Expected 'left', 'right', or None.")
    if space not in valid_spaces:
        raise ValueError(f"Invalid value for 'space'. Expected one of {valid_spaces}.")

    surf_gii = get_resource_path(
        "tpl-avg_hemi-{hemi}_space-{space}_label-hippdentate_density-{density}_midthickness.surf.gii"
    )
    curv_gii = get_resource_path(
        "tpl-avg_label-hippdentate_density-{density}_curvature.shape.gii"
    )

    plot_kwargs = {
        "surf_map": surf_map,
        "bg_map": curv_gii.format(density=density),
        "alpha": alpha,
        "bg_on_data": bg_on_data,
        "darkness": darkness,
        "avg_method": avg_method,
        "cmap": cmap,
        "view": view,
        "vmin": vmin,
        "vmax": vmax,
    }

    # add any user arguments
    plot_kwargs.update(kwargs)

    # Define the plotting order for each hemisphere
    hemi_space_map = {"left": ["unfold", "canonical"], "right": ["canonical", "unfold"]}

    # Determine the number of plots to be made
    hemis_to_plot = [hemi] if hemi else hemi_space_map.keys()
    num_plots = sum(len([space] if space else hemi_space_map[h]) for h in hemis_to_plot)

    # Validate axes input
    if axes is not None:
        if isinstance(axes, plt.Axes):
            if num_plots > 1:
                raise ValueError(
                    "Multiple plots requested, but only one axis provided."
                )
            axes = [axes]
        elif isinstance(axes, np.ndarray):
            if len(axes) != num_plots:
                raise ValueError(f"Expected {num_plots} axes, but got {len(axes)}.")
        else:
            raise ValueError(
                "Invalid type for 'axes'. Expected matplotlib.axes.Axes or array of matplotlib.axes.Axes."
            )

    # Create a figure if not provided
    if figure is None:
        figure = plt.figure(figsize=figsize, dpi=dpi)

    # Define positions for 4 tall side-by-side axes
    positions = [
        [0.05, 0.1, 0.2, 0.8],  # Left, bottom, width, height
        [0.18, 0.1, 0.2, 0.8],
        [0.30, 0.1, 0.2, 0.8],
        [0.43, 0.1, 0.2, 0.8],
        [0.55, 0.1, 0.2, 0.8],
    ]

    # Create axes if not provided
    if axes is None:
        axes = [
            figure.add_axes(positions[i], projection="3d") for i in range(num_plots)
        ]

    pos = 0

    # Build the composite plot
    for h in hemis_to_plot:
        spaces_to_plot = [space] if space else hemi_space_map[h]
        for s in spaces_to_plot:
            ax = axes[pos]
            plot_surf(
                surf_mesh=surf_gii.format(hemi=h, space=s, density=density),
                axes=ax,
                figure=figure,
                **plot_kwargs,
            )
            (xlim_kwargs, ylim_kwargs) = get_surf_limits(
                surf_mesh=surf_gii.format(hemi=h, space=s, density=density)
            )
            ax.set_xlim(**xlim_kwargs)
            ax.set_ylim(**ylim_kwargs)
            ax.set_facecolor((0, 0, 0, 0))  # RGBA: last value is alpha for transparency
            pos = pos + 1

    if colorbar:  # custom colorbar
        import matplotlib as mpl

        (datamin, datamax) = get_data_limits(surf_map)
        norm = mpl.colors.Normalize(
            vmin=vmin if vmin else datamin, vmax=vmax if vmax else datamax
        )  # Match your data range
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # Dummy array for ScalarMappable
        plt.colorbar(sm, ax=figure.axes, shrink=colorbar_shrink)

    return figure
