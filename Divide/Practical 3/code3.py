import math

def get_key_matrix_from_word(word, n):
    word = word.upper().replace(" ", "")
    key_numbers = [ord(char) - ord('A') for char in word if char.isalpha()]

    if len(key_numbers) < n * n:
        print(f"Key too short, padding with 'A'.")
        key_numbers += [0] * (n * n - len(key_numbers))  # Pad with 'A' (i.e., 0)
    elif len(key_numbers) > n * n:
        print(f"Key too long, truncating.")
        key_numbers = key_numbers[:n * n]  # Truncate extra characters

    key_matrix = []
    for i in range(n):
        key_matrix.append(key_numbers[i * n: (i + 1) * n])

    return key_matrix


def text_to_numbers(text):
    text = text.upper()
    numbers = [ord(char) - ord('A') for char in text if char.isalpha()]
    return numbers


def numbers_to_text(numbers):
    text = ''.join([chr(num % 26 + ord('A')) for num in numbers])
    return text


def matrix_multiply_modulo(matrix, vector, modulus):
    n = len(matrix)
    result = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += matrix[i][j] * vector[j]
        result.append(s % modulus)
    return result


def matrix_determinant(matrix):
    n = len(matrix)
    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        det = a * d - b * c
    elif n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        det = (a * e * i + b * f * g + c * d * h) - (c * e * g + b * d * i + a * f * h)
    else:
        print("Determinant not implemented for matrices larger than 3x3.")
        return None
    return det % 26


def modular_inverse(a, modulus):
    a = a % modulus
    for x in range(1, modulus):
        if (a * x) % modulus == 1:
            return x
    return None


def matrix_inverse_modulo(matrix, modulus):
    n = len(matrix)
    det = matrix_determinant(matrix)
    det_inv = modular_inverse(det, modulus)
    if det_inv is None:
        print(f"Determinant {det} has no inverse modulo {modulus}.")
        return None
    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        # Compute adjugate matrix
        adjugate = [[d, -b], [-c, a]]
        # Bring adjugate elements into the range [0, modulus)
        for i in range(n):
            for j in range(n):
                adjugate[i][j] = adjugate[i][j] % modulus
        # Multiply adjugate by determinant inverse modulo modulus
        inverse = []
        for row in adjugate:
            inverse_row = [(det_inv * element) % modulus for element in row]
            inverse.append(inverse_row)
        return inverse
    else:
        print("Matrix inverse not implemented for matrices larger than 2x2.")
        return None


def prepare_text(text, block_size):
    numbers = text_to_numbers(text)
    if len(numbers) % block_size != 0:
        padding_length = block_size - (len(numbers) % block_size)
        numbers += [text_to_numbers('X')[0]] * padding_length
    return numbers


def encrypt(plaintext_numbers, key_matrix, modulus):
    n = len(key_matrix)
    ciphertext_numbers = []
    for i in range(0, len(plaintext_numbers), n):
        block = plaintext_numbers[i:i + n]
        cipher_block = matrix_multiply_modulo(key_matrix, block, modulus)
        ciphertext_numbers.extend(cipher_block)
    return ciphertext_numbers


def decrypt(ciphertext_numbers, inverse_key_matrix, modulus):
    n = len(inverse_key_matrix)
    plaintext_numbers = []
    for i in range(0, len(ciphertext_numbers), n):
        block = ciphertext_numbers[i:i + n]
        plain_block = matrix_multiply_modulo(inverse_key_matrix, block, modulus)
        plaintext_numbers.extend(plain_block)
    return plaintext_numbers


def main():
    modulus = 26
    print("Hill Cipher Encryption and Decryption")
    word_key = input("Enter the word key: ")
    n = 2  # Only support 2x2 matrices for now
    key_matrix = get_key_matrix_from_word(word_key, n)

    print("Key Matrix:")
    for row in key_matrix:
        print(row)

    det = matrix_determinant(key_matrix)
    det_inv = modular_inverse(det, modulus)
    if det_inv is None:
        print(f"The determinant ({det}) is not invertible modulo {modulus}. Cannot proceed.")
        return

    plaintext = input("Enter the plaintext: ")
    plaintext_numbers = prepare_text(plaintext, n)
    ciphertext_numbers = encrypt(plaintext_numbers, key_matrix, modulus)
    ciphertext = numbers_to_text(ciphertext_numbers)
    print("Ciphertext:", ciphertext)

    # Now, decrypt
    inverse_key_matrix = matrix_inverse_modulo(key_matrix, modulus)
    if inverse_key_matrix is None:
        print("Cannot compute inverse key matrix. Decryption not possible.")
        return
    decrypted_numbers = decrypt(ciphertext_numbers, inverse_key_matrix, modulus)
    decrypted_text = numbers_to_text(decrypted_numbers)
    print("Decrypted text:", decrypted_text)


if __name__ == "__main__":
    main()
