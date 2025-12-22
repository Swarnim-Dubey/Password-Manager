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
        print(f"decode error : {e}")
        return b""
    
print("-" * 20, "BASE64 TEST (TESTING_PHASE)", "-" * 20)
print()

while True:
    print("\n What you want to do?")
    print("1. Encode")
    print("2. Decode")
    print("3. Exit")

    ch = int(input("Enter choice : "))

    if ch == 1:
        s = input("Enter the text to encode : ")
        out = encode_b64(s.encode("utf-8"))
        print(f"Encoded text = {out}")

    elif ch == 2:
        s = input("Enter the text to decode : ")
        result = decode_b64(s)
        try:
            print(f"Decode text = {result.decode("utf-8")}")
        except:
            print("Not decodeabloe to text, raw bytes detected were : ", result)
    elif ch == 3:
        print("Bye!!")
        break
    else:
        print("Wromg choice was entered")
