
def print_dict(in_dict: dict, depth: int = 0) -> None:
    for key in in_dict.keys():
        for i in range(depth):
            print(' │ ', end='')
        if isinstance(in_dict[key], dict):
            print(str(key))
            print_dict(in_dict[key], depth + 1)
        else:
            print(str(key) + ': ' + str(in_dict[key]))