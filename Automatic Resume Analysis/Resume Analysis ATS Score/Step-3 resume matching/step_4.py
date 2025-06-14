import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import os
import pymupdf
import docx
import pandas as pd
import numpy as np

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Global resources
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    pos_tagged = nltk.pos_tag([word])
    if pos_tagged:
        pos_tag = pos_tagged[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(pos_tag, wordnet.NOUN)
    return wordnet.NOUN

def preprocess_text(text):
    sentences = sent_tokenize(text)
    processed_sentences = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub(r'[^a-zA-Z0-9\s%-]', '', sentence)
        tokens = word_tokenize(sentence)
        filtered_tokens = [word for word in tokens if word not in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in filtered_tokens]
        processed_sentences.append(' '.join(lemmatized_tokens))
    return ' '.join(processed_sentences)

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

def get_keywords(text):
    tokens = word_tokenize(text.lower())
    return set([lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens if word.isalpha() and word not in stop_words])

def calculate_ats_score(resume_keywords, jd_keywords):
    if not jd_keywords:
        return 0.0
    match_count = len(resume_keywords.intersection(jd_keywords))
    return round((match_count / len(jd_keywords)) * 100, 2)

def load_job_description(jd_path):
    if jd_path.endswith(".pdf"):
        return extract_text_from_pdf(jd_path)
    elif jd_path.endswith(".docx"):
        return extract_text_from_docx(jd_path)
    elif jd_path.endswith(".txt"):
        try:
            with open(jd_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading JD file: {e}")
    return ""

def rank_and_shortlist(scores_dict, top_n=5):
    df = pd.DataFrame(scores_dict.items(), columns=["Candidate", "ATS_Score"])
    df.sort_values(by="ATS_Score", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    print("\n📊 Ranked Candidates:")
    print(df)

    print(f"\n✅ Top {top_n} Shortlisted Candidates:")
    print(df.head(top_n))

    df.to_csv("ranked_candidates.csv", index=False)
    print("\n📁 Results saved to 'ranked_candidates.csv'")

def process_resumes(pdf_folder, docx_folder, jd_text):
    jd_processed = preprocess_text(jd_text)
    jd_keywords = get_keywords(jd_processed)
    scores = {}

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
                continue

            if text:
                processed_text = preprocess_text(text)
                resume_keywords = get_keywords(processed_text)
                ats_score = calculate_ats_score(resume_keywords, jd_keywords)
                scores[filename] = ats_score
            else:
                print(f"Skipping empty or unreadable file: {filename}")

    rank_and_shortlist(scores, top_n=5)

# Entry point
if __name__ == "__main__":
    pdf_folder = input("Enter the path for the PDF resumes folder: ")
    docx_folder = input("Enter the path for the DOCX resumes folder: ")
    jd_path = input("Enter the path for the Job Description file (TXT, PDF, or DOCX): ")

    jd_text = load_job_description(jd_path)
    if not jd_text:
        print("❌ Failed to load job description. Please check the path or format.")
    else:
        process_resumes(pdf_folder, docx_folder, jd_text)
