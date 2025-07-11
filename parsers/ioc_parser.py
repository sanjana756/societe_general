import re
from typing import List

# Quick sanity‐check at import time
print("Running IOC parser…")

# Regex patterns for common IOCs
IPV4_PATTERN    = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
URL_PATTERN     = r"\bhttps?://[^\s'\"<>]+\b"
MD5_PATTERN     = r"\b[a-fA-F0-9]{32}\b"
SHA256_PATTERN  = r"\b[a-fA-F0-9]{64}\b"
HASH_PATTERN    = f"(?:{MD5_PATTERN}|{SHA256_PATTERN})"

PATTERNS = {
    "IPv4": re.compile(IPV4_PATTERN),
    "URL":  re.compile(URL_PATTERN),
    "Hash": re.compile(HASH_PATTERN),
}

def extract_iocs(text: str) -> List[str]:
    """
    Scan text and return a sorted, de‐duplicated list of all matches
    for each IOC pattern.
    """
    found = set()
    for name, pattern in PATTERNS.items():
        for match in pattern.findall(text):
            found.add(match)
    return sorted(found)

if __name__ == "__main__":
    sample = (
        "Malicious IPs: 192.168.1.5, 10.0.0.1; "
        "Download at http://bad.example.com/malware.exe; "
        "Sample hashes: d41d8cd98f00b204e9800998ecf8427e, "
        # full 64-char SHA256 (empty‐string hash for example)
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    print("IOCs found:", extract_iocs(sample))
