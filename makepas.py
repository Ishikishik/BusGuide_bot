import secrets
import string

# 使う文字セット
characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{};:,.<>?"

# 10桁のランダム文字列生成
random_str = ''.join(secrets.choice(characters) for _ in range(10))
print(random_str)
