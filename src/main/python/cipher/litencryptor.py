from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
from base64 import b64decode


COMMON_INITIAL_VECTOR = bytes("abcdef1234567890", "ascii")

SGPOSS_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
SECURE_ENDPOINTS_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
CHAT_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_1_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_2_KEY = "EIOWUGWOERGJKNLDKGJFOI879KJNSDKJ"
MODE_3_KEY = "f1c9208ccd8ef6d85c44b451da593cd4"
MODE_4_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
MODE_5_KEY = "LTMWUGWOBNLJKIOEKGJFOI256KIOWNKF"

def decrypt_with_custom_iv(data: str, key: str, iv: bytes) -> str:
    aes = AES.new(bytes(key, "ascii"), AES.MODE_CBC, iv)
    return unpad(aes.decrypt(b64decode(bytes(base64_decode_transform(data), "utf8"))), AES.block_size).decode("utf-8")


def encrypt_with_custom_iv(data: str, key: str, iv: bytes) -> str:
    aes = AES.new(bytes(key, "ascii"), AES.MODE_CBC, iv)
    return b64encode(aes.encrypt(pad(bytes(data, "utf8"), AES.block_size))).decode("utf-8")


def base64_decode_transform(input: str) -> str:
    return input.replace("-", "+").replace("_", "/").replace(".", "=")


def base64_encode_transform(input: str) -> str:
    return input.replace("+", "-").replace("/", "_").replace("=", ".")


def decrypt_libguard(data: str, mode: int) -> str:
    if mode == 1:
        return decrypt_with_custom_iv(data, MODE_1_KEY, COMMON_INITIAL_VECTOR)
    if mode == 2:
        return decrypt_with_custom_iv(data, MODE_2_KEY, COMMON_INITIAL_VECTOR)
    if mode == 3:
        input_data = b64decode(base64_decode_transform(data))
        encrypted_data = input_data[0:-0x10]
        iv = input_data[-0x10:]
        aes = AES.new(bytes(MODE_3_KEY, "ascii"), AES.MODE_CBC, iv)
        return unpad(aes.decrypt(encrypted_data), AES.block_size).decode("utf-8")

    if mode == 4:
        return decrypt_with_custom_iv(data, MODE_4_KEY, COMMON_INITIAL_VECTOR)
    if mode == 5:
        return decrypt_with_custom_iv(data, MODE_5_KEY, COMMON_INITIAL_VECTOR)
    raise ValueError("Mode can only be 1 ~ 5, but found " + str(mode) + " instead!")


def encrypt_libguard(data: str, mode: int) -> str:

    if mode == 1:
        return base64_encode_transform(encrypt_with_custom_iv(data, MODE_1_KEY, COMMON_INITIAL_VECTOR))
    if mode == 2:
        return base64_encode_transform(encrypt_with_custom_iv(data, MODE_2_KEY, COMMON_INITIAL_VECTOR))
    if mode == 3:
        iv = get_random_bytes(0x10)

        aes = AES.new(bytes(MODE_3_KEY, "ascii"), AES.MODE_CBC, iv)
        encrypted_data = aes.encrypt(pad(bytes(data, "utf8"), AES.block_size))
        result = base64_encode_transform(b64encode(encrypted_data + iv).decode("utf-8"))
        return result
    if mode == 4:
        return base64_encode_transform(encrypt_with_custom_iv(data, MODE_4_KEY, COMMON_INITIAL_VECTOR))
    if mode == 5:
        return base64_encode_transform(encrypt_with_custom_iv(data, MODE_5_KEY, COMMON_INITIAL_VECTOR))
    raise ValueError("Mode can only be 1 ~ 5, but found " + str(mode) + " instead!")

# litencryptor.decrypt_libguard(litencryptor.encrypt_libguard("Hello, WorldDDDDDDDDDDDDDDDDDDD!", 3), 3)