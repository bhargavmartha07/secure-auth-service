from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64, os, time, pyotp
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

DATA_PATH = "/data/seed.txt"

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str


def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def hex_to_base32(hex_seed: str) -> str:
    return base64.b32encode(bytes.fromhex(hex_seed)).decode()


@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    try:
        private_key = load_private_key()
        encrypted_bytes = base64.b64decode(req.encrypted_seed)

        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        seed = decrypted.decode().strip()

        if len(seed) != 64:
            raise ValueError("Invalid seed length")

        os.makedirs("/data", exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    totp = pyotp.TOTP(hex_to_base32(seed))
    code = totp.now()
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    totp = pyotp.TOTP(hex_to_base32(seed))

    valid = totp.verify(req.code, valid_window=1)
    return {"valid": valid}
