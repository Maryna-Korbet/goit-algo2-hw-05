from bitarray import bitarray
import mmh3
from colorama import Fore, Style, init
from typing import List, Dict, Union

init(autoreset=True)


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        """
        Initialize the Bloom Filter.
        :param size: Size of the bit array.
        :param num_hashes: Number of hash functions to use.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _get_indexes(self, item: str) -> List[int]:
        """
        Generate multiple hash indexes for the given item.
        :param item: String to hash.
        :return: List of bit array positions.
        """
        return [mmh3.hash(item, i) % self.size for i in range(self.num_hashes)]

    def add(self, item: str) -> None:
        """
        Add an item to the Bloom Filter.
        :param item: String to add.
        """
        if not isinstance(item, str) or not item:
            return
        for index in self._get_indexes(item):
            self.bit_array[index] = 1

    def contains(self, item: str) -> bool:
        """
        Check if an item might be in the Bloom Filter.
        :param item: String to check.
        :return: True if the item might be present, False if definitely not.
        """
        if not isinstance(item, str) or not item:
            return False
        return all(self.bit_array[index] for index in self._get_indexes(item))


def check_password_uniqueness(bloom: BloomFilter, passwords: List[Union[str, None]]) -> Dict[str, str]:
    """
    Check the uniqueness of passwords using a Bloom Filter.
    :param bloom: BloomFilter instance.
    :param passwords: List of passwords to check.
    :return: Dictionary mapping password to its status ('already used', 'unique', or 'invalid').
    """
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            results[str(password)] = "invalid"
            continue

        if bloom.contains(password):
            results[password] = "already used"
        else:
            results[password] = "unique"
            bloom.add(password)  # Add to the filter so future checks consider it used
    return results


if __name__ == "__main__":
    # Initialize the Bloom Filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Passwords to check
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print results
    print("\nPassword check results:")
    for password, status in results.items():
        if status == "already used":
            color = Fore.RED
        elif status == "unique":
            color = Fore.GREEN
        else:
            color = Fore.YELLOW
        print(f"{Fore.CYAN}Password '{password}' - {color}{status}{Style.RESET_ALL}.")