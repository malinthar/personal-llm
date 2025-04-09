import requests
import argparse

def generate_text(prompt, api_url="http://localhost:8000"):
    """Send a request to the LLM API and get a response."""
    endpoint = f"{api_url}/generate"
    payload = {
        "prompt": prompt,
        "max_length": 512,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()["text"]
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for LLM API")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt for the model")
    parser.add_argument("--api_url", type=str, default="http://localhost:8000", help="URL of the API server")
    
    args = parser.parse_args()
    
    response = generate_text(args.prompt, args.api_url)
    if response:
        print("Response:", response)
