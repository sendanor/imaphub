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
