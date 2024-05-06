import random
import hashlib


class AttributeUtilities:
    def __init__(self, utility_scores):
        """
        Initialize with a dictionary of attribute utility scores.
        Lower scores mean higher sensitivity and need for more obfuscation.
        """
        self.utility_scores = utility_scores

    def obfuscate_data(self, data):
        """
        Obfuscates data based on utility scores.
        More sensitive data (lower utility score) will receive stronger obfuscation.
        """
        obfuscated_data = {}
        for key, value in data.items():
            utility = self.utility_scores.get(key, 1)  # Default utility is 1 (normal sensitivity)
            obfuscated_data[key] = self.apply_obfuscation(value, utility)
        return obfuscated_data

    @staticmethod
    def apply_obfuscation(value, utility):
        """
        Applies obfuscation based on the utility of the attribute.
        Lower utility attributes get higher noise addition or hashing.
        """
        if isinstance(value, (int, float)):
            noise_level = 0.1 / utility  # Increase noise for sensitive attributes
            return value + (noise_level * random.uniform(-1, 1) * value)
        elif isinstance(value, str) and utility < 0.5:  # Consider hashing very sensitive string data
            return hashlib.sha256(value.encode()).hexdigest()
        return value


def main():
    user_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "salary": 50000
    }

    # Example utility scores: Lower score indicates higher sensitivity
    utility_scores = {
        "name": 0.8,  # Name is moderately sensitive
        "age": 0.9,  # Age is less sensitive
        "email": 0.3,  # Email is highly sensitive
        "salary": 0.2  # Salary is very sensitive
    }

    attribute_utilities = AttributeUtilities(utility_scores)
    obfuscated_data = attribute_utilities.obfuscate_data(user_data)

    print("Original Data:", user_data)
    print("Obfuscated Data:", obfuscated_data)


if __name__ == "__main__":
    main()
