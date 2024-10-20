import hashlib
import random

def create_signature(message, secret_key):
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    signature = message_hash + secret_key
    return signature

def verify_signature(message, secret_key, signature):
    expected_signature = create_signature(message, secret_key)
    return expected_signature == signature

def generate_keys():
    private_key = random.randint(1, 100)
    public_key = private_key + 2
    return private_key, public_key

def rsa_sign(message, private_key):
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    return message_hash + str(private_key)

def rsa_verify(message, signature, public_key):
    expected_signature = rsa_sign(message, public_key - 2)
    return expected_signature == signature

message = input("Enter the message: ")
secret_key = input("Enter your secret key: ")

simple_signature = create_signature(message, secret_key)
print(f"Simple Signature: {simple_signature}")

is_verified = verify_signature(message, secret_key, simple_signature)
print(f"Signature verified: {is_verified}")

private_key, public_key = generate_keys()
rsa_signature = rsa_sign(message, private_key)
print(f"RSA Signature: {rsa_signature}")

is_rsa_verified = rsa_verify(message, rsa_signature, public_key)
print(f"RSA Signature verified: {is_rsa_verified}")
