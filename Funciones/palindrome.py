# **********
# PALÍNDROMO
# **********


def is_palindrome(text: str) -> bool:
    if text[::-1].replace(" ", "").lower() == text.replace(" ", "").lower():
        return True
    else:
        return False
