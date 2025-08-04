import ulid

def generate_ulid():
    """Generate a ULID."""
    return str(ulid.new())

