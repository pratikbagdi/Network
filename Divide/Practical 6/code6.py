# Simplified S-box for AES
s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf1, 0x7d, 0x22, 0xb6, 0xbf, 0x12, 0x98,
    0x48, 0xa9, 0xa7, 0xa4, 0xf5, 0x4b, 0xa0, 0xe8
]

def substitute_bytes(byte, s_box):
    """Substitute bytes using the given S-box."""
    if 0 <= byte < len(s_box):
        return s_box[byte]
    else:
        raise IndexError("Byte value is out of range for substitution.")

def add_round_key(state, round_key):
    """Add round key to state (XOR operation)."""
    return [s ^ k for s, k in zip(state, round_key)]

def aes_encrypt(plaintext, key):
    """Encrypt plaintext using a simplified AES-like algorithm."""
    key = [ord(c) for c in key]
    plaintext = [ord(c) for c in plaintext]

    # Ensure plaintext length is a multiple of 16
    while len(plaintext) % 16 != 0:
        plaintext.append(0)  # Pad with zeroes

    encrypted_text = ""

    # Process 16-byte blocks
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        state = block

        # Step 1: Add round key (XOR with key)
        state = add_round_key(state, key)

        # Step 2: Substitute bytes using S-box
        try:
            state = [substitute_bytes(b, s_box) for b in state]
        except IndexError as e:
            print(f"ERROR! {e}")
            return None

        # Convert to encrypted characters
        encrypted_text += ''.join(chr(b) for b in state)

    return encrypted_text

def aes_decrypt(ciphertext, key):
    """Decrypt ciphertext (reverse of simplified encryption)."""
    key = [ord(c) for c in key]
    ciphertext = [ord(c) for c in ciphertext]

    decrypted_text = ""

    # Process 16-byte blocks
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        state = block

        # Step 1: Reverse Substitute bytes using S-box (reverse process)
        state = [s_box.index(b) for b in state]

        # Step 2: Reverse Add round key (XOR with key)
        state = add_round_key(state, key)

        # Convert to decrypted characters
        decrypted_text += ''.join(chr(b) for b in state)

    return decrypted_text.strip('\x00')  # Remove padding

def main():
    key = input("Enter a 16-character key: ")
    if len(key) != 16:
        print("Key must be exactly 16 characters!")
        return

    plaintext = input("Enter the message to encrypt (max 16 characters): ")
    if len(plaintext) > 16:
        print("Message should not exceed 16 characters.")
        return

    print(f"\nPlain text: {plaintext}")

    # Encryption
    encrypted_text = aes_encrypt(plaintext, key)
    if encrypted_text is None:
        return
    print(f"Encrypted text: {''.join(hex(ord(c))[2:] for c in encrypted_text)}")

    # Decryption
    decrypted_text = aes_decrypt(encrypted_text, key)
    print(f"Decrypted text: {decrypted_text}")

if __name__ == "__main__":
    main()
