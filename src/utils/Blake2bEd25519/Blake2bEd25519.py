"""
Module: Blake2bEd25519

Description:
------------
This module provides functionality for hashing data using the Blake2b algorithm and verifying signatures 
using the Ed25519 algorithm. It includes methods to hash data, verify signatures from hashed data, and 
verify signatures directly from raw data.

Classes:
--------
Blake2bEd25519:
    A class that provides static methods to:
        - Hash data using Blake2b.
        - Verify Ed25519 signatures from hashed data.
        - Verify Ed25519 signatures from raw data.

Methods:
--------
Blake2bEd25519.hash_data(data):
    Hashes the input data using Blake2b.

    Parameters:
        data (str or bytes): The data to be hashed. Can be either a string or bytes.

    Returns:
        bytes: The hashed data.

    Raises:
        InvalidDataTypeError: If the data is not of type str or bytes.

Blake2bEd25519.verify_signature_from_hash(public_key_pem, hashed_data, signature):
    Verifies an Ed25519 signature against the hashed data using the provided public key.

    Parameters:
        public_key_pem (bytes): The public key in PEM format.
        hashed_data (bytes): The hashed data to verify.
        signature (bytes): The signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        InvalidDataTypeError: If the types of the parameters are incorrect.
        SignatureVerificationError: If the signature verification fails.
        Blake2bEd25519Exception: If there is an error loading the public key or verifying the signature.

Blake2bEd25519.verify_signature_from_raw_data(public_key_pem, data, signature):
    Verifies an Ed25519 signature against the raw data using the provided public key. 
    The raw data is first hashed using Blake2b before verification.

    Parameters:
        public_key_pem (bytes): The public key in PEM format.
        data (bytes): The raw data to verify.
        signature (bytes): The signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        InvalidDataTypeError: If the types of the parameters are incorrect.
        SignatureVerificationError: If the signature verification fails.
        Blake2bEd25519Exception: If there is an error hashing the data or verifying the signature.

Exceptions:
-----------
Blake2bEd25519Exception:
    Base exception class for errors in the Blake2bEd25519 module.

InvalidDataTypeError:
    Raised when the provided data type is invalid.

SignatureVerificationError:
    Raised when signature verification fails.
"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

from exception.Blake2bEd25519Exception import Blake2bEd25519Exception, InvalidDataTypeError, SignatureVerificationError

class Blake2bEd25519:
    @staticmethod
    def hash_data(data):
        """
        Hashes the raw data using Blake2b.

        :param data: Data to be hashed, can be str or bytes.
        :return: Hashed data as bytes.
        :raises InvalidDataTypeError: If the data type is not str or bytes.
        """
        if not isinstance(data, (str, bytes)):
            raise InvalidDataTypeError(expected_type="str or bytes", actual_type=type(data).__name__)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        digest = hashes.Hash(hashes.BLAKE2b(64), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    @staticmethod
    def verify_signature_from_hash(public_key_pem: bytes, hashed_data: bytes, signature: bytes):
        """
        Verifies if the hashed data is signed with Ed25519 using the public key.

        :param public_key_pem: Public key in PEM format.
        :param hashed_data: Hashed data to verify.
        :param signature: Signature to verify.
        :return: True if the signature is valid, False otherwise.
        :raises InvalidDataTypeError: If the argument types are incorrect.
        :raises SignatureVerificationError: If the signature verification fails.
        """
        if not isinstance(public_key_pem, bytes) or not isinstance(hashed_data, bytes) or not isinstance(signature, bytes):
            raise InvalidDataTypeError(expected_type="bytes", actual_type=f"public_key_pem: {type(public_key_pem).__name__}, hashed_data: {type(hashed_data).__name__}, signature: {type(signature).__name__}")
        
        try:
            public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
            if not isinstance(public_key, ed25519.Ed25519PublicKey):
                raise InvalidDataTypeError(expected_type="Ed25519PublicKey", actual_type=type(public_key).__name__)
            
            public_key.verify(signature, hashed_data)
            return True
        except InvalidSignature:
            raise SignatureVerificationError()
        except (ValueError, TypeError) as e:
            raise Blake2bEd25519Exception(f"Error loading the public key or verifying the signature: {str(e)}")

    @staticmethod
    def verify_signature_from_raw_data(public_key_pem: bytes, data: bytes, signature: bytes):
        """
        Verifies if the raw data is signed with Ed25519 using the public key.

        :param public_key_pem: Public key in PEM format.
        :param data: Raw data to verify.
        :param signature: Signature to verify.
        :return: True if the signature is valid, False otherwise.
        :raises InvalidDataTypeError: If the argument types are incorrect.
        :raises SignatureVerificationError: If the signature verification fails.
        """
        if not isinstance(public_key_pem, bytes) or not isinstance(data, bytes) or not isinstance(signature, bytes):
            raise InvalidDataTypeError(expected_type="bytes", actual_type=f"public_key_pem: {type(public_key_pem).__name__}, data: {type(data).__name__}, signature: {type(signature).__name__}")
        
        try:
            hashed_data = Blake2bEd25519.hash_data(data)
            return Blake2bEd25519.verify_signature_from_hash(public_key_pem, hashed_data, signature)
        except (ValueError, TypeError) as e:
            raise Blake2bEd25519Exception(f"Error hashing the data or verifying the signature: {str(e)}")
