import alphabet


def encrypt(text, key):
    text = list(text)
    key = key % 26
    position = 0
    for r in range(0, len(text)):
        if text[r].isspace() or text[r].isdigit():
            text[r] = text[r]
        else:
            position = alphabet.alphabetENG.index(text[r])
            position += key
            text[r] = alphabet.alphabetENG[position]

    return ''.join(text)