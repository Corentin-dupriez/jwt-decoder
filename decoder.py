import base64
import re

def pretty_print_jwt(header: dict, payload: dict): 
    """
    Pretty prints a given header and payload as a string in a given format:

    {
        "key": "value",
        "key2": "value2"
    }.{
        "key3": "value3",
        "key4": "value4"
    }.[SIGNATURE]

    Parameters
    ----------
    header : dict
        The header of the JWT token as a dictionary.
    payload : dict
        The payload of the JWT token as a dictionary.

    Returns
    -------
    str
        The pretty printed string.
    """
    string = '{\n' 
    if header:
        string += ',\n'.join(f'\t"{key}": "{value}"' if not value.isdigit() else f'\t"{key}": {value}' for key, value in header.items()) + '\n}'
       
    if payload and header:
        string += '.{\n'
        
    if payload:
        string += ',\n'.join(f'\t"{key}": "{value}"' if not value.isdigit() else f'\t"{key}": {value}' for key, value in payload.items()) + '\n}.[SIGNATURE]'
    
    return string


def decode_jwt(jwt: str, part='all'): 
    """ 
    Decodes a given JWT token and returns the header and payload as dictionaries

    Parameters
    ----------
    jwt : str
        The JWT token to be decoded

    Returns
    -------
    header_decoded : dict
        The header of the JWT token as a dictionary
    payload_decoded : dict
        The payload of the JWT token as a dictionary
    """
    try:
        header, payload, signature = jwt.split('.')
        
    except ValueError:
        raise ValueError('Invalid JWT')
    
    header += '=' * (-len(header) % 4)
    header_decoded = convert_to_dict(base64.b64decode(header))
    
    payload_decoded = convert_to_dict(base64.b64decode(payload))
    
    if part == 'all':
        return pretty_print_jwt(header_decoded, payload_decoded)
    elif part == 'header':
        return pretty_print_jwt(header_decoded, {})
    elif part == 'payload':
        return pretty_print_jwt({}, payload_decoded)


def clean_string(string: bytes) -> str:
    """
    Clean a given string by removing {, }, and " characters.
    
    Parameters
    ----------
    string : bytes
        The string to be cleaned
    
    Returns
    -------
    str
        The cleaned string
    """
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


