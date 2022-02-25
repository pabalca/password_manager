# password_manager
Password manager web app. Specifications:
- Uses BIP39 or EFF Diceware wordlists to create high entropy passwords.
- Passwords are stored using AES encryption with a key per environment.
- User management system.

## Configuration
Change the encryption key `ENV FLASK_ENCRYPTION=somethingstrong` in the Dockerfile.

## Build docker image and run it
```
docker build -t passwords .
docker run --name secretsweb -v sqldata1:/usr/src/passwords/database -p 8000:5000 passwords
```

## Create user
An user is just defined by its password, no usernames here.
```
docker exec -it secretsweb flask createuser
```
