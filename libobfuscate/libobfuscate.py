import re
import random
import string

__name__ = 'libobfuscate'
__version__ = '1.0.0'
#__author__ = ''
__description__ = 'A module to obfuscate placeholders in a string with variable-lenth random strings.'

def obfuscate(s, chars, min_length, max_length):
    """
    Obfuscates placeholders in the input string with random strings.

    Parameters:
    s (str):             The input string containing placeholders.
    chars (list of str): List of character sets to use ('?u' for uppercase, '?l' for lowercase, '?d' for digits).
    min_length (int):    Minimum length of the generated random string.
    max_length (int):    Maximum length of the generated random string.

    Returns:
    str: The input string with placeholders replaced by random strings.

    Example:
    >>> obfuscate('<%=obf placeholder %>', ['?u', '?l'], 5, 10)
    'AbcDeFgHiJ'
    """

    if not isinstance(s, str):
        raise ValueError("Input must be a string.")

    if not isinstance(chars, list):
        raise ValueError("Chars must be a list of strings representing character sets (?u, ?l, ?d).")

    if not all(isinstance(char, str) and char in ['?u', '?l', '?d'] for char in chars):
        raise ValueError(f"Chars must be a list containing only {' '.join(valid_char_sets)}.")

    if not (isinstance(min_length, int) and isinstance(max_length, int) and min_length > 0 and max_length >= min_length):
        raise ValueError("min_length and max_length must be positive integers with max_length >= min_length.")

    pattern = r'<%=obf (.*?) %>'
    placeholder_values = {}

    first_character = ''
    all_characters  = ''

    characters = {
        '?u': string.ascii_uppercase,
        '?l': string.ascii_lowercase,
        '?d': string.digits
    }
    for i in chars:
        if i in characters.keys():
            all_characters += characters[i]
        if i != '?d':
            first_character += characters[i]

    if not first_character:
        raise ValueError("At least one of '?u' or '?l' must be included in chars.")

    def get_or_generate_random_string(match):
        placeholder = match.group(1)
        if placeholder not in placeholder_values:
            length = random.randint(min_length, max_length)
            random_string = random.choice(first_character)
            random_string += ''.join(random.choice(all_characters) for _ in range(length - 1))
            placeholder_values[placeholder] = random_string
        return placeholder_values[placeholder]

    result_string = re.sub(pattern, get_or_generate_random_string, s)

    return result_string
