from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)


def logistic_map(x0, n):
    r = 3.99999999999999999999999999999999999999999
    x = x0
    for _ in range(100):
        x = r * x * (1 - x)
    for _ in range(n):
        x = r * x * (1 - x)
        x = (x + x0) % 1.0
    return x


def encrypt(message, x0, mode, x1=None):
    encrypted = []
    for i, char in enumerate(message):
        x = logistic_map(x0, i + 1)
        chaos = int(x * 1000) % 256
        encrypted_char = (ord(char) + chaos) % 256
        encrypted.append(encrypted_char)
    if mode == "double":
        double_encrypted = []
        for i, num in enumerate(encrypted):
            x = logistic_map(x1, i + 1)
            chaos = int(x * 1000) % 256
            double_encrypted_char = (num + chaos) % 256
            double_encrypted.append(double_encrypted_char)
        return double_encrypted
    return encrypted


def decrypt(encrypted, x0, mode, x1=None):
    if mode == "double":
        partially_decrypted = []
        for i, num in enumerate(encrypted):
            x = logistic_map(x1, i + 1)
            chaos = int(x * 1000) % 256
            decrypted_char = (num - chaos) % 256
            partially_decrypted.append(decrypted_char)
        encrypted = partially_decrypted

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
            background-color: #d43d22;
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            max-width: 700px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 500;
        }
        textarea, input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }
        textarea:focus, input[type="number"]:focus {
            outline: none;
            border-color: #3498db;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        .button {
            flex: 1;
            background-color: #3498db;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            font-size: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        .button.primary {
            background-color: #2ecc71;
        }
        .button.secondary {
            background-color: #7f8c8d;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
        }
        .result h3 {
            color: #2c3e50;
            margin-top: 0;
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
                <label>Mode:</label>
                <select name="mode" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px; margin-bottom: 15px;">
                    <option value="single">Single Encryption</option>
                    <option value="double">Double Encryption</option>
                </select>
            </div>
            <div class="form-group">
                <label>First Seed (Any Rational Number Between 0 And 1):</label>
                <input type="number" name="seed1" step="any" required>
            </div>
            <div class="form-group" id="seed2Group" style="display: none;">
                <label>Second Seed (Any Rational Number Between 0 And 1):</label>
                <input type="number" name="seed2" step="any">
            </div>
            <script>
                document.querySelector('select[name="mode"]').addEventListener('change', function() {
                    document.getElementById('seed2Group').style.display = 
                        this.value === 'double' ? 'block' : 'none';
                });
            </script>
            <div class="button-group">
                <button type="submit" class="button primary">Encrypt</button>
                <a href="/" class="button secondary">Back to Home</a>
            </div>
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            max-width: 700px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.2em;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 500;
        }
        textarea, input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }
        textarea:focus, input[type="number"]:focus {
            outline: none;
            border-color: #3498db;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        .button {
            flex: 1;
            background-color: #3498db;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            font-size: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        .button.primary {
            background-color: #2ecc71;
        }
        .button.secondary {
            background-color: #7f8c8d;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
        }
        .result h3 {
            color: #2c3e50;
            margin-top: 0;
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
                <label>Mode:</label>
                <select name="mode" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px; margin-bottom: 15px;">
                    <option value="single">Single Encryption</option>
                    <option value="double">Double Encryption</option>
                </select>
            </div>
            <div class="form-group">
                <label>First Seed (Any Rational Number Between 0 And 1):</label>
                <input type="number" name="seed1" step="any" required>
            </div>
            <div class="form-group" id="seed2Group" style="display: none;">
                <label>Second Seed (Any Rational Number Between 0 And 1):</label>
                <input type="number" name="seed2" step="any">
            </div>
            <script>
                document.querySelector('select[name="mode"]').addEventListener('change', function() {
                    document.getElementById('seed2Group').style.display = 
                        this.value === 'double' ? 'block' : 'none';
                });
            </script>
            <div class="button-group">
                <button type="submit" class="button primary">Decrypt</button>
                <a href="/" class="button secondary">Back to Home</a>
            </div>
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
        mode = request.form['mode']
        seed1 = float(request.form['seed1'])
        seed2 = float(request.form['seed2']) if mode == "double" else None
        encrypted = encrypt(message, seed1, mode, seed2)
        return render_template_string(ENCRYPT_TEMPLATE,
                                      result=f"Encrypted message: {encrypted}")
    return render_template_string(ENCRYPT_TEMPLATE)


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
            return render_template_string(
                DECRYPT_TEMPLATE, result=f"Decrypted message: {decrypted}")
        except Exception as e:
            return render_template_string(DECRYPT_TEMPLATE,
                                          result=f"Error: {str(e)}")
    return render_template_string(DECRYPT_TEMPLATE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
