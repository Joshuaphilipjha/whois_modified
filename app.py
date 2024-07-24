from flask import Flask, render_template, request
import subprocess
import shlex

app = Flask(__name__)

def get_domain_info(domain_name):
    try:
        # Sanitize the domain name input to prevent shell injection
        sanitized_domain_name = shlex.quote(domain_name)
        result = subprocess.run(['whois', sanitized_domain_name], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: Command failed with return code {e.returncode}. Output: {e.output}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    domain_name = request.form['domain_name']
    domain_info = get_domain_info(domain_name)
    return render_template('index.html', domain_info=domain_info)

if __name__ == '__main__':
    app.run(debug=True)
