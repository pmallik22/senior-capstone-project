from flask import *
import os
import extract_prose_pdf as extract
import zeroshot_NER as ner
import webscraping as wbs   
import convert_to_excel as convert
import cleanup as clean

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads' 
EXTRACTED_FOLDER = 'extracted-files'
ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_ACRONYM_EXTENSIONS = {'txt'}
LABELS = ["Textbook", "Books"]
MAX_LENGTH = 300
DATABASE_NAME = "reading_requirements"
OUTPUT = "static/output-report.xlsx"
CURRENT_DIR = os.getcwd()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_acronym_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_ACRONYM_EXTENSIONS

@app.route('/')
def main():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        url = request.form['url']
        acronym_file = request.files['file']
        
        if not files:
            return render_template('error.html', error_message="No acronym file uploaded. Please upload a valid text file.")
        
        if not url:
            return render_template('error.html', error_message="No url provided. Please include a valid library website link.")
        
        if not acronym_file or acronym_file.filename == '':
            return render_template('error.html', error_message="No acronym file uploaded. Please upload a valid text file.")

        for file in files:
            if not allowed_file(file.filename):
                return render_template('error.html', error_message="Invalid file type for the syllabi. Please upload PDF files.")

            else:
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
        
        if not allowed_acronym_file(acronym_file.filename):
            return render_template('error.html', error_message="Invalid file type for acronyms. Please upload a text file.")

        else:
            acronym_filepath = os.path.join(CURRENT_DIR, acronym_file.filename)
            acronym_file.save(acronym_filepath)

        extract.extract_prose(UPLOAD_FOLDER, EXTRACTED_FOLDER)

        extracted_chunks = ner.extract_text(EXTRACTED_FOLDER, MAX_LENGTH)  

        entities = ner.zero_shot(extracted_chunks, LABELS)

        ner.storing_in_database(DATABASE_NAME, entities, acronym_file.filename)

        wbs.scrape_and_store(url, DATABASE_NAME)

        convert.convert(DATABASE_NAME, OUTPUT)

        clean.cleanup(UPLOAD_FOLDER, EXTRACTED_FOLDER, DATABASE_NAME, acronym_file.filename)
        
        return render_template('success.html', OUTPUT='output-report.xlsx')
                
    
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=9900, debug=True)
    app.run(debug=True)