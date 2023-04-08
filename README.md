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
