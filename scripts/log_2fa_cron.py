import pyotp, base64, datetime

SEED_PATH = "/data/seed.txt"

try:
    seed = open(SEED_PATH).read().strip()
    base32 = base64.b32encode(bytes.fromhex(seed)).decode()
    totp = pyotp.TOTP(base32)
    code = totp.now()

    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts} - 2FA Code: {code}")

except Exception as e:
    print("ERROR:", e)
