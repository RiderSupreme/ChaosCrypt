
from flask import Flask, render_template_string, request

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

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chaos-Based Encryption/Decryption</title>
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
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"], input[type="number"], textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
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
        <h1>Chaos-Based Cryptography</h1>
        
        <div class="form-group">
            <form method="POST" action="/encrypt">
                <h2>Encryption</h2>
                <label>Message to Encrypt:</label>
                <textarea name="message" rows="4" required></textarea>
                <label>Initial Seed (between 0 and 1):</label>
                <input type="number" name="seed" step="0.000001" min="0" max="1" required>
                <button type="submit">Encrypt</button>
            </form>
        </div>

        <div class="form-group">
            <form method="POST" action="/decrypt">
                <h2>Decryption</h2>
                <label>Encrypted Message (comma-separated numbers):</label>
                <textarea name="encrypted" rows="4" required></textarea>
                <label>Initial Seed (between 0 and 1):</label>
                <input type="number" name="seed" step="0.000001" min="0" max="1" required>
                <button type="submit">Decrypt</button>
            </form>
        </div>

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
    return render_template_string(HTML_TEMPLATE)

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    message = request.form['message']
    seed = float(request.form['seed'])
    encrypted = encrypt(message, seed)
    return render_template_string(HTML_TEMPLATE, result=f"Encrypted message: {encrypted}")

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        encrypted_str = request.form['encrypted']
        encrypted_list = [int(x.strip()) for x in encrypted_str.strip('[]').split(',')]
        seed = float(request.form['seed'])
        decrypted = decrypt(encrypted_list, seed)
        return render_template_string(HTML_TEMPLATE, result=f"Decrypted message: {decrypted}")
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
