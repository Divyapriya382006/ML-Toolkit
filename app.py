from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dataframe = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global dataframe
    file = request.files['datafile']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Read file
    ext = file.filename.split('.')[-1]
    if ext == 'csv':
        dataframe = pd.read_csv(filepath)
    elif ext == 'xlsx':
        dataframe = pd.read_excel(filepath)
    elif ext == 'txt':
        dataframe = pd.read_csv(filepath, delimiter='\\s+|,|\\t', engine='python')  # flexible txt reader
    else:
        return "Unsupported file format"

    return redirect(url_for('read_file'))

@app.route('/read')
def read_file():
    global dataframe
    if dataframe is not None:
        return dataframe.to_html(classes='table table-striped')
    return "No file uploaded!"

@app.route('/labels')
def labels():
    global dataframe
    if dataframe is not None:
        cols = list(dataframe.columns)
        idxs = list(dataframe.index)
        return {
            "columns": cols,
            "rows": idxs
        }
    return "No file uploaded!"

@app.route('/headtail')
def headtail():
    global dataframe
    if dataframe is not None:
        return {
            "head": dataframe.head().to_dict(),
            "tail": dataframe.tail().to_dict()
        }
    return "No file uploaded!"

@app.route('/missing')
def missing_values():
    global dataframe
    if dataframe is not None:
        return (dataframe.isnull().sum()).to_dict()
    return "No file uploaded!"

# Add more routes for stats, visuals, ML etc.

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
