def deepmerge(source, target):
    for k, v in source.items():
        if isinstance(v, dict):
            n = target.setdefault(k, {})
            deepmerge(v, n)
        else:
            target[k] = v

    return target
