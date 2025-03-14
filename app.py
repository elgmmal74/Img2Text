from flask import Flask, render_template, request, redirect, url_for
import easyocr
import os
from werkzeug.utils import secure_filename

# Initialize Flask
app = Flask(__name__)

# Folder to upload images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize EasyOCR with support for Arabic and English
reader = easyocr.Reader(['ar', 'en'])  # Add more languages if needed

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        # If no file is selected
        if file.filename == '':
            return redirect(request.url)
        
        # Save the uploaded file
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from the image
            results = reader.readtext(filepath, detail=0, paragraph=True)
            
            # Display the results
            return render_template('index.html', text=results, image_url=filepath)
    
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)