# base64 encoding testing

import base64
# from security.base64_utils import base64_encode, base64_decode

def base64_encode(data: bytes) -> str:
    """
    Encodes binary data into a Base64 string.
    """
    encoded_bytes = base64.b64encode(data)
    return encoded_bytes.decode("utf-8")

def base64_decode(data: str) -> bytes:
    """
    Decodes a Base64 string back into binary data.
    """
    decoded_bytes = base64.b64decode(data.encode("utf-8"))
    return decoded_bytes


print("-" * 20)
print(" BASE64 ENCODER / DECODER (TESTING) ")
print("-" * 20)

while True:
    print("\nChoose an option:")
    print("1. Encode to Base64")
    print("2. Decode from Base64")
    print("3. Exit")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        text = input("\nEnter text to encode: ")
        encoded = base64_encode(text.encode("utf-8"))
        print("\nBase64 Encoded Output:")
        print(encoded)

    elif choice == "2":
        encoded = input("\nEnter Base64 string to decode: ")
        try:
            decoded = base64_decode(encoded)
            print("\nDecoded Output:")
            print(decoded.decode("utf-8"))
        except Exception:
            print("\nInvalid Base64 string")

    elif choice == "3":
        print("\nExiting Base64")
        break

    else:
        print("\nInvalid choice")
