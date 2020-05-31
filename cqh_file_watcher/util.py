
def string_replace(param_str: str, env_d):
    for key, value in env_d.items():
        param_str = param_str.replace("${%s}" % key, value)
    return param_str
