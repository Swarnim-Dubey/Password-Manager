# base64 testing script
# just trying out encode/decode with the libraries

import base64

def encode_b64(data: bytes) -> str:
    # turn bytes into base64 string
    b = base64.b64encode(data)
    return b.decode("utf-8")

def decode_b64(txt: str) -> bytes:
    # turn base64 string back to bytes
    try:
        b = base64.b64decode(txt.encode("utf-8"))
        return b
    except Exception as e:
        print("decode error:", e)
        return b""


