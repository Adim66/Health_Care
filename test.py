# test.py
import requests

# URL correcte avec port 8003 et endpoint /api/data
BACKEND_URL = "http://127.0.0.1:8003/api/data"

def main():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            data = response.json()
            print("Derniers messages reçus depuis le serveur :")
            for record in data:
                print(record)
        else:
            print(f"Erreur HTTP : {response.status_code}")
    except Exception as e:
        print(f"Impossible de contacter le serveur : {e}")

if __name__ == "__main__":
    main()
