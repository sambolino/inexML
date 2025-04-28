import requests
from .molecules import MOLECULES

BASE_URL = "http://servo.aob.rs/mold/"

def get_XY(identifier: str, quantum_number_1: int, quantum_number_2: int):
    """
    Fetch XY data for a molecule via web request.

    Args:
        identifier (str): InChIKey identifier.
        quantum_number_1 (int): First quantum number (e.g., vibrational state).
        quantum_number_2 (int): Second quantum number (e.g., rotational state).

    Returns:
        dict: JSON response containing the data.

    Raises:
        Exception: If the request fails.
    """
    endpoint = f"{BASE_URL}get_XY/{identifier}/{quantum_number_1}/{quantum_number_2}/"
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

