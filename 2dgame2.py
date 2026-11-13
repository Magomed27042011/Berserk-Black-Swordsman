import secrets
import string

def generate_password(length=16, use_cyrillic=False, avoid_ambiguous=True):
    # Базовые наборы символов
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]{}"

    if avoid_ambiguous:
        # убираем символы, которые легко перепутать при вводе: l, I, 1, O, 0
        ambiguous = "lI1O0"
        lower = ''.join(c for c in lower if c not in ambiguous)
        upper = ''.join(c for c in upper if c not in ambiguous)
        digits = ''.join(c for c in digits if c not in ambiguous)

    pool = lower + upper + digits + special

    if use_cyrillic:
        cyr_lower = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        cyr_upper = cyr_lower.upper()
        pool += cyr_lower + cyr_upper

    if length < 4:
        raise ValueError("Слишком короткий пароль")

    # гарантируем хотя бы по одному символу каждого обязательного типа
    password = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(special),
    ]
    password += [secrets.choice(pool) for _ in range(length - len(password))]

    # перемешиваем, чтобы обязательные символы не стояли всегда в начале
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

print(generate_password(16))