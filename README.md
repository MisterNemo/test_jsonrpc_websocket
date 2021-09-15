# Sber Lab test project

## Project setup
```
docker-compose build
```
```
docker-compose up -d
```
```
docker-compose exec app python manage.py makemigrations
```
```
docker-compose exec app python manage.py migrate
```


### User requests examples
_Create user_
```
curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=test&password=pretendtobe'
```
_Get token_
```
curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'username=test&password=pretendtobe'
```

### Url for WS connection
[ws://127.0.0.1:8000/ws/{token}
](ws://127.0.0.1:8000/ws/{token})

### Request examples
_send a message to yourself:_
`{
  "jsonrpc": "2.0",
  "method": "sendEcho",
  "params": {
    "message": "Hi"
  },
  "id": 1
}`

_send a message to public chat:_
`{
  "jsonrpc": "2.0",
  "method": "chat",
  "params": {
    "message": "Hi"
  },
  "id": 6
}`

_send a private message to certain people or everyone_
`{
  "jsonrpc": "2.0",
  "method": "sendMessage",
  "params": {
    "ids": [3, 2],
    "message": "Hi"
  },
  "id": 6
}`
for all people: `"ids": "*"
`