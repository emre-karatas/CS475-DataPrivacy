import random
import hashlib
import numpy as np
from PIL import Image, ImageFilter
import logging
import math
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
            utility = self.utility_scores.get(key, 1)
            method = getattr(self, f"obfuscate_{key}", self.apply_general_obfuscation)
            obfuscated_data[key] = method(value, utility)
            logging.info(f"Obfuscated {key}: Original Value: {value}, Utility: {utility}")
        return obfuscated_data

    def obfuscate_location(self, location, utility):
        """
        Advanced method to obfuscate geographic locations based on utility.
        Applies different levels of noise and area generalization.
        """
        coordinates_map = {
            "Ankara, TR": (39.925533, 32.866287),
            "San Francisco, CA": (37.7749, -122.4194),
            "Istanbul, TR": (41.015137, 28.979530)
        }

        coordinates = coordinates_map.get(location, (0, 0))

        radius = 1000 if utility < 0.3 else 500 if utility < 0.6 else 100 if utility < 0.8 else 0
        obfuscated_coords = self.add_location_noise(coordinates, radius) if radius else coordinates
        return f"https://maps.google.com/?q={obfuscated_coords[0]},{obfuscated_coords[1]}"

    @staticmethod
    def add_location_noise(coordinates, radius):
        """
        Adds random geospatial noise to coordinates within a specified radius in meters.
        """
        lat, lon = coordinates
        angle = random.uniform(0, 2 * math.pi)
        r = radius * random.uniform(0, 1) ** 0.5
        new_lat = lat + (r * math.cos(angle)) / 111321
        new_lon = lon + (r * math.sin(angle)) / (111321 * math.cos(lat * math.pi / 180))
        return new_lat, new_lon

    @staticmethod
    def obfuscate_gender(gender, utility):
        """
        Gender is either not changed or fully hidden based on sensitivity.
        """
        return "Unspecified" if utility < 0.5 else gender

    def obfuscate_profile_photo(self, photo_path, utility):
        """
        Applies varying levels of privacy techniques to the profile photo based on the utility.
        """
        try:
            image = Image.open(photo_path)
            if utility < 0.3:
                return self.scramble_by_random_permutation(photo_path)
            elif utility < 0.5:
                return self.scramble_by_random_sign_conv(photo_path)
            elif utility < 0.7:
                return self.pixelize_image(photo_path)
            else:
                return self.apply_gaussian_blur(photo_path)
        except IOError:
            logging.error(f"Error opening image {photo_path}")
            return photo_path

    @staticmethod
    def apply_gaussian_blur(photo_path, sigma=8):
        """
        Applies Gaussian blur with a specified standard deviation.
        """
        image = Image.open(photo_path)
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=sigma))
        blurred_path = photo_path.replace('.jpg', '_gaussian_blurred.jpg')
        blurred_image.save(blurred_path)
        return blurred_path

    @staticmethod
    def pixelize_image(photo_path, pixel_size=10):
        """
        Applies pixelization to the image.
        """
        image = Image.open(photo_path)
        image = image.resize(
            (image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST
        )
        image = image.resize(image.size, Image.NEAREST)
        pixelized_path = photo_path.replace('.jpg', '_pixelized.jpg')
        image.save(pixelized_path)
        return pixelized_path

    @staticmethod
    def scramble_by_random_sign_conv(photo_path):
        """
        Scrambles the image by random sign convolution.
        """
        image = Image.open(photo_path)
        np_image = np.array(image)
        sign_mask = np.random.choice([-1, 1], np_image.shape)
        scrambled_image = np_image * sign_mask
        scrambled_path = photo_path.replace('.jpg', '_scrambled_sign_conv.jpg')
        Image.fromarray(scrambled_image.astype(np.uint8)).save(scrambled_path)
        return scrambled_path

    @staticmethod
    def scramble_by_random_permutation(photo_path):
        """
        Scrambles the image by random permutation.
        """
        image = Image.open(photo_path)
        np_image = np.array(image).flatten()
        np.random.shuffle(np_image)
        scrambled_image = np_image.reshape(image.size[1], image.size[0], -1)
        scrambled_path = photo_path.replace('.jpg', '_scrambled_permutation.jpg')
        Image.fromarray(scrambled_image.astype(np.uint8)).save(scrambled_path)
        return scrambled_path

    def obfuscate_freetext(self, text, utility):
        """
        Applies text hashing or sentiment reduction based on sensitivity.
        """
        if utility < 0.3:
            return hashlib.sha256(text.encode()).hexdigest()
        elif utility < 0.6:
            return self.reduce_sentiment(text)
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
            noise_level = 0.2 / utility
            return value + (noise_level * random.uniform(-1, 1) * value)
        elif isinstance(value, str) and utility < 0.5:
            return hashlib.sha256(value.encode()).hexdigest()
        return value


def display_images(original_path, obfuscated_paths):
    """
    Display the original and obfuscated images.
    """
    images = [Image.open(original_path)] + [Image.open(path) for path in obfuscated_paths]
    titles = ["Original"] + [path.split('_')[-1].replace('.jpg', '') for path in obfuscated_paths]

    plt.figure(figsize=(15, 5))
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, len(images), i + 1)
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')
    plt.show()


def save_obfuscated_data(obfuscated_data, filename="obfuscated_data.txt"):
    """
    Save the obfuscated data to a text file.
    """
    with open(filename, "w") as file:
        for key, value in obfuscated_data.items():
            file.write(f"{key}: {value}\n")
    logging.info(f"Obfuscated data saved to {filename}")


def main():
    user_data = {
        "location": "Ankara, TR",
        "gender": "Male",
        "profile_photo": "profile.jpg",
        "freetext": """Hello there! 👋 I'm Emre Karataş, a senior Computer Science student at Bilkent University, and I'm thrilled that you've stumbled upon my GitHub profile!

I'm captivated by the fascinating universe of software engineering, with an enduring passion for Machine Learning, AI, and Data Science. 🧠💻 My repositories here represent that fervor, presenting a series of adventures through a diverse set of programming languages like Java, JavaScript, Python, PHP, C/C++ and a dive into the world of web development with React and Spring.

As you navigate through my profile, you'll encounter tales of innovation, personal growth, and complex problem-solving. I hold a steadfast commitment to creating clean, efficient code, and it's the thirst for continuous learning within this dynamic field that keeps me motivated. Venturing into the expansive domain of AI, Data Science, and Machine Learning, I've discovered that the future is kind to those who can interpret and leverage data effectively.

Each project showcased here tells a story of not just my work, but my evolution as a software developer. Whether you're here to collaborate or simply learn something new, you're always welcome in my digital workspace. So feel free to explore, and enjoy the journey through my realm of code. Happy coding! 🚀💻""",
        "age": 22
    }

    utility_scores = {
        "location": 0.1,
        "gender": 0.3,
        "profile_photo": 0.1,
        "freetext": 0.4,
        "age": 0.9
    }

    attribute_utilities = AttributeUtilities(utility_scores)
    obfuscated_data = attribute_utilities.obfuscate_data(user_data)

    print("Original Data:", user_data)
    print("Obfuscated Data:", obfuscated_data)

    save_obfuscated_data(obfuscated_data)

    original_path = user_data["profile_photo"]
    obfuscated_paths = [
        attribute_utilities.scramble_by_random_permutation(original_path),
        attribute_utilities.scramble_by_random_sign_conv(original_path),
        attribute_utilities.pixelize_image(original_path),
        attribute_utilities.apply_gaussian_blur(original_path)
    ]
    display_images(original_path, obfuscated_paths)


if __name__ == "__main__":
    main()
