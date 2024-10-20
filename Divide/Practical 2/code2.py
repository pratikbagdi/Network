# Function to generate the Playfair cipher key matrix
def generate_key_matrix(key):
    key = key.upper().replace("J", "I")  # Replace 'J' with 'I' as Playfair usually uses a 5x5 matrix
    key_matrix = []
    seen = set()

    # Add key characters to the matrix
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            key_matrix.append(char)

    # Add remaining letters of the alphabet to the matrix
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # 'J' is omitted
        if char not in seen:
            seen.add(char)
            key_matrix.append(char)

    # Convert the list into a 5x5 matrix
    return [key_matrix[i:i + 5] for i in range(0, 25, 5)]


# Function to find the position of a letter in the key matrix
def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None


# Function to preprocess the plaintext (handle repeating characters and add filler)
def preprocess_text(plaintext):
    plaintext = plaintext.upper().replace("J", "I")  # Replace 'J' with 'I'
    processed = ""

    i = 0
    while i < len(plaintext):
        char1 = plaintext[i]
        if i + 1 < len(plaintext):
            char2 = plaintext[i + 1]
        else:
            char2 = 'X'  # Add filler if it's the last letter

        if char1 == char2:
            processed += char1 + 'X'  # Insert 'X' between repeated letters
            i += 1
        else:
            processed += char1 + char2
            i += 2

    if len(processed) % 2 != 0:
        processed += 'X'  # Add filler if the text length is odd

    return processed


# Function to encrypt/decrypt a digraph (pair of letters)
def process_digraph(matrix, char1, char2, encrypt=True):
    row1, col1 = find_position(matrix, char1)
    row2, col2 = find_position(matrix, char2)

    if row1 == row2:  # Same row
        if encrypt:
            return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        else:
            return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:  # Same column
        if encrypt:
            return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:  # Rectangle case
        return matrix[row1][col2] + matrix[row2][col1]


# Function to encrypt plaintext using Playfair cipher
def encrypt(plaintext, key):
    key_matrix = generate_key_matrix(key)
    plaintext = preprocess_text(plaintext)
    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        ciphertext += process_digraph(key_matrix, plaintext[i], plaintext[i + 1], encrypt=True)

    return ciphertext


# Function to decrypt ciphertext using Playfair cipher
def decrypt(ciphertext, key):
    key_matrix = generate_key_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        plaintext += process_digraph(key_matrix, ciphertext[i], ciphertext[i + 1], encrypt=False)

    return plaintext


# Main program
def main():
    print("Playfair Cipher")
    key = input("Enter the key: ")
    choice = input("Encrypt or Decrypt (e/d): ").lower()

    if choice == 'e':
        plaintext = input("Enter the plaintext: ")
        ciphertext = encrypt(plaintext, key)
        print(f"Ciphertext: {ciphertext}")
    elif choice == 'd':
        ciphertext = input("Enter the ciphertext: ")
        plaintext = decrypt(ciphertext, key)
        print(f"Plaintext: {plaintext}")
    else:
        print("Invalid choice. Please enter 'e' to encrypt or 'd' to decrypt.")


if __name__ == "__main__":
    main()
