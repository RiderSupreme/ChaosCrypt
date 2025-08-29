from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Optimized Python functions
def logistic_map(x0, n, prev_state=None):
    """Optimized logistic map that can continue from a previous state"""
    r = 3.99999

    if prev_state is None:
        # Initial warmup
        x = x0
        for _ in range(100):
            x = r * x * (1 - x)
    else:
        # Continue from previous state
        x = prev_state

    # Calculate the next value for the sequence
    x = r * x * (1 - x)
    x = (x + x0) % 1.0

    return x


def encrypt(message, x0, mode, x1=None):
    """Optimized encryption that avoids recalculating the sequence for each character"""
    encrypted = []

    # Initialize state for first encryption
    state = x0
    # Initial warmup
    for _ in range(100):
        state = 3.99999 * state * (1 - state)

    # Encrypt each character
    for char in message:
        state = 3.99999 * state * (1 - state)
        state = (state + x0) % 1.0
        chaos = int(state * 1000) % 256
        encrypted_char = (ord(char) + chaos) % 256
        encrypted.append(encrypted_char)

    # Double encryption
    if mode == "double":
        double_encrypted = []

        # Initialize state for second encryption
        state2 = x1
        # Initial warmup
        for _ in range(100):
            state2 = 3.99999 * state2 * (1 - state2)

        # Apply second encryption
        for num in encrypted:
            state2 = 3.99999 * state2 * (1 - state2)
            state2 = (state2 + x1) % 1.0
            chaos = int(state2 * 1000) % 256
            double_encrypted_char = (num + chaos) % 256
            double_encrypted.append(double_encrypted_char)

        return double_encrypted

    return encrypted


def decrypt(encrypted, x0, mode, x1=None):
    """Optimized decryption that matches the optimized encryption"""
    if mode == "double":
        partially_decrypted = []

        # Initialize state for first decryption (of second encryption)
        state2 = x1
        # Initial warmup
        for _ in range(100):
            state2 = 3.99999 * state2 * (1 - state2)

        # Apply first decryption
        for num in encrypted:
            state2 = 3.99999 * state2 * (1 - state2)
            state2 = (state2 + x1) % 1.0
            chaos = int(state2 * 1000) % 256
            decrypted_char = (num - chaos) % 256
            partially_decrypted.append(decrypted_char)

        encrypted = partially_decrypted

    # Initialize state for main decryption
    state = x0
    # Initial warmup
    for _ in range(100):
        state = 3.99999 * state * (1 - state)

    # Decrypt each character
    decrypted = ''
    for num in encrypted:
        state = 3.99999 * state * (1 - state)
        state = (state + x0) % 1.0
        chaos = int(state * 1000) % 256
        decrypted_char = (num - chaos) % 256
        decrypted += chr(decrypted_char)

    return decrypted


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')


@app.route('/credits')
def credits():
    return render_template('credits.html')


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    if request.method == 'POST':
        message = request.form['message']
        mode = request.form['mode']
        seed1 = float(request.form['seed1'])
        seed2 = float(request.form['seed2']) if mode == "double" else None
        encrypted = encrypt(message, seed1, mode, seed2)
        return render_template('encrypt.html',
                               result=f"Encrypted message: {encrypted}")
    return render_template('encrypt.html')


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    if request.method == 'POST':
        try:
            encrypted_str = request.form['encrypted']
            encrypted_list = [
                int(x.strip()) for x in encrypted_str.strip('[]').split(',')
            ]
            mode = request.form['mode']
            seed1 = float(request.form['seed1'])
            seed2 = float(request.form['seed2']) if mode == "double" else None
            decrypted = decrypt(encrypted_list, seed1, mode, seed2)
            return render_template('decrypt.html',
                                   result=f"Decrypted message: {decrypted}")
        except Exception as e:
            return render_template('decrypt.html', result=f"Error: {str(e)}")
    return render_template('decrypt.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
