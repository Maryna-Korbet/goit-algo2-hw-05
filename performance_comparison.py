from colorama import Fore, Style, init
import time
from datasketch import HyperLogLog
import re
from tabulate import tabulate
from typing import List
import os

try:
    import gdown
except ImportError:
    raise ImportError("Please install gdown: pip install gdown")


init(autoreset=True)


def download_file_from_gdrive(file_id: str, output: str):
    """
    Download a file from Google Drive by file_id if it does not exist locally.
    """
    if not os.path.exists(output):
        print(Fore.YELLOW + f"File '{output}' not found locally. Downloading from Google Drive..." + Style.RESET_ALL)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)
        print(Fore.GREEN + f"Downloaded '{output}' successfully." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"File '{output}' already exists locally. Skipping download." + Style.RESET_ALL)


def load_data(file_path: str) -> List[str]:
    """
    Load IP addresses from the log file, ignoring malformed lines.
    Validates IPv4 addresses loosely.
    """
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    ip_addresses = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    ip = match.group()
                    if all(0 <= int(octet) <= 255 for octet in ip.split(".")):
                        ip_addresses.append(ip)
    except (FileNotFoundError, UnicodeDecodeError, Exception) as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        raise

    if not ip_addresses:
        raise ValueError("No valid IP addresses found in the file.")

    return ip_addresses


def exact_count_unique_ips(ip_addresses: List[str]) -> int:
    """Return exact count of unique IP addresses using a set."""
    return len(set(ip_addresses))


def hyperloglog_count_unique_ips(ip_addresses: List[str], p: int = 14) -> int:
    """
    Estimate unique IP addresses count using HyperLogLog.
    p - precision parameter (higher means better accuracy, more memory).
    """
    hll = HyperLogLog(p)
    for ip in ip_addresses:
        hll.update(ip.encode("utf-8"))
    return int(hll.count())


def compare_methods(ip_addresses: List[str]):
    """Compare performance and results of exact count vs HyperLogLog."""

    start_time = time.perf_counter()
    exact_count = exact_count_unique_ips(ip_addresses)
    exact_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    hll_count = hyperloglog_count_unique_ips(ip_addresses)
    hll_time = time.perf_counter() - start_time

    data = [
        ["Unique Elements", exact_count, hll_count],
        ["Execution Time (sec)", f"{exact_time:.4f}", f"{hll_time:.4f}"],
    ]

    print(Fore.CYAN + "Comparison Results:" + Style.RESET_ALL)
    print(tabulate(data, headers=["Metric", "Exact Count", "HyperLogLog"], tablefmt="grid"))


if __name__ == "__main__":
    gdrive_file_id = "1kQuHo_UCWjWKAIkjQ0TlIRrB0kJpaV0Z"  
    local_file_path = "lms-stage-access.log"

    try:
        download_file_from_gdrive(gdrive_file_id, local_file_path)
        ip_addresses = load_data(local_file_path)
        compare_methods(ip_addresses)
    except Exception as e:
        print(Fore.RED + f"Program terminated with error: {e}" + Style.RESET_ALL)
