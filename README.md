# Task 1: Bloom Filter Password Uniqueness Checker

This project implements a Bloom Filter to efficiently check the uniqueness of passwords without storing the actual passwords. It allows you to quickly determine if a password was used before, using minimal memory.

## Features

- **BloomFilter class**: Implements a Bloom Filter with customizable size and number of hash functions.
- **check_password_uniqueness function**: Checks a list of passwords against the Bloom Filter and returns their uniqueness status.
- Handles invalid inputs (e.g., empty strings, None).
- Automatically adds new unique passwords to the Bloom Filter for future checks.
- Uses `mmh3` (MurmurHash3) for hashing and `bitarray` for compact bit storage.
- Colored console output with `colorama` for clear status visualization.

## Installation

Make sure you have Python 3.6+ installed.

Install required dependencies:

```bash
pip install bitarray mmh3 colorama
python bloom_filter.py
```
---
