import tools

with open('config') as f:
    config_data = [x.strip('\n') for x in f.readlines()]

for datum in config_data:
    param_split = datum.split('=')
    param = param_split[0]
    # TODO: Note there is no try/catch here. Up to user to configure config correctly.
    param_val = float(param_split[1])

    if param == 'window_size':
        window_size = int(param_val)
    if param == 'test_ratio':
        test_ratio = param_val
    if param == 'epochs':
        epochs = int(param_val)
    if param == 'neurons':
        neurons = int(param_val)
