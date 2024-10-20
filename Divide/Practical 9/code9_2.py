import hashlib
import random


# Generate a simple hash for the message
def create_signature(message):
    # Create a SHA-256 hash of the message
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    return message_hash


# Simple implementation of signing a message (not a secure method)
def sign_message(message):
    private_key = random.randint(1, 100)  # Simulating a private key
    signature = create_signature(message) + str(private_key)  # Combine hash with private key
    return signature, private_key


# Verify the signature
def verify_signature(message, signature):
    # Extract the original signature (hash) and private key
    original_hash = signature[:-2]
    private_key = int(signature[-2:])

    # Recreate the signature from the message
    recreated_signature = create_signature(message) + str(private_key)

    return recreated_signature == signature


# Main function
def main():
    # User input
    message = input("Enter a message to sign: ")

    # Sign the message
    signature, private_key = sign_message(message)
    print(f"Signature: {signature}")

    # Verification
    verification_result = verify_signature(message, signature)
    if verification_result:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")


if __name__ == "__main__":
    main()
