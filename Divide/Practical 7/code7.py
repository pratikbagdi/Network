import random


# Function to generate a prime number
def generate_prime():
    # Using a simple method to generate a prime number
    prime_candidates = [17, 19, 23, 29, 31, 37, 41, 43, 47]
    return random.choice(prime_candidates)


# Function to generate a primitive root
def generate_primitive_root(prime):
    roots = []
    for g in range(2, prime):
        if len(set(pow(g, powers, prime) for powers in range(1, prime))) == prime - 1:
            roots.append(g)
    return random.choice(roots)


# Function to compute the shared secret
def diffie_hellman(private_key_a, private_key_b, prime, primitive_root):
    public_key_a = pow(primitive_root, private_key_a, prime)
    public_key_b = pow(primitive_root, private_key_b, prime)

    shared_secret_a = pow(public_key_b, private_key_a, prime)
    shared_secret_b = pow(public_key_a, private_key_b, prime)

    return shared_secret_a, shared_secret_b


# Simple XOR encryption/decryption function
def xor_encrypt_decrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)


def main():
    # Generate prime and primitive root
    prime = generate_prime()
    primitive_root = generate_primitive_root(prime)

    print(f"Prime: {prime}, Primitive Root: {primitive_root}")

    # User inputs for private keys
    private_key_a = int(input("User A, enter your private key: "))
    private_key_b = int(input("User B, enter your private key: "))

    # Compute the shared secret
    shared_secret_a, shared_secret_b = diffie_hellman(private_key_a, private_key_b, prime, primitive_root)

    print(f"Shared Secret (User A): {shared_secret_a}")
    print(f"Shared Secret (User B): {shared_secret_b}")

    # Use the shared secret as a symmetric key (simplified for demonstration)
    symmetric_key = shared_secret_a % 256  # Use modulo to keep key in byte range
    print(f"Symmetric Key: {symmetric_key}")

    # Encrypt and decrypt a message
    message = input("Enter a message to encrypt: ")
    encrypted_message = xor_encrypt_decrypt(message, symmetric_key)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = xor_encrypt_decrypt(encrypted_message, symmetric_key)
    print(f"Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    main()
