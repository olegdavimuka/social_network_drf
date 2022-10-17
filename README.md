## Unzip env.zip (password: secret)
```sh
unzip env.zip
```
## Start the app
```sh
docker-compose up
```

## Send POST to api/token/ to get token (change username and password)
```sh
curl -X POST -d "username=admin&password=admin" http://localhost:8000/api/token/
```
