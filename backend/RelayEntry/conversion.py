import re

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_snake_case(camel_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

def convert_keys_to_camel_case(data):
    if isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    elif isinstance(data, dict):
        return {to_camel_case(key): convert_keys_to_camel_case(value) for key, value in data.items()}
    else:
        return data

def convert_keys_to_snake_case(data):
    if isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    elif isinstance(data, dict):
        return {to_snake_case(key): convert_keys_to_snake_case(value) for key, value in data.items()}
    else:
        return data
