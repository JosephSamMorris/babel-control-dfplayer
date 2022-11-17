def constrain(v, vmin, vmax):
    if v < vmin:
        return vmin
    elif v > vmax:
        return vmax

    return v
