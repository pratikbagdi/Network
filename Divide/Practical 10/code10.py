import hashlib

def calculate_sha256(input_string):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    sha256_hash.update(input_string.encode('utf-8'))

    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

# Get user input
user_input = input("Enter a string to hash with SHA-256: ")

# Calculate and display the SHA-256 hash
hash_result = calculate_sha256(user_input)
print(f"SHA-256 Hash: {hash_result}")
