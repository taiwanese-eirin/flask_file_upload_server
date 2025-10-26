import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash

app = Flask(__name__)

# Read the upload folder from the environment variable, with a fallback for local development
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

def get_file_list(folder_path):
    os.chdir(folder_path)
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return [{'name': f, 'type': get_file_extension(f)[1:].lower(), 'path': os.path.join(folder_path, f)} for f in file_list]

def get_file_time(file):
    return os.path.getmtime(file['path'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        files = request.files.getlist('file')
        for file in files:
            if file.filename: # Ensure filename is not empty
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Process file
    file_list_decoded = get_file_list(UPLOAD_FOLDER)
    file_list_decoded.sort(key=get_file_time, reverse=True)
    return render_template('index.html', files=file_list_decoded)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete_file(filename):
    if request.method == 'POST':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            flash('File not found')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
