from gliner import GLiNER
import os
import sqlite3
from isbntools.app import *

# Funtion to extract text from the syllabi directory and return a list of chunks of text
def extract_text(path, length):
    print(path, length)
    data_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".txt")]
    text = ""
    
    for data_file in data_files:
        with open(data_file, "r") as opened_file:
            text += opened_file.read()
    
    text_in_chunks = split_text(text, length)

    return text_in_chunks

# Function to split the text into chunks
def split_text(text, length):
    text = text.split()
    chunks = []
    chunk = []
    
    for word in text:
        if (len(" ".join(chunk))) > length:
            chunks.append(" ".join(chunk))
            chunk = []
        chunk.append(word)

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

# Identity reading requirements from the books and return a labeled list
def zero_shot(text_chunks, labels):
    model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")
    entities = []
    for chunk in text_chunks:
        entity = model.predict_entities(chunk, labels, threshold=0.5)
        entities.extend(entity)

    return entities

# Storing the information in the database
def storing_in_database(database, entities, acronym_file):
    acronyms = open(acronym_file, "r")
    acronymsFile = acronyms.readlines()
    acronymsList = []

    conn = sqlite3.connect(database)    
    cursor = conn.cursor()              
    cursor.execute('''CREATE TABLE IF NOT EXISTS reading_requirements (
                        id INTEGER PRIMARY KEY,
                        isbn TEXT,
                        book_title TEXT UNIQUE,
                        availability TEXT)''')     
    
    for acronym in acronymsFile:
        acronymsList.append(acronym.strip())
    
    # Insert data into the table
    for entity in entities:
        if entity['text'] not in acronymsList:
            isbn = isbn_from_words(entity['text'])
            cursor.execute('''INSERT OR IGNORE INTO reading_requirements (isbn, book_title, availability) VALUES (?, ?, ?)''', (str(isbn), entity["text"], "not checked"))

    conn.commit()  

    conn.close()   