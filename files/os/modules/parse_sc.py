def sc_to_dict(file_path: str) -> dict:
    sc_dict = {}
    f = open(file_path, 'r').read()
    lines = f.split('\n')
    for line in lines:
        option, args = line.split('=', 1)
        if not (args.startswith('\"') and args.endswith('\"')):
            args = args.split(', ')
        else:
            args = [args[1:len(args) - 1]]
        sc_dict[option] = args
    return sc_dict