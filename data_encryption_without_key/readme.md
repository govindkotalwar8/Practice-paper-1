## Create a text file with some sensitive text. Share this file with the other developer by encrypting it without a shared password. Else sharing the password itself can be tricky. The encryption should happen on the command line in a linux machine. Use docker if needed.

# Data Encryption Without Shared Password

```
gpg --full-generate-key
gpg --list-keys
gpg --export -a govindkotalwargk@gmail.com > Govind-public.key

gpg --encrypt --recipient govindkotalwargk@gmail.com secret.txt

gpg --decrypt secret.txt.gpg > decrypted.txt

cat decrypted.txt


```
