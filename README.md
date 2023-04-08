# imaphub

IMAP to REST API microservice

### Run the server

```shell
docker-compose up --build
```

### Run unit tests

```shell
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Run system tests

```shell
docker-compose -f docker-compose.systemtest.yml up --build --abort-on-container-exit
```

#### Running in development mode (and reload on changes)

```shell
docker-compose -f docker-compose.dev.yml up --build
```

### Testing the API manually

#### Sending a message as JSON

```shell
curl -i -X POST -H 'Content-Type: application/json' -d '{"subject": "Test email", "from": "foo@example.com", "to": "bar@example.com", "body": "Hello world"}' http://localhost:4001/v1/messages 
```

#### Sending a message as rfc822

```shell
curl -i -X POST -H "Content-Type: message/rfc822" --data-binary "@samples/email.eml" http://localhost:4001/v1/messages
```

#### Listing messages

```shell
curl -i http://localhost:4001/v1/messages
```

### Using Virtual ENV

#### Opening Python venv on Linux/Mac

```shell
python -m venv venv
source venv/bin/activate
```

#### Installing new requirements

```shell
pip install imaplib
```

#### Freeze requirements

```shell
pip freeze > requirements.txt
```

#### Running Flask in development mode

```shell
flask --app app.py --debug run --reload --host=0.0.0.0 --port=4001
```
