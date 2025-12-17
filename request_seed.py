import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23A91A6183"   # ⚠️ mee exact student ID
REPO_URL = "https://github.com/bhargavmartha/pki"  
# ⚠️ MUST be EXACT repo URL (mee actual GitHub repo URL pettu)

with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": REPO_URL,
    "public_key": public_key
}

response = requests.post(API_URL, json=payload, timeout=30)
response.raise_for_status()

data = response.json()

encrypted_seed = data["encrypted_seed"]

with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

print("✅ encrypted_seed.txt created successfully")
