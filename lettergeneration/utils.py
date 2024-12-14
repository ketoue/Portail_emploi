import PyPDF2
from dotenv import load_dotenv
import openai
from docx import Document
import os
load_dotenv()

#traitement for the all file to the cover letter
openai.api_key = os.getenv("API_KEY")

def extraire_donnees(filepath):
    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            contenu = ""
            for page in reader.pages:
                contenu += page.extract_text()
        return contenu
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as file:
            contenu = file.read()
        return contenu
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        contenu = ""
        for paragraph in doc.paragraphs:
            contenu += paragraph.text + '\n'
        return contenu
    else:
        raise ValueError("Format de fichier non pris en charge. Veuillez utiliser un fichier PDF, TXT ou DOCX.")

def generer_lettre_motivation(data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes cover letters."},
            {"role": "user", "content": f"Utilise les informations suivantes pour rédiger une lettre de motivation: {data}"}
        ]
    )
    return response.choices[0].message['content']