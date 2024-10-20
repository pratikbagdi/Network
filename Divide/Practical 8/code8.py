import random


def generate_prime(bits=8):
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    if phi == 1:
        return 0
    while e > 1:
        q = e // phi
        t = phi
        phi = e % phi
        e = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    # Make x1 positive
    if x1 < 0:
        x1 += m0
    return x1


def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(plaintext, public_key):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext


def main():
    public_key, private_key = generate_keys()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    plaintext = input("Enter the Plaintext: ").strip()
    print(f"Plaintext: {plaintext}")

    ciphertext = encrypt(plaintext, public_key)
    print(f"Encrypted text: {ciphertext}")

    decrypted_text = decrypt(ciphertext, private_key)
    print(f"Decrypted text: {decrypted_text}")


if __name__ == "__main__":
    main()
