from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from os import chmod

# generate private/public key pair
key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
    key_size=2048)

# get public key in OpenSSH format
public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
    serialization.PublicFormat.OpenSSH)

# get private key in PEM container format
pem = key.private_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())

# decode to printable strings
private_key_str = pem.decode('utf-8')
public_key_str = public_key.decode('utf-8')

print('Private key = ')
print(private_key_str)
print('Public key = ')
print(public_key_str)


with open("/tmp/private.key", 'w') as f:
    chmod("/tmp/private.key", 0o0600)
    f.write(private_key_str)

with open("/tmp/public.key", 'w') as f:
    f.write(public_key_str)
