"""
Module: Blake2bEd25519Exceptions

Description:
------------
This module defines custom exception classes used in the Blake2bEd25519 module. These exceptions are raised 
for specific error conditions such as invalid data types or signature verification failures.

Classes:
--------
Blake2bEd25519Exception(Exception):
    Base exception class for all exceptions in the Blake2bEd25519 module.

InvalidDataTypeError(Blake2bEd25519Exception):
    Exception raised when the data type provided is invalid.

SignatureVerificationError(Blake2bEd25519Exception):
    Exception raised when signature verification fails.

Classes:
--------
Blake2bEd25519Exception:
    Base class for exceptions in the Blake2bEd25519 module.

    Methods:
    --------
    __init__(self, message=None, *args):
        Initializes the exception with an optional message.

    __str__(self):
        Returns the exception message as a string.

InvalidDataTypeError:
    Exception raised for invalid data types.

    Methods:
    --------
    __init__(self, expected_type, actual_type, message=None):
        Initializes the exception with expected and actual data types, and an optional message.

    __str__(self):
        Returns the exception message, including expected and actual data types.

SignatureVerificationError:
    Exception raised for signature verification failures.

    Methods:
    --------
    __init__(self, message="La vérification de la signature a échoué", *args):
        Initializes the exception with a default or custom message.
"""

class Blake2bEd25519Exception(Exception):
    """Base class for exceptions in the Blake2bEd25519 module."""
    def __init__(self, message=None, *args):
        if message is None:
            message = "An error occurred in the Blake2bEd25519 module."
        self.message = message
        super().__init__(self.message, *args)

    def __str__(self):
        return self.message

class InvalidDataTypeError(Blake2bEd25519Exception):
    """Exception raised for invalid data types."""
    def __init__(self, expected_type, actual_type, message=None):
        if message is None:
            message = f"Invalid data type. Expected: {expected_type}, Got: {actual_type}"
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(message)

    def __str__(self):
        return f"{self.message} (Expected: {self.expected_type}, Got: {self.actual_type})"

class SignatureVerificationError(Blake2bEd25519Exception):
    """Exception raised for signature verification failures."""
    def __init__(self, message="Signature verification failed", *args):
        self.message = message
        super().__init__(self.message, *args)
