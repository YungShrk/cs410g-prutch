# Filename: obfuscated_script.py
def get_message():
    encoded_chars = [chr(ord(c) ^ 42) for c in "Jgnnq\"Yqtnf!"]
    message = "".join(encoded_chars)
    return message

print(get_message())

