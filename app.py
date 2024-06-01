# app.py
from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Replace 'default_secret_key' with a fallback or raise an error

CF_API_URL = "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ciphers"

# Cipher suites for different security levels
SECURITY_LEVEL_CIPHERS = {
    'modern': [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305"
    ],
    'compatible': [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "AES128-GCM-SHA256",
        "AES256-GCM-SHA384",
        "AES128-SHA",
        "AES256-SHA"
    ],
    'legacy': [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "AES128-GCM-SHA256",
        "AES256-GCM-SHA384",
        "AES128-SHA",
        "AES256-SHA",
        "DES-CBC3-SHA"
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zone_id = request.form['zone_id']
        api_token = request.form['api_token']
        security_level = request.form.get('security_level')
        ciphers = request.form.getlist('ciphers')
        
        # Determine cipher suites to use
        if security_level and not ciphers:
            ciphers = SECURITY_LEVEL_CIPHERS.get(security_level, [])
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        data = {
            "value": ciphers
        }
        
        response = requests.patch(CF_API_URL.format(zone_id=zone_id), headers=headers, json=data)
        
        if response.status_code == 200:
            flash('Cipher suites updated successfully.', 'success')
        else:
            flash('Error updating cipher suites: ' + response.text, 'danger')
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
