from Crypto.PublicKey import RSA
privateRSAKey = RSA.generate(4096)
publicRSAKey = privateRSAKey.publickey()
print privateRSAKey.exportKey()
print publicRSAKey.exportKey()
