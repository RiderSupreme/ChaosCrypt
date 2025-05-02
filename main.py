
def logistic_map(x0, n):
    x = x0
    for _ in range(n):
        x = 4 * x * (1 - x)
    return x

def encrypt(message, x0):
    encrypted = []
    for i, char in enumerate(message):
        x = logistic_map(x0, i + 1)
        chaos = int(x * 1000) % 256
        encrypted_char = (ord(char) + chaos) % 256
        encrypted.append(encrypted_char)
    return encrypted

def decrypt(encrypted, x0):
    decrypted = ''
    for i, num in enumerate(encrypted):
        x = logistic_map(x0, i + 1)
        chaos = int(x * 1000) % 256
        decrypted_char = (num - chaos) % 256
        decrypted += chr(decrypted_char)
    return decrypted

# --- Demonstration ---
print("=== CHAOS-BASED ENCRYPTION/DECRYPTION ===")
mode = input("Choose mode (1 for encryption, 2 for decryption): ")

if mode == "1":
    # Encryption mode
    message = input("Enter your message to encrypt: ")
    x0 = float(input("Enter initial seed (between 0 and 1): "))
    encrypted_message = encrypt(message, x0)
    print(f"\nEncrypted message (as ints): {encrypted_message}")

elif mode == "2":
    # Decryption mode
    encrypted_str = input("Enter the encrypted message (comma-separated numbers): ")
    encrypted_list = [int(x.strip()) for x in encrypted_str.strip('[]').split(',')]
    x0 = float(input("Enter initial seed (between 0 and 1): "))
    decrypted_message = decrypt(encrypted_list, x0)
    print(f"\nDecrypted message: {decrypted_message}")

else:
    print("Invalid mode selected!")
