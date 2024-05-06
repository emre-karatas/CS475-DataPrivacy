import random
import hashlib


class DataObfuscation:
    @staticmethod
    def hash_data(data):
        """
        Hashes the given data using SHA256 algorithm and returns the hexadecimal representation of the hash value.

        :param data: The data to be hashed.
        :type data: str
        :return: The hexadecimal representation of the hashed data.
        :rtype: str
        """
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def noise_addition(data, noise_level=0.1):
        """
        Apply noise addition to the given data.

        :param data: The input data to which noise will be added. It can be an integer, float, or another data type.
        :param noise_level: The level of noise to be added. The default value is 0.1.

        :return: The input data with noise added to it.
        """
        if isinstance(data, int) or isinstance(data, float):
            noise = data * noise_level * random.uniform(-1, 1)
            return data + noise
        return data


class SelectiveSharingController:
    def __init__(self, user_settings):
        """Initializes with user-specific settings."""
        self.settings = user_settings

    def filter_data(self, data):
        """Filters data based on user privacy settings."""
        filtered_data = {}
        for key, value in data.items():
            if self.settings.get(key, False):
                filtered_data[key] = value
        return filtered_data


def main():
    """
    The `main` method is the entry point of the program. It initializes some user data and settings, performs data obfuscation on the salary, filters the data based on user settings, and then prints the original and shared data.

    :return: None
    """
    user_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "salary": 50000
    }

    user_settings = {
        "name": True,
        "age": False,
        "email": False,
        "salary": True
    }

    obfuscation = DataObfuscation()
    user_data["salary"] = obfuscation.noise_addition(user_data["salary"])

    sharing_controller = SelectiveSharingController(user_settings)
    shared_data = sharing_controller.filter_data(user_data)

    print("Original Data:", user_data)
    print("Shared Data:", shared_data)


if __name__ == "__main__":
    main()
