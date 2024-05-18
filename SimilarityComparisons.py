from jellyfish import jaro_winkler_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import imagehash
import Levenshtein
import wikipedia


def jaro_winkler(name1, name2):
    return jaro_winkler_similarity(name1, name2)

def edit_distance(name1, name2):
    return Levenshtein.ratio(name1, name2)

def tfidf_cosine_similarity(bio1: str, bio2: str) -> float:
    # Check for empty bios
    if not bio1 or not bio2:
        print("One or both bios are empty.")
        return 0.0
    
    try:
        # Fit and transform the bios into TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([bio1, bio2])
        
        # Convert the matrix to an array
        vectors = tfidf_matrix.toarray()
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors)[0][1]
        
        return similarity
    except Exception as e:
        print(f"Error in tfidf_cosine_similarity: {e}")
        return 0.0

def image_similarity(image1_path, image2_path):
    hash1 = imagehash.average_hash(Image.open(image1_path))
    hash2 = imagehash.average_hash(Image.open(image2_path))
    return 1 - (hash1 - hash2) / len(hash1.hash) ** 2

def esa_similarity(text1: str, text2: str) -> float:
    def get_wikipedia_article(text):
        try:
            page = wikipedia.page(text)
            return page.content
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error for {text}: {e.options}")
            # Attempt to use the first option
            try:
                page = wikipedia.page(e.options[0])
                return page.content
            except Exception as e:
                print(f"Failed to resolve disambiguation for {text}: {e}")
                return None
        except wikipedia.exceptions.PageError:
            print(f"Page error for {text}: Page does not exist")
            return None
        except Exception as e:
            print(f"Error fetching page for {text}: {e}")
            return None

    try:
        article1 = get_wikipedia_article(text1)
        article2 = get_wikipedia_article(text2)

        if not article1 or not article2:
            print("One or both articles could not be fetched.")
            return 0.0
        
        # Construct TF-IDF vectors
        vectorizer = TfidfVectorizer().fit_transform([article1, article2])
        vectors = vectorizer.toarray()
        
        # Compute cosine similarity
        similarity = cosine_similarity(vectors)[0][1]
    except Exception as e:
        print(f"Error while computing ESA similarity: {e}")
        similarity = 0.0
    return similarity


def combined_similarity(name_sim, username_sim, bio_sim, pic_sim, following_sim, weights):
    total_weight = sum(weights.values())
    combined_score = (name_sim * weights['name'] +
                      username_sim * weights['username'] +
                      bio_sim * weights['bio'] +
                      pic_sim * weights['picture'] +
                      following_sim * weights['following']) / total_weight
    return combined_score