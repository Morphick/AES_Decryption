import sys
from Crypto.Cipher import AES
import struct
import argparse

def decrypt_file(key, in_file, out_file=None):
    """ 
        AES file decryption script. Adaptation of script written by Eli Bendersky.
        params:
            - key: key to used to decrypt file
            - in_file: encrypted file to decrypt
            - out_file: Optional, if not provided in_file will be used with a .zip suffix.
    """
    if not out_file:
        out_file = in_file + '.zip'

    with open(in_file, 'rb') as infile:
        orig_file_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            outfile.write(decryptor.decrypt(infile.read()))
            outfile.truncate(orig_file_size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AES File Decryptor')
    parser.add_argument('-k', '--key', type=str, help='Key to decrypt file', required=True)
    parser.add_argument('-i', '--in_file', type=str, help='Encrypted file', required=True)
    parser.add_argument('-o', '--out_file', type=str, help='Output file')
    args = parser.parse_args()

    decrypt_file(args.key, args.in_file, args.out_file)
    print('File decrypted successfully.')
