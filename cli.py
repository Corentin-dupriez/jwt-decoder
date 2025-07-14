from decoder import decode_jwt
import argparse

def main():
    parser = argparse.ArgumentParser(description='Decode a JWT token')
    
    parser.add_argument('jwt', 
                        type=str, 
                        help='The JWT token to decode')
    
    parser.add_argument('--part', 
                        type=str, 
                        help='The part of the JWT token to decode', 
                        default='all',
                        choices=['header', 'payload', 'all'])
    
    args = parser.parse_args()
    try:
        print(decode_jwt(args.jwt, args.part))
    except Exception as e:
        print(f'Error decoding JWT: {e}')

if __name__ == '__main__': 
    main()