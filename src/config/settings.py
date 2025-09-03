import re

def load_credentials(path: str):
    """Load Neo4j AuraDB credentials from file."""
    with open(path, "r") as f:
        content = f.read()
    uri = re.search(r"NEO4J_URI=(.*)", content).group(1).strip()
    user = re.search(r"NEO4J_USERNAME=(.*)", content).group(1).strip()
    password = re.search(r"NEO4J_PASSWORD=(.*)", content).group(1).strip()
    return uri, user, password
