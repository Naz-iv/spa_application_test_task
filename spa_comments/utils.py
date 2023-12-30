import random
import string


def generate_random_alphanumeric_challenge(length=6):
    challenge = u""
    response = u""
    characters = string.ascii_letters + string.digits
    for _ in range(length):
        digit = random.choice(characters)
        challenge += digit
        response += digit
    return challenge, response
