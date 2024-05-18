from jellyfish import jaro_winkler_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import imagehash
import Levenshtein


def jaro_winkler(name1, name2):
    return jaro_winkler_similarity(name1, name2)

def edit_distance(name1, name2):
    return Levenshtein.ratio(name1, name2)

def tfidf_cosine_similarity(bio1, bio2):
    vectorizer = TfidfVectorizer().fit_transform([bio1, bio2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]

def image_similarity(image1_path, image2_path):
    hash1 = imagehash.average_hash(Image.open(image1_path))
    hash2 = imagehash.average_hash(Image.open(image2_path))
    return 1 - (hash1 - hash2) / len(hash1.hash) ** 2

def combined_similarity(name_sim, username_sim, bio_sim, pic_sim, following_sim, weights):
    total_weight = sum(weights.values())
    combined_score = (name_sim * weights['name'] +
                      username_sim * weights['username'] +
                      bio_sim * weights['bio'] +
                      pic_sim * weights['picture'] +
                      following_sim * weights['following']) / total_weight
    return combined_score