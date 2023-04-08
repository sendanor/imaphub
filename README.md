# imaphub

IMAP to REST API microservice

### Run the server over docker-compose

```shell
docker-compose up --build
```

### Run unit tests over docker-compose

```shell
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Run system tests over docker-compose

```shell
docker-compose -f docker-compose.systemtest.yml up --build --abort-on-container-exit
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

#### Running Flask in development mode

```shell
flask --app app.py --debug run --reload
```

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
