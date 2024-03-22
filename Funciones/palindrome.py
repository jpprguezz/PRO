# **********
# PALÍNDROMO
# **********


def is_palindrome(text: str) -> bool:
    return text.replace(' ', "")[::-1].lower() == text.replace(' ', "").lower()
