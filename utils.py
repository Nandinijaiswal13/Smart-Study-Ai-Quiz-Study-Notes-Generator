import PyPDF2
import nltk
import re
from collections import Counter

nltk.download('punkt')

# 📄 Extract text
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# 🧹 Preprocess text
def preprocess_text(text):
    text = re.sub(r'\d+\.', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace("\n", " ")

    sentences = nltk.sent_tokenize(text)
    return text, sentences


# 🔍 Keyword extraction
def content_analysis(text):
    words = nltk.word_tokenize(text.lower())
    words = [w for w in words if w.isalnum() and len(w) > 4]

    freq = Counter(words)
    return [w for w, _ in freq.most_common(10)]


# 📝 Notes generation (important sentences)
def generate_notes(text):
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text.lower())

    words = [w for w in words if w.isalnum() and len(w) > 3]
    freq = Counter(words)

    scores = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    top = sorted(scores, key=scores.get, reverse=True)[:5]
    return " ".join(top)


# Quiz generation (rule-based)
def generate_quiz(sentences):
    quiz = []

    for sent in sentences:
        words = sent.split()

        if len(words) < 6:
            continue

        # Pick meaningful word
        keywords = [w for w in words if len(w) > 5]

        if not keywords:
            continue

        key = keywords[0]

        # Create better questions
        question = f"What is the meaning of {key}?"


        quiz.append({
            "question": question,
        })

        if len(quiz) >= 5:
            break

    return quiz