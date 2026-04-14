## Create a text file with some sensitive text. Share this file with the other developer by encrypting it with a shared password. The encryption should happen on the command line in a linux machine. Use docker if needed

## Encryption Command

```
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -in test.decrypted  -out test.encrypted

```

## Decryption Command

```

openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 -in test.encrypted -out test.decrypted

```

