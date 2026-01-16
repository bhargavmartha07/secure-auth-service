import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# 🔴 PASTE YOUR COMMIT HASH HERE
COMMIT_HASH = "6cbbc9b52c3a9ccc6672331dab10de8e09cdd78f"

# Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Sign commit hash (ASCII string!)
signature = private_key.sign(
    COMMIT_HASH.encode("utf-8"),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(f.read())

# Encrypt signature using RSA-OAEP SHA256
encrypted_signature = instructor_public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Base64 encode (SINGLE LINE)
final_signature = base64.b64encode(encrypted_signature).decode()

print("===== ENCRYPTED COMMIT SIGNATURE (SUBMIT THIS) =====")
print(final_signature)
