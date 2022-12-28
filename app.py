"""
Author: Muhammad Adiyaksa
Github: adiyaksa1234
"""

# Module
from flask import Flask, render_template, send_file, request, url_for, redirect


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():  
    """
    Request Method
    """
    if request.method == 'POST':
        return "a"
    
    if request.method == 'GET':
       download = True
       return render_template('index.html', download = download)

if __name__ == "__main__":
    app.run()