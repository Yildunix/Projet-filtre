#####################################################################
####################### Modules standards############################
#####################################################################
import os 

#####################################################################
#################### Modules exportes ###############################
#####################################################################

import pandas as pd 
from flask import Flask, request 
from utils import get_file_extension, load_csv, is_csv

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    file = request.files['file']
    filename = file.filename

    if not is_csv(filename):
        return {'error': 'Only CSV files are supported'}, 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    data = load_csv(filepath)

    return {'message': 'File uploaded successfully', 'filepath': filepath, 'data_preview': data.head().to_json()}, 200

@app.route('/filter', methods=['POST'])
def filter_data():
    data = request.get_json()
    filepath = data.get('filepath')
    filters = data.get('filters', {})

    if not filepath or not os.path.exists(filepath):
        return {'error': 'Invalid file path'}, 400

    if not is_csv(filepath):
        return {'error': 'Only CSV files are supported'}, 400

    df = load_csv(filepath)

    columns_to_keep = filters.get('columns_to_keep')
    if columns_to_keep:
        df = df[columns_to_keep]

    conditions = filters.get('conditions', {})
    for column, value in conditions.items():
        df = df[df[column] == value]

    cleaned_filepath = filepath.replace('.csv', '_cleaned.csv')
    df.to_csv(cleaned_filepath, index=False)

    return {'message': 'File filtered successfully', 'cleaned_filepath': cleaned_filepath}, 200

if __name__ == '__main__':
    app.run(debug=True)