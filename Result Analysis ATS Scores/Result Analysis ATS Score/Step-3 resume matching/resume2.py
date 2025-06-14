import os
import numpy as np
import nltk
import pymupdf
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(word):
    """Map POS tag to first character used by WordNetLemmatizer"""
    pos_tagged = nltk.pos_tag([word])
    if pos_tagged:
        pos_tag = pos_tagged[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(pos_tag, wordnet.NOUN)
    return wordnet.NOUN

def preprocess_text(text):
    sentences = sent_tokenize(text)
    processed_sentences = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

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

def process_resumes(pdf_folder, docx_folder):
    resumes = []

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
                resumes.append((filename, processed_text))
            else:
                print(f"Skipping empty or unreadable file: {filename}")
    
    return resumes

def vectorize_text(job_description, resumes_texts):
    texts = [job_description] + resumes_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts)
    return vectors

def calculate_similarity(job_description, resumes_texts):
    vectors = vectorize_text(job_description, resumes_texts)
    job_desc_vector = vectors[0]
    resume_vectors = vectors[1:]
    similarities = cosine_similarity(job_desc_vector, resume_vectors)
    return similarities.flatten()

def rank_resumes(job_description, resumes, threshold=1e-6):
    similarity_scores = calculate_similarity(job_description, [text for _, text in resumes])
    resume_scores = [(filename, score) for (filename, _), score in zip(resumes, similarity_scores)]

    # Filter out resumes with negligible similarity
    filtered_scores = [(filename, score) for filename, score in resume_scores if score > threshold]
    
    sorted_resumes = sorted(filtered_scores, key=lambda x: x[1], reverse=True)
    return sorted_resumes

def save_results_to_file(results, output_path="ranked_resumes.txt"):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Rank\tFilename\tSimilarity Score\n")
        for rank, (filename, score) in enumerate(results, start=1):
            f.write(f"{rank}\t{filename}\t{score:.4f}\n")
    print(f"\nResults saved to '{output_path}'")

def main():
    # User input for job description
    job_description = input("Enter the job description:\n")

    # Folder paths
    pdf_folder = r"C:\Users\ankit\OneDrive\Desktop\PYTHON\resume pdf"
    docx_folder = r"C:\Users\ankit\OneDrive\Desktop\PYTHON\resume docx"

    # Process resumes
    resumes = process_resumes(pdf_folder, docx_folder)

    if not resumes:
        print("No resumes were successfully processed.")
        return

    # Rank resumes
    ranked_resumes = rank_resumes(job_description, resumes)

    if not ranked_resumes:
        print("No relevant resumes found (all similarity scores are negligible or zero).")
        return

    # Print results to console
    print("\nRelevant matching resumes (Ranked):")
    for rank, (filename, score) in enumerate(ranked_resumes, start=1):
        print(f"Rank {rank}: {filename} - Similarity Score: {score:.4f}")

    # Save results to file
    save_results_to_file(ranked_resumes)

if __name__ == "__main__":
    main()
