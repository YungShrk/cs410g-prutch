# Filename: vulnerable_script.py
import requests

def send_data_to_server(data):
    """
    Sends data to a remote server.
    Args:
        data (str): Data to send.
    """
    url = "http://example.com/api"
    try:
        response = requests.post(url, data={"payload": data})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending data: {e}")

send_data_to_server("Sensitive Information")

