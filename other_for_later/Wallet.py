from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

class Wallet:
    @staticmethod
    def generate_keys():
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def get_private_key_hex(private_key):
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_key_bytes.hex()

    @staticmethod
    def get_public_key_hex(public_key):
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return public_key_bytes.hex()

    @staticmethod
    def hash_data(data):
        """
        Hashes the raw data using Blake2b.

        :param data: Data to be hashed, can be str or bytes.
        :return: Hashed data as bytes.
        :raises InvalidDataTypeError: If the data type is not str or bytes.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        digest = hashes.Hash(hashes.BLAKE2b(64))
        digest.update(data)
        return digest.finalize()
    
    @staticmethod
    def sign_data(private_key_hex, data):
        """
        Signe les données hachées en utilisant la clé privée Ed25519.
        """
        private_key_bytes = bytes.fromhex(private_key_hex)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        hashed_data = Wallet.hash_data(data)
        signature = private_key.sign(hashed_data)
        return signature.hex()
    
# Utilisation de la classe Wallet pour générer des clés
private_key, public_key = Wallet.generate_keys()
private_key_hex = Wallet.get_private_key_hex(private_key)
public_key_hex = Wallet.get_public_key_hex(public_key)

print("Clé privée:\n", private_key_hex)
print("Clé publique:\n", public_key_hex)
