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

# Get message from user input and set initial seed
original_message = input("Enter your message to encrypt: ")
x0 = 0.123456  # Initial value (x⁰), must be kept secret between sender and receiver

# Encrypt the message
encrypted_message = encrypt(original_message, x0)

# Decrypt it back
decrypted_message = decrypt(encrypted_message, x0)

# Output the results
print("=== CHAOS-BASED ENCRYPTION DEMO ===")
print(f"Original Message     : {original_message}")
print(f"Initial Seed (x⁰)    : {x0}")
print(f"Encrypted (as ints)  : {encrypted_message}")
print(f"Decrypted Message    : {decrypted_message}")