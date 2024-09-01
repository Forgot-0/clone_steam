

def convert_bytes_to_str(value: dict[bytes, bytes]) -> dict[str, str]:
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in value.items()}
