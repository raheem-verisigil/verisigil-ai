import requests

API_URL = "https://www.verisigilai.com/api/passport"  # adjust if needed

def create_agent(name):
    payload = {
        "name": name
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()

        print("Agent created successfully!")
        print("DID:", data.get("did"))

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    create_agent("example-agent")
