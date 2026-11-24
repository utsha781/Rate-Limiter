import urllib.request
import urllib.error

url = "http://127.0.0.1:5000/api/data"

users = ["user1", "user2"]

for user in users:

    print("\nTesting:", user)

    headers = {"X-User-ID": user}

    for i in range(1, 7):

        req = urllib.request.Request(url, headers=headers)

        try:
            response = urllib.request.urlopen(req)
            print(f"Request {i}: {response.status} - ALLOWED")

        except urllib.error.HTTPError as e:
            print(f"Request {i}: {e.code} - REJECTED")
            print(e.read().decode())