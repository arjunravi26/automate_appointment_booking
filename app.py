from flask import Flask, render_template, request, jsonify
from main import automate
import time
import json

app = Flask(__name__)

def process_automation(user_input):
    """
    Function to process the automation request using Selenium.
    In a real implementation, this would contain the actual automation logic.
    For demo purposes, we'll return a sample result.
    """
    result = automate(user_input)

    # Simulate processing time
    time.sleep(2)

    return result

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    user_input = request.json.get('message', '')

    # Process the automation
    result = process_automation(user_input)

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)