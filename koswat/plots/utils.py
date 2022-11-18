from matplotlib import pyplot


def get_cmap(n_colors: int, name="hsv"):
    """
    Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    """
    return pyplot.cm.get_cmap(name, n_colors)
