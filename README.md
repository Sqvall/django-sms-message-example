## Django template for examples

### Project ready to up with docker.

To run use `Makefile`:

```shell
make initialize
```

Or use `long way`:

```shell
cp .env.example .env # or copy manually .env.example to .env
docker-compose up --build -d
docker-compose exec app python manage.py makemigrations --noinput
docker-compose exec app python manage.py migrate --noinput
docker-compose exec app python manage.py createsuperuser --noinput &> /dev/null || true
```

After initialize, you can open django admin:
http://localhost:8080/admin

### Notes

- If you need get access for you uploaded files, your can open http://localhost:49001
  for access to `minio` with _username:_ `SomeKeyID` and _password:_ `SomeSecretKey`.
