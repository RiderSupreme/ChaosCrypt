from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

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

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chaos-Based Cryptography</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { color: #333; }
        .button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            margin: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            font-size: 16px;
        }
        .button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chaos-Based Cryptography</h1>
        <h2>Choose Operation</h2>
        <a href="/encrypt" class="button">Encryption</a>
        <a href="/decrypt" class="button">Decryption</a>
    </div>
</body>
</html>
'''

ENCRYPT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Encryption - Chaos-Based Cryptography</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        textarea, input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        .button:hover { background-color: #45a049; }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Encryption</h1>
        <form method="POST">
            <div class="form-group">
                <label>Message to Encrypt:</label>
                <textarea name="message" rows="4" required></textarea>
            </div>
            <div class="form-group">
                <label>Initial Seed (between 0 and 1):</label>
                <input type="number" name="seed" step="0.000000001" min="0" max="1" required>
            </div>
            <button type="submit" class="button">Encrypt</button>
            <a href="/" class="button">Back to Home</a>
        </form>
        {% if result %}
        <div class="result">
            <h3>Result:</h3>
            <p>{{ result }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

DECRYPT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Decryption - Chaos-Based Cryptography</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        textarea, input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        .button:hover { background-color: #45a049; }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Decryption</h1>
        <form method="POST">
            <div class="form-group">
                <label>Encrypted Message (comma-separated numbers):</label>
                <textarea name="encrypted" rows="4" required></textarea>
            </div>
            <div class="form-group">
                <label>Initial Seed (between 0 and 1):</label>
                <input type="number" name="seed" step="0.000000001" min="0" max="1" required>
            </div>
            <button type="submit" class="button">Decrypt</button>
            <a href="/" class="button">Back to Home</a>
        </form>
        {% if result %}
        <div class="result">
            <h3>Result:</h3>
            <p>{{ result }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    if request.method == 'POST':
        message = request.form['message']
        seed = float(request.form['seed'])
        encrypted = encrypt(message, seed)
        return render_template_string(ENCRYPT_TEMPLATE, result=f"Encrypted message: {encrypted}")
    return render_template_string(ENCRYPT_TEMPLATE)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    if request.method == 'POST':
        try:
            encrypted_str = request.form['encrypted']
            encrypted_list = [int(x.strip()) for x in encrypted_str.strip('[]').split(',')]
            seed = float(request.form['seed'])
            decrypted = decrypt(encrypted_list, seed)
            return render_template_string(DECRYPT_TEMPLATE, result=f"Decrypted message: {decrypted}")
        except Exception as e:
            return render_template_string(DECRYPT_TEMPLATE, result=f"Error: {str(e)}")
    return render_template_string(DECRYPT_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)