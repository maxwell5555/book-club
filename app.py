from flask import Flask, jsonify, render_template
from load_spells import load_spells_from_ods

app = Flask(__name__)
SPELLS_FILE = 'data/Book_Club_Data_2024.ods'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/spells')
def get_spells():
    spells = load_spells_from_ods(SPELLS_FILE)
    return jsonify(spells)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)