import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_courses():
    df = pd.read_csv("data/courses.csv")
    return df

def recommend_courses(user_input, top_n=3):
    df = load_courses()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'] + " " + df['category'])

    user_vec = tfidf.transform([user_input])
    similarity = cosine_similarity(user_vec, tfidf_matrix).flatten()

    top_indices = similarity.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][['course_name', 'category', 'difficulty']]
