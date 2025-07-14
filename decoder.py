import base64
import re

def decode_jwt(jwt: str): 
    try:
        header, payload, signature = jwt.split('.')
    except ValueError:
        raise ValueError('Invalid JWT')
    
    header += '=' * (-len(header) % 4)
    header_decoded = convert_to_dict(base64.b64decode(header))
    print(base64.b64decode(payload))
    payload_decoded = convert_to_dict(base64.b64decode(payload))
    return header_decoded, payload_decoded

def clean_string(string: bytes) -> str:
    return re.sub('"', '',re.sub('}', '', re.sub('{', '', string.decode('utf-8'))))

def convert_to_dict(element: bytes) -> dict:
    """
    Convert a bytes object (e.g. a string) into a dictionary.
    
    Args:
        element (bytes): The bytes object to convert.
    
    Returns:
        dict: The converted dictionary.
    """
    el_dict = {}
    element = clean_string(element)
    element = element.split(',')
    for el in element:
        key, value = el.split(':')[0], el.split(':')[1:]
        el_dict[key.strip()] = ':'.join(value).strip()
    return el_dict


if __name__ == '__main__': 
    jwt = input('Enter JWT: ')
    print(decode_jwt(jwt))