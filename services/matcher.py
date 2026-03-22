'''from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Generic words to ignore
GENERIC_WORDS = {
    "data", "analysis", "experience", "learning",
    "looking", "strong", "machine"
}


from services.skill_map import SKILL_SYNONYMS

def normalize_skills(keywords):
    normalized = set()

    for kw in keywords:
        kw_lower = kw.lower()
        matched = False

        for canonical, variants in SKILL_SYNONYMS.items():
            if kw_lower == canonical or kw_lower in variants:
                normalized.add(canonical)
                matched = True
                break

        if not matched:
            normalized.add(kw_lower)

    return list(normalized)






def compute_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=2000
    )

    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0], tfidf[1])[0][0]


def extract_keywords(text):
    """
    Extract meaningful keywords from text using TF-IDF
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50
    )

    tfidf = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()

    cleaned = []
    for kw in keywords:
        if len(kw.split()) == 1 and kw in GENERIC_WORDS:
            continue
        cleaned.append(kw)

    return set(cleaned)


def analyze_resumes(resume_sections, jd_text):
    results = []

    jd_skills = extract_keywords(jd_text)

    for sections in resume_sections:
        # Section-wise similarity
        skills_score = compute_similarity(sections["skills"], jd_text)
        experience_score = compute_similarity(sections["experience"], jd_text)
        projects_score = compute_similarity(sections["projects"], jd_text)

        final_score = (
            0.5 * skills_score +
            0.3 * experience_score +
            0.2 * projects_score
        )

        # Skill coverage
        resume_skills = extract_keywords(sections["skills"])

        raw_matched = resume_skills & jd_skills
        raw_missing = jd_skills - resume_skills

        matched_skills = normalize_skills(list(raw_matched))
        missing_skills = normalize_skills(list(raw_missing))

        coverage = (
            len(matched_skills) / len(jd_skills)
            if jd_skills else 0
        )

        results.append({
            "score": final_score,
            "skills_score": skills_score,
            "experience_score": experience_score,
            "projects_score": projects_score,
            "skill_coverage": coverage,
            "matched_skills": matched_skills[:10],
            "missing_skills": missing_skills[:10]
        })

    return results'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

# Load BERT model (only once)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generic words to ignore
GENERIC_WORDS = {
    "data", "analysis", "experience", "learning",
    "looking", "strong", "machine",
    "model", "models", "skills", "skill",
    "real", "based", "using", "work", "project",
    "projects", "knowledge", "system", "development",
     "random", "based", "end", "hands"
}
IMPORTANT_SKILLS = {
    "python", "machine learning", "deep learning",
    "pytorch", "tensorflow", "flask", "sql",
    "matplotlib", "seaborn", "pandas", "numpy",
    "random forest", "xgboost"
}

from services.skill_map import SKILL_SYNONYMS


def normalize_skills(keywords):
    normalized = set()

    for kw in keywords:
        kw_lower = kw.lower()
        matched = False

        for canonical, variants in SKILL_SYNONYMS.items():
            if kw_lower == canonical or kw_lower in variants:
                normalized.add(canonical)
                matched = True
                break

        if not matched:
            normalized.add(kw_lower)

    return list(normalized)


# 🔥 UPDATED: BERT-based similarity
def compute_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0

    embeddings = model.encode([text1, text2])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]


def extract_keywords(text):
    """
    Extract meaningful keywords from text using TF-IDF
    (kept same for skill extraction)
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50
    )

    tfidf = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()

    '''cleaned = []
    for kw in keywords:
        if len(kw.split()) == 1 and kw in GENERIC_WORDS:
            continue
        cleaned.append(kw)'''
    cleaned = []
    for kw in keywords:

        kw = kw.lower().strip()

    # Remove very short words
        if len(kw) < 3:

            continue

    # 🔥 Remove generic SINGLE words only (keep phrases)
        if " " not in kw and kw in GENERIC_WORDS:

            continue
        if len(kw.split()) > 3:

            continue
    # Remove numeric junk
        if kw.isnumeric():
            continue

        cleaned.append(kw)
    
    text_lower = text.lower()

    for skill in IMPORTANT_SKILLS:
        if skill in text_lower:
            cleaned.append(skill)

    return set(cleaned)


'''def analyze_resumes(resume_sections, jd_text):
    results = []

    jd_skills = extract_keywords(jd_text)

    for sections in resume_sections:
        # 🔥 Section-wise semantic similarity using BERT
        skills_score = compute_similarity(sections["skills"] + " ", jd_text)
        experience_score = compute_similarity(sections["experience"] + " ", jd_text)
        projects_score = compute_similarity(sections["projects"] + " ", jd_text)

        # Weighted scoring
        final_score = (
            0.5 * skills_score +
            0.3 * experience_score +
            0.2 * projects_score
        )

        # Skill coverage (still TF-IDF based - good hybrid approach)
        resume_skills = extract_keywords(sections["skills"])

        raw_matched = resume_skills & jd_skills
        raw_missing = jd_skills - resume_skills

        matched_skills = normalize_skills(list(raw_matched))
        missing_skills = normalize_skills(list(raw_missing))

        coverage = (
            len(matched_skills) / len(jd_skills)
            if jd_skills else 0
        )

        results.append({
            "score": float(final_score),
            "skills_score": float(skills_score),
            "experience_score": float(experience_score),
            "projects_score": float(projects_score),
            "skill_coverage": coverage,
            "matched_skills": matched_skills[:10],
            "missing_skills": missing_skills[:10]
        })

    return results'''


def analyze_resumes(resume_sections, jd_text):
    results = []

    jd_skills = extract_keywords(jd_text)

    for sections in resume_sections:

        # 🔥 Combine full resume text (IMPORTANT FIX)
        full_resume = (
            sections["skills"] + " " +
            sections["experience"] + " " +
            sections["projects"]
        )

        # 🔥 Main semantic score using full context
        semantic_score = compute_similarity(full_resume, jd_text)

        # Section-wise similarity (kept for explainability)
        skills_score = compute_similarity(sections["skills"], jd_text)
        experience_score = compute_similarity(sections["experience"], jd_text)
        projects_score = compute_similarity(sections["projects"], jd_text)

        # 🔥 NEW weighted scoring (BERT-focused)
        final_score = (
            0.6 * semantic_score +
            0.2 * skills_score +
            0.1 * experience_score +
            0.1 * projects_score
        )

        # Skill coverage (TF-IDF based)
        resume_skills = extract_keywords(sections["skills"])

        raw_matched = resume_skills & jd_skills
        raw_missing = jd_skills - resume_skills

        matched_skills = normalize_skills(list(raw_matched))
        missing_skills = normalize_skills(list(raw_missing))

        coverage = (
            len(matched_skills) / len(jd_skills)
            if jd_skills else 0
        )

        results.append({
            "score": float(final_score),
            "semantic_score": float(semantic_score),  # 🔥 new (useful for debug/viva)
            "skills_score": float(skills_score),
            "experience_score": float(experience_score),
            "projects_score": float(projects_score),
            "skill_coverage": coverage,
            "matched_skills": matched_skills[:10],
            "missing_skills": missing_skills[:10]
        })

    return results
