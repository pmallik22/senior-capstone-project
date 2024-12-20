import os
from PyPDF2 import PdfReader
import sys

def extract_prose(input_dir, output_dir):

    # Check if the input directory exists, exit if it does not
    if not os.path.exists(input_dir):
        print("error,", input_dir, "does not exist, exiting.", file=sys.stderr)
        exit(-1)

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each PDF file in the input directory
    for filename in os.listdir(input_dir):

        if filename.endswith(".pdf"):  # Check if the file is a PDF

            pdf_path = os.path.join(input_dir, filename)
            txt_path = os.path.join(output_dir, filename.replace(".pdf", ".txt"))
            
            # Read the PDF file
            reader = PdfReader(pdf_path)

            # Open the output text file
            with open(txt_path, "w", encoding="utf-8") as txtFile:

                # Extract and write text from each page
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    txtFile.write(page.extract_text())

            txtFile.close()
            
    print("Text extraction completed for all PDF files.")