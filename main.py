from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Your existing Python functions remain unchanged
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
    <title>Chaos Cryptography</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: #000;
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        #bgCanvas {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 0;
        }

        .hero {
            position: relative;
            z-index: 1;
        }

        .animate-text, .animate-up {
            opacity: 0;
        }

        .nav {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
        }

        .logo {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
            -webkit-background-clip: text;
            color: transparent;
        }

        .nav-links a {
            color: #fff;
            text-decoration: none;
            margin-left: 30px;
            font-size: 16px;
            opacity: 0.8;
            transition: opacity 0.3s;
        }

        .nav-links a:hover {
            opacity: 1;
        }

        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0 20px;
            background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
        }

        .hero h1 {
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
            -webkit-background-clip: text;
            color: transparent;
        }

        .hero p {
            font-size: 20px;
            max-width: 600px;
            margin-bottom: 40px;
            opacity: 0.8;
            line-height: 1.6;
        }

        .cta-buttons {
            display: flex;
            gap: 20px;
        }

        .button {
            padding: 15px 30px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 500;
            text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .button:hover {
            transform: translateY(-2px);
        }

        .primary {
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
            color: #fff;
            box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3);
        }

        .secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
        }
            .hero-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                width: 100%;
                max-width: 800px;
                z-index: 2;
            }
            .glitch {
                position: relative;

        }
        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
            -webkit-background-clip: text;
            color: transparent;
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="logo">CHAOSCRYPT</div>
        <div class="nav-links">
            <a href="/encrypt">Encrypt</a>
            <a href="/decrypt">Decrypt</a>
            <a href="/how-it-works">Learn More</a>
        </div>
    </nav>

    <canvas id="bgCanvas"></canvas>
    <section class="hero">
        <div class="hero-content">
            <h1 class="animate-text glitch" data-text="Secure Your Data With Chaos">Secure Your Data<br>With Chaos</h1>
            <p class="animate-text">Experience military-grade encryption powered by chaos theory and advanced mathematics. Protect your messages with unprecedented security.</p>
            <div class="cta-buttons animate-up">
                <a href="/encrypt" class="button primary">Start Encrypting</a>
                <a href="/how-it-works" class="button secondary">Learn More</a>
            </div>
        </div>
    </section>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Three.js Scene Setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({
            canvas: document.querySelector('#bgCanvas'),
            alpha: true
        });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);

        // Create particle system
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 5000;
        const posArray = new Float32Array(particlesCount * 3);

        for(let i = 0; i < particlesCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 5;
        }

        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.005,
            color: '#ff3366'
        });

        const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particlesMesh);
        camera.position.z = 2;

        // Mouse movement effect
        let mouseX = 0;
        let mouseY = 0;

        document.addEventListener('mousemove', (event) => {
            mouseX = event.clientX / window.innerWidth - 0.5;
            mouseY = event.clientY / window.innerHeight - 0.5;
        });

        // Animation
        function animate() {
            requestAnimationFrame(animate);
            particlesMesh.rotation.y += 0.001;
            particlesMesh.rotation.x += mouseY * 0.001;
            particlesMesh.rotation.y += mouseX * 0.001;
            renderer.render(scene, camera);
        }
        animate();

        // GSAP Animations
        gsap.from('.animate-text', {
            duration: 1,
            y: 100,
            opacity: 0,
            stagger: 0.2,
            ease: "power4.out"
        });

        gsap.from('.animate-up', {
            duration: 1,
            y: 50,
            opacity: 0,
            delay: 0.8,
            ease: "power3.out"
        });

        // Resize handler
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
'''

HOW_IT_WORKS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>How It Works - Chaos-Based Cryptography</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #222; /* Dark background */
            color: #eee; /* Light text */
        }
        .container {
            background-color: #333; /* Darker container */
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(255,0,0,0.1); /* Red shadow */
            margin-bottom: 20px;
            border: 1px solid #555; /* Dark border */
        }
        h1, h2, h3 { color: #ff4d4d; /* Red headings */ }
        .button {
            display: inline-block;
            background-color: #7f8c8d;
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
            background-color: #95a5a6;
        }
        .explanation {
            text-align: left;
            padding: 20px;
        }
        .graph {
            margin: 20px 0;
            padding: 10px;
            border: 1px solid #555; /* Dark border */
            border-radius: 4px;
        }
        .code-block {
            background-color: #444; /* Darker gray code block */
            padding: 15px;
            border-radius: 4px;
            font-family: monospace;
            margin: 10px 0;
            color: #eee; /* Light text */
        }
    </style>
</head>
<body>
    <div class="container explanation">
        <h2>How Does It Work?</h2>

        <h3>1. The Logistic Map</h3>
        <p>At the heart of our encryption system is the logistic map, a chaotic mathematical function:</p>
        <div class="code-block">x_{n+1} = r * x_n * (1 - x_n)</div>
        <p>Where:</p>
        <ul>
            <li>r ≈ 4 (we use 3.99999...)</li>
            <li>x_n is a value between 0 and 1</li>
        </ul>
        <div id="logisticPlot" class="graph"></div>

        <h3>2. Encryption Process</h3>
        <p>The encryption process follows these steps:</p>
        <ol>
            <li>Each character in the input message is converted to its ASCII value</li>
            <li>The logistic map generates a unique chaos value for each character</li>
            <li>The chaos value is used to shift the ASCII value (modulo 256)</li>
            <li>In double encryption mode, this process is repeated with a second seed</li>
        </ol>

        <h3>3. Security Features</h3>
        <ul>
            <li><strong>Sensitivity to Initial Conditions:</strong> Even a tiny change in the seed value produces completely different results</li>
            <li><strong>Deterministic Chaos:</strong> The system is deterministic yet unpredictable without the correct seed</li>
            <li><strong>Double Encryption Option:</strong> Adds an extra layer of security with a second chaotic sequence</li>
        </ul>

        <div id="sensitivityPlot" class="graph"></div>
    </div>

    <script>
        // Generate logistic map plot
        function generateLogisticData(x0, n) {
            let x = x0;
            const r = 3.99999999999999;
            const xValues = [x];
            const yValues = [];

            for(let i = 0; i < n; i++) {
                const nextX = r * x * (1 - x);
                xValues.push(nextX);
                yValues.push(nextX);
                x = nextX;
            }

            return [xValues.slice(0, -1), yValues];
        }

        // Plot logistic map
        const [x1, y1] = generateLogisticData(0.2, 100);
        const trace1 = {
            x: x1,
            y: y1,
            mode: 'markers',
            name: 'x0 = 0.2',
            marker: { size: 3 }
        };

        const layout1 = {
            title: 'Logistic Map Behavior',
            xaxis: { title: 'x_n' },
            yaxis: { title: 'x_{n+1}' }
        };

        Plotly.newPlot('logisticPlot', [trace1], layout1);

        // Plot sensitivity demonstration
        const [x2, y2] = generateLogisticData(0.2, 50);
        const [x3, y3] = generateLogisticData(0.201, 50);

        const trace2 = {
            y: y2,
            mode: 'lines',
            name: 'x0 = 0.2'
        };

        const trace3 = {
            y: y3,
            mode: 'lines',
            name: 'x0 = 0.201'
        };

        const layout2 = {
            title: 'Sensitivity to Initial Conditions',
            xaxis: { title: 'Iteration' },
            yaxis: { title: 'Value' }
        };

        Plotly.newPlot('sensitivityPlot', [trace2, trace3], layout2);
    </script>
    <div style="text-align: center; margin-top: 20px;">
        <a href="/" class="button">Back to Home</a>
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
            background-color: #222; /* Dark background */
            color: #eee; /* Light text */
        }
        .container {
            background-color: #333; /* Darker container */
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(255,0,0,0.1); /* Red shadow */
            max-width: 700px;
            margin: 0 auto;
            border: 1px solid #555; /* Dark border */
        }
        h1 {
            color: #ff4d4d; /* Red heading */
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
            color: #ff4d4d; /* Red labels */
            font-weight: 500;
        }
        textarea, input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ff0000; /* Red border */
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
            box-sizing: box-sizing;
            background-color: #1a1a1a; /* Dark gray background */
            color: #ffffff; /* White text */
        }
        textarea:focus, input[type="number"]:focus {
            outline: none;
            border-color: #007bff; /* Blue border on focus */
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        .button {
            flex: 1;
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
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
            box-shadow: 0 5px 15px rgba(255, 51, 102, 0.3); /* Blue shadow */
        }
        .button.secondary {
            background-color: #7f8c8d;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #444; /* Dark gray result */
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
            color: #eee; /* Light text */
        }
        .result h3 {
            color: #ff4d4d; /* Red heading */
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
                <select name="mode" style="width: 100%; padding: 12px; border: 2px solid #ff0000; border-radius: 10px; font-size: 16px; margin-bottom: 15px; background-color: #1a1a1a; color: #ffffff;">
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
                <button type="submit" class="button">Encrypt</button>
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
            background-color: #222; /* Dark background */
            color: #eee; /* Light text */
        }
        .container {
            background-color: #333; /* Darker container */
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(255,0,0,0.1); /* Red shadow */
            max-width: 700px;
            margin: 0 auto;
            border: 1px solid #555; /* Dark border */
        }
        h1 {
            color: #ff4d4d; /* Red heading */
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
            color: #ff4d4d; /* Red labels */
            font-weight: 500;
        }
        textarea, input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ff0000; /* Red border */
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
            box-sizing: box-sizing;
            background-color: #1a1a1a; /* Dark gray background */
            color: #ffffff; /* White text */
        }
        textarea:focus, input[type="number"]:focus {
            outline: none;
            border-color: #007bff; /* Blue border on focus */
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        .button {
            flex: 1;
            background: linear-gradient(45deg, #ff3366, #ff6b6b);
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
            box-shadow: 0 5px 15px rgba(255, 51, 102, 0.3); /* Blue shadow */
        }
        .button.secondary {
            background-color: #7f8c8d;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #444; /* Dark gray result */
            border-radius: 10px;
            border-left: 4px solid #2ecc71;
            color: #eee; /* Light text */
        }
        .result h3 {
            color: #ff4d4d; /* Red heading */
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
                <select name="mode" style="width: 100%; padding: 12px; border: 2px solid #ff0000; border-radius: 10px; font-size: 16px; margin-bottom: 15px; background-color: #1a1a1a; color: #ffffff;">
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
                <button type="submit" class="button">Decrypt</button>
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

@app.route('/how-it-works')
def how_it_works():
    return render_template_string(HOW_IT_WORKS_TEMPLATE)


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