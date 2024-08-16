"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] AES encryption of strings
    - https://onboardbase.com/blog/aes-encryption-decryption
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2 import Type
from argon2 import hash_password_raw
from argon2.exceptions import VerifyMismatchError
import hashlib
import json

import global_schema
from lib.logger import Logger as Lg
from loading_animation import ScreenLoadingAnimation


class CredentialGenerator(object):

    GEN_CREDENTIAL_SEPARATOR = get_random_bytes(4)
    GEN_PASSWORD_PEPPER = 'V]=tDk$3<=_qA2TR'
    GEN_PASSWORD_SALT = hashlib.sha512(get_random_bytes(32))

    def __init__(self):
        self.anim = global_schema.anim
        pass

    def encrypt(self, json_data_to_encrypt: dict, unlock_key: str):
        """
        Generates credential bytes that securely encodes a dict data containing API keys and OAUTH2.0 tokens.
        :param json_data_to_encrypt: a dict object which will be encrypted.
        :param unlock_key: the password (in UTF-8 string) to encrypt-decrypt the JSON data.
        :return: a bytes which encode the JSON data.
        """

        # Convert the user's input password into a 16-bytes Argon2 hash.
        msg = 'Converting password into 16-bytes Argon2id hash ...'
        self.anim.set_prog_msg(40, msg)
        Lg('lib.credentials.CredentialGenerator.encrypt', msg)
        key = self.generate_hash(unlock_key, self.GEN_PASSWORD_SALT.hexdigest())

        # GCM (Galois Counter Mode) is the most secure mode, [1]
        # but AES-OFB is less complex to implement.
        msg = 'Generating the AES-OFB cipher ...'
        self.anim.set_prog_msg(75, msg)
        Lg('lib.credentials.CredentialGenerator.encrypt', msg)
        cipher = AES.new(bytes(key), AES.MODE_OFB)
        cipher_text = cipher.encrypt(json.dumps(json_data_to_encrypt).encode())
        iv = cipher.iv

        # DEBUG. Please always comment out on production.
        # print(self.GEN_CREDENTIAL_SEPARATOR, cipher_text, iv, self.GEN_PASSWORD_SALT.digest())

        # This is the output, encrypted byte string.
        msg = 'Credential generated successfully!'
        self.anim.set_prog_msg(100, msg)
        Lg('lib.credentials.CredentialGenerator.encrypt', msg)
        sep = self.GEN_CREDENTIAL_SEPARATOR
        out = sep + cipher_text + sep + iv + sep + self.GEN_PASSWORD_SALT.digest()
        return out

    def generate_hash(self, encrypt_decrypt_key: str, salt: str):
        """
        Generates Argon2id hash used in encrypting/decrypting the JSON credential.
        :param encrypt_decrypt_key: in plain UTF-8 string, the password to unlock/lock the JSON data.
        :param salt: if exists, the salting of the encrypted JSON data (in UTF-8 string format).
        :return: an Argon2id hash in raw bytes.
        """
        return hash_password_raw(
            password=(encrypt_decrypt_key + self.GEN_PASSWORD_PEPPER).encode('utf-8'),
            salt=salt.encode('utf-8'),
            time_cost=30,
            memory_cost=65536,
            parallelism=16,
            hash_len=16,
            type=Type.ID
        )


class CredentialValidator(object):

    VALIDATOR_PASSWORD_PEPPER = CredentialGenerator.GEN_PASSWORD_PEPPER

    def __init__(self, cred_loc: str = ''):
        """
        Initializes the validator.
        :param cred_loc: the encrypted JSON file to validate and decrypt.
        """
        self.anim_window = global_schema.anim

        # Pass the variable to all of this class' method.
        self.cred_loc = cred_loc

    def decrypt(self, cred_password: str):
        """
        Validates whether the given credential password can be used
        to decrypt the encrypted JSON file containing the API keys.
        :param cred_password: the password used to decrypt the JSON file.
        :param anim_window: the animation loading window displaying the progress bar as well as the status message.
        :return: A tuple of three of: True if valid, False if the password cannot be used to decrypt the JSON file,
        the decrypted JSON dict, and a message specifying the operation status.
        """

        try:
            # Attempt to open the encrypted JSON data.
            with open(self.cred_loc, 'rb') as fo:
                parsed_bytes = fo.read()

            # Obtains the separator byte.
            msg = 'Obtaining the separator byte ...'
            self.anim_window.set_prog_msg(10, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            sep = parsed_bytes[:4]
            split_bytes = parsed_bytes.split(sep)

            # Obtains the cipher text, iv value, and password salt.
            msg = 'Resolving the AES-OFB cipher text, iv value, and password salt ...'
            self.anim_window.set_prog_msg(25, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            cipher_text = split_bytes[1]
            iv = split_bytes[2]
            salt = split_bytes[3]

            # Obtains the Argon2id hash with the given credential password.
            msg = 'Obtaining the Argon2id encryption hash ...'
            self.anim_window.set_prog_msg(50, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            generator = CredentialGenerator()
            argon2id_hash = generator.generate_hash(cred_password, salt.hex())

            # DEBUG. Please always comment out on production.
            # print(sep, self.cipher_text, self.iv, self.salt)

            # Attempts to decipher the text.
            msg = 'Transforming rounds and deciphering the text ...'
            self.anim_window.set_prog_msg(75, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            decrypt_cipher = AES.new(argon2id_hash, AES.MODE_OFB, iv=iv)
            plain_text = decrypt_cipher.decrypt(cipher_text).decode('utf-8')

            # DEBUG. Please always comment out on production.
            # print(plain_text)

            # Attempts to parse the decrypted plain text as a Python dict.
            msg = 'Parsing the JSON ...'
            self.anim_window.set_prog_msg(90, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            parsed_dict = json.loads(plain_text)

            # DEBUG. Please always comment out on production.
            # print(parsed_dict)
            # print(type(parsed_dict))

            # Return the decrypted JSON dict.
            msg = 'The encrypted JSON credential has been decrypted successfully!'
            self.anim_window.set_prog_msg(100, msg)
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            return True, parsed_dict, msg

        except UnicodeDecodeError as e:
            msg = f'The password you are specifying is invalid: {e}'
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            return False, {}, msg

        except VerifyMismatchError as e:
            msg = f'The password you are specifying is invalid: {e}'
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            return False, {}, msg

        except ValueError as e:
            msg = f'The JSON file you specified is invalid, corrupted, or broken: {e}'
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            return False, {}, msg

        except FileNotFoundError as e:
            msg = f'The credential file you are specifying cannot be found!: {e}'
            Lg('lib.credentials.CredentialValidator.decrypt', msg)
            return False, {}, msg
