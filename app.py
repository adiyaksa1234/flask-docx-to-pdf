# Module 
from flask import Flask, render_template, send_file, request, url_for, redirect, flash, session
from flask_toastr import Toastr
import os   
import subprocess
import time

# Create Flask app instance
app = Flask(__name__)
# Generate random secret key for app
app.secret_key = os.urandom(15)
# Create instance of Toastr
toastr = Toastr(app)

@app.route('/', methods=['GET', 'POST'])
def home():  
    if request.method == 'POST':
        # Check if file is present in the form submission
        if request.files.get('formFile'):
            file = request.files.get('formFile')
            # Check if file is valid and has allowed extension
            if file and allowed_file(file.filename):
                    # Create temp directory if it doesn't already exist
                    if not os.path.exists('temp'):
                            os.makedirs('temp')
                    # Generate temporary filename using the uploaded file's name and current timestamp
                    filename = f'{file.filename.rsplit(".", 1)[0]}_{int(time.time())}.docx'
                    # Save file to temp directory
                    file.save(os.path.join('temp', filename))
                    # Convert file to PDF using unoconv
                    subprocess.call(['unoconv', '-f', 'pdf', os.path.join('temp', filename)])
                    # Save PDF filename to session
                    session['pdf_filename'] = filename.replace('.docx', '.pdf')
                                         # Set download flag to True
                    download = True
                    # Show success message
                    flash({'title': "Success", 'message': "You can download it now thanks"}, 'success')
                    # Render template with download flag
                    return render_template('index.html', download = download)
            else:
                    # Show error message if file is not valid
                    flash({'title': "Error", 'message': "Files can only be docx !"}, 'error')
                    # Render template
                    return render_template('index.html')
        else:
            # Show error message if no file is present in form submission
            flash({'title': "Error", 'message': "Please enter your files!"}, 'error')
            # Render template
            return render_template('index.html')
    
    if request.method == 'GET':
       # Clear session data
       session.clear()
       # Render template
       return render_template('index.html')
   
@app.route('/download')
def download():
    # Check if PDF file is available in session
    if "pdf_filename" or not session or session.get('pdf_filename'):
            # Get PDF filename from session
            pdf_filename = session.get('pdf_filename')
            # Send PDF file to user with Content-Disposition header
            return send_file(os.path.join('temp', pdf_filename),  as_attachment=True)
    else:
        # Redirect to home page if PDF file is not available in session
        return redirect(url_for('home'))
   
def allowed_file(filename):
    # Check if file has allowed extension
   return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'docx'

# Run app
if __name__ == "__main__":
    app.run()   


