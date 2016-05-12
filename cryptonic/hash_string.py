import hashlib


class StringEncryption:
    def __init__(self, string_to_hash):
        self.string_to_hash = string_to_hash

    #   @params string_to_hash
    #   Return the sha256 hash of string_to_hash
    def hashStringMd5(self):
        hash_object = hashlib.md5(self.string_to_hash)
        return hash_object.hexdigest()

    # Generates a random 16 digit invite key
    def generate_invite_key():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                string.digits + string.ascii_lowercase) for _ in range(16))
