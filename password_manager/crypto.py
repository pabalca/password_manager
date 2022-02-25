import base64
import hashlib
import os

from Crypto.Cipher import AES


class Cypher:
    def __init__(self):
        password = os.environ.get(
            "FLASK_ENCRYPTION_KEY",
            "mousefridgecurtainpaintingwebcam192-012ramones",
        )
        self.key = hashlib.sha256(password.encode("utf-8")).digest()

        BLOCK_SIZE = 16
        self.pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
            BLOCK_SIZE - len(s) % BLOCK_SIZE
        )
        self.unpad = lambda s: s[:-ord(s[len(s) - 1 :])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            return bytes.decode(self.unpad(cipher.decrypt(enc[16:])), "utf-8")
        except UnicodeDecodeError:
            return ""
