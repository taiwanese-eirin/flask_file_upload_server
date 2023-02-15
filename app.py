import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = b'./uploads'  # Define the folder where uploaded files will be saved
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

def get_file_list(folder_path):
    file_list = os.listdir(folder_path)
    return [{'name': f.decode('utf-8'), 'type': get_file_extension(f.decode('utf-8'))[1:].lower()} for f in file_list]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        files = request.files.getlist('file')
        for file in files:
            filename = file.filename.encode('utf-8')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'].decode('utf-8'), filename.decode('utf-8')))
            os.chmod(os.path.join(app.config['UPLOAD_FOLDER'].decode('utf-8'), filename.decode('utf-8')), 0o777)
        # Process file
        file_list_decoded = get_file_list(UPLOAD_FOLDER)
        return render_template('index.html', files=file_list_decoded)
    else:
        file_list_decoded = get_file_list(UPLOAD_FOLDER)
        return render_template('index.html', files=file_list_decoded)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'].decode('utf-8'), filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete_file(filename):
    if request.method == 'POST':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.encode('utf-8'))
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(url_for('index'))
    else:
        flash('File not found')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
