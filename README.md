# line-provider - Провайдер информации о событиях 

### Перед запуском:
- создать ```.env``` в src и в корне, скопировав ```.env.sample``` (соответственно ```src/.env.sample > src/.env``` и ```.env.sample > .env```)
- если установлена утилита `make`, то запустить команду `make create-network`
- если утилита `make` не установлена, тогда запускаем `docker network create storage_default || echo "Network already exists"`
- билдим образ: `make build` или `docker-compose build`.


### Запуск:
- `make up` или `docker-compose up`


### Стоит запускать этот сервис совместно с ```bet-maker```, потому что эти сервисы связаны, и логика в них связана (в docker-compose предусмотрен одновременный запуск сервисов). При одельном запуске этого сервиса некоторые функции могут не работать.