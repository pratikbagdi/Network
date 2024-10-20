class Blowfish:
    def __init__(self, key):
        self.P = [0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,
                  0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89,
                  0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
                  0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917,
                  0x9216D5D9, 0x8979FB1B]
        self.S = [0xD1310BA6, 0x98DFB5AC, 0x2FFD72DB, 0xD01ADFB7,
                  0xB8E1AFED, 0x6A267E96, 0xBA7C9045, 0xF12C7F99,
                  0x24A19947, 0xB3916CF7, 0x0801F2E2, 0x858EFC16,
                  0x636920D8, 0x71574E69, 0xA458FEA3, 0xF4933D7E]

    def F(self, x):
        return ((self.S[0] + x) * self.S[1]) & 0xFFFFFFFF

    def encrypt_block(self, L, R):
        for i in range(16):
            L = L ^ self.P[i]
            R = self.F(L) ^ R
            L, R = R, L
        L, R = R, L
        R = R ^ self.P[16]
        L = L ^ self.P[17]
        return L, R

    def decrypt_block(self, L, R):
        for i in range(17, 1, -1):
            L = L ^ self.P[i]
            R = self.F(L) ^ R
            L, R = R, L
        L, R = R, L
        R = R ^ self.P[1]
        L = L ^ self.P[0]
        return L, R

    def encrypt(self, plaintext):
        L = int.from_bytes(plaintext[:4].encode(), byteorder='big')
        R = int.from_bytes(plaintext[4:].encode(), byteorder='big')
        L, R = self.encrypt_block(L, R)
        return (L.to_bytes(4, byteorder='big') + R.to_bytes(4,byteorder='big')).hex()

    def decrypt(self, ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        L = int.from_bytes(ciphertext[:4], byteorder='big')
        R = int.from_bytes(ciphertext[4:], byteorder='big')
        L, R = self.decrypt_block(L, R)
        return (L.to_bytes(4, byteorder='big') + R.to_bytes(4,byteorder='big')).decode()

def main():
    key = "simplekey"
    plaintext = "hello123"
    blowfish = Blowfish(key)
    print(f"Plaintext: {plaintext}")
    encrypted_text = blowfish.encrypt(plaintext)
    print(f"Encrypted text: {encrypted_text}")
    decrypted_text = blowfish.decrypt(encrypted_text)
    print(f"Decrypted text: {decrypted_text}")

if __name__ == "__main__":
    main()
