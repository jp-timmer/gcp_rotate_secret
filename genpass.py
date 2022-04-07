import string
import secrets

alphabet = string.ascii_letters + string.digits
passwords = ''.join(secrets.choice(alphabet) for i in range(30))

print(passwords)