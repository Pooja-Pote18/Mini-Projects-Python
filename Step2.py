import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import string
import os
import pymupdf
import docx

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('all')


def get_wordnet_pos(word):
    """Map POS tag to first character used by WordNetLemmatizer"""
    pos_tagged = nltk.pos_tag([word])
    if pos_tagged:
        pos_tag = pos_tagged[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(pos_tag, wordnet.NOUN)
    return wordnet.NOUN

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    sentences = sent_tokenize(text)
    processed_sentences = []
    
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub(r'[^a-zA-Z0-9\s%-]', '', sentence)  # Preserve necessary symbols
        
        tokens = word_tokenize(sentence)
        filtered_tokens = [word for word in tokens if word not in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in filtered_tokens]
        
        processed_sentences.append("- " + ' '.join(lemmatized_tokens))  # Add bullet points
    
    return "\n".join(processed_sentences)  # Return formatted list


def extract_text_from_pdf(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error reading DOCX '{docx_path}': {e}")
        return ""

def process_resumes(pdf_folder, docx_folder):
    for resume_folder in [pdf_folder, docx_folder]:
        if not os.path.exists(resume_folder):
            print(f"Folder '{resume_folder}' not found!")
            continue
        
        for filename in os.listdir(resume_folder):
            file_path = os.path.join(resume_folder, filename)
            
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                continue  # Skip unsupported files
            
            if text:
                processed_text = preprocess_text(text)
                print(f"Processed Resume ({filename}):\n{processed_text}\n")
            else:
                print(f"Skipping empty or unreadable file: {filename}")

# Example usage
if __name__ == "__main__":
    pdf_folder = input("Enter the path for the PDF resumes folder: ")
    docx_folder = input("Enter the path for the DOCX resumes folder: ")
    
    process_resumes(pdf_folder, docx_folder)

    