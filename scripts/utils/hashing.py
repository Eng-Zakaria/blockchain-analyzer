import hashlib

def anonymize_address(address):
    """Pseudonymize wallet addresses for privacy"""
    return hashlib.sha256(address.encode()).hexdigest()[:40]
