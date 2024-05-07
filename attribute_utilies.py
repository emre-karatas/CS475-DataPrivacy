import random
import hashlib

import np
from PIL import Image, ImageFilter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# noinspection PyTypeChecker
class AttributeUtilities:
    def __init__(self, utility_scores):
        """
        Initialize with a dictionary of attribute utility scores.
        Lower scores mean higher sensitivity and need for more obfuscation.
        """
        self.utility_scores = utility_scores

    def obfuscate_data(self, data):
        """
        Obfuscates data based on utility scores and attribute type.
        More sensitive data (lower utility score) will receive stronger obfuscation.
        """
        obfuscated_data = {}
        for key, value in data.items():
            utility = self.utility_scores.get(key, 1)  # Default utility is 1 (normal sensitivity)
            method = getattr(self, f"obfuscate_{key}", self.apply_general_obfuscation)
            obfuscated_data[key] = method(value, utility)
            logging.info(f"Obfuscated {key}: Original Value: {value}, Utility: {utility}")
        return obfuscated_data

    def obfuscate_location(location, utility):
        """
        Advanced method to obfuscate geographic locations based on utility.
        Applies different levels of noise and area generalization.
        """
        coordinates_map = {
            "New York, NY": (40.7128, -74.0060),
            "San Francisco, CA": (37.7749, -122.4194),
            "Los Angeles, CA": (34.0522, -118.2437)
        }

        coordinates = coordinates_map.get(location, (0, 0))

        if utility < 0.3:
            return AttributeUtilities.add_location_noise(coordinates, radius=1000)
        elif utility < 0.6:
            return AttributeUtilities.add_location_noise(coordinates, radius=500)
        elif utility < 0.8:
            return AttributeUtilities.add_location_noise(coordinates, radius=100)
        return location

    @staticmethod
    def add_location_noise(coordinates, radius):
        """
        Adds random geospatial noise to coordinates within a specified radius in meters.
        """
        lat, lon = coordinates
        angle = random.uniform(0, 2 * 3.1415926535)
        r = radius * random.uniform(0, 1) ** 0.5
        new_lat = lat + (r * random.cos(angle)) / 111321
        new_lon = lon + (r * random.sin(angle)) / (
                    111321 * random.cos(lat * 3.1415926535 / 180))
        return new_lat, new_lon

    @staticmethod
    def obfuscate_gender(gender, utility):
        """
        Gender is either not changed or fully hidden based on sensitivity.
        """
        if utility < 0.5:
            return "Unspecified"
        return gender

    @staticmethod
    def obfuscate_profile_photo(photo_path, utility):
        """
        Applies varying levels of blurring to the profile photo based on the utility.
        """
        try:
            image = Image.open(photo_path)
            blur_radius = 5 if utility > 0.5 else 10  # More blur for lower utility
            blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            blurred_path = photo_path.replace('.jpg', '_blurred.jpg')
            blurred_image.save(blurred_path)
            return blurred_path
        except IOError:
            logging.error(f"Error opening image {photo_path}")
            return photo_path

    @staticmethod
    def apply_heavy_blur_and_noise(image, photo_path):
        """
        Applies heavy Gaussian blur and adds Gaussian noise to an image.
        """
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=10))
        np_image = np.array(blurred_image)
        row, col, ch = np_image.shape
        mean = 0
        sigma = 16
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = np_image + gauss
        noisy_image = Image.fromarray(np.clip(noisy, 0, 255).astype(np.uint8))
        blurred_noisy_path = photo_path.replace('.jpg', '_blurred_noisy.jpg')
        noisy_image.save(blurred_noisy_path)
        return blurred_noisy_path

    @staticmethod
    def apply_gaussian_blur(image_path, sigma=8):
        """
        Applies Gaussian blur with a specified standard deviation.
        """
        image = cv2.imread(image_path)
        if image is None:
            return image_path

        blurred_image = cv2.GaussianBlur(image, (0, 0), sigma)
        blurred_path = image_path.replace('.jpg', '_gaussian_blurred.jpg')
        cv2.imwrite(blurred_path, blurred_image)
        return blurred_path

    def obfuscate_freetext(self, text, utility):
        """
        Applies text hashing or sentiment reduction based on sensitivity.
        """
        if utility < 0.3:
            return hashlib.sha256(text.encode()).hexdigest()
        elif utility < 0.6:
            return self.reduce_sentiment(text)  # Mocked sentiment reduction
        return text

    @staticmethod
    def reduce_sentiment(text):
        """
        Mock method to 'reduce sentiment' in text, simulating neutralization of sensitive opinions.
        """
        return "This text has been neutralized for privacy."

    @staticmethod
    def apply_general_obfuscation(value, utility):
        """
        General numeric and string data obfuscation method.
        Adds noise or hashes data based on utility.
        """
        if isinstance(value, (int, float)):
            noise_level = 0.2 / utility  # More noise for sensitive attributes
            return value + (noise_level * random.uniform(-1, 1) * value)
        elif isinstance(value, str) and utility < 0.5:
            return hashlib.sha256(value.encode()).hexdigest()
        return value


def main():
    user_data = {
        "location": "New York, NY",
        "gender": "Male",
        "profile_photo": "profile.jpg",
        "freetext": "Here are some very personal thoughts about my day.",
        "age": 30
    }

    utility_scores = {
        "location": 0.4,
        "gender": 0.8,
        "profile_photo": 0.2,
        "freetext": 0.5,
        "age": 0.9
    }

    attribute_utilities = AttributeUtilities(utility_scores)
    obfuscated_data = attribute_utilities.obfuscate_data(user_data)

    print("Original Data:", user_data)
    print("Obfuscated Data:", obfuscated_data)


if __name__ == "__main__":
    main()
