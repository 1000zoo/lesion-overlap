from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import os
from overlap.detector import Lesion
import nibabel as nib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.secret_key = os.urandom(16) 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return jsonify({'error': 'No selected file'}), 400
        if file and is_nii_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            nii = nib.load(filename).get_fdata()
            l = Lesion(nii)
            result, info = l.overlap_detection()
            data = {'result': result, 'info': info}
            print(data)
            os.remove(filename)
            return jsonify({'redirect': url_for('uploaded_file', data = data)}), 200
        else:
            flash('Allowed file types are .nii')
            return jsonify({'error': 'Allowed file types are .nii'}), 400
    return render_template('index.html')


@app.route('/uploaded', methods=['GET'])
def uploaded_file():
    data = eval(request.args.get('data'))
    return render_template('uploaded.html', result=data['result'], info=data['info'])


def is_nii_file(filename: str):
    sp = filename.split(".")
    return sp[-1] == "nii" or (sp[-2] == "nii" and sp[-1] == "gz")

if __name__ == '__main__':
    app.run(debug=True)
