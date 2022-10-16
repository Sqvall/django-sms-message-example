## Django sms integration

Repository prepare for [article](https://blog.sq-dev.net/articles/integraciya-sms-soobshenij-v-django-prilozhenie).

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

After initialize, you can open form for example: http://localhost:8080/

### Введение

Тут описан один из возможных способов интеграции sms рассылки из Django приложения.

Постараюсь осветить основные моменты данного решения в описании, а также вы можете самостоятельно ознакомиться с реализацией по ссылке из [репозитория](https://github.com/Sqvall/django-sms-message-example).

### Описание

Создаём интерфейс для наших реализаций адаптеров (в примере названы `backends`, т.к. хотелось сделать похожим на встроенный в Django - EmailMessage).

```python
class BaseSmsBackend(metaclass=ABCMeta):
    """ Base SMS backend class. """

    def __init__(self, **options):
        pass

    @abstractmethod
    def send_sms(self, phone_numbers: List[str], message: str):
        """ Sends a message to the specified numbers. """
        raise NotImplementedError()

```

Ограничимся конструктором и одним методом, т.к. этого достаточно для примера.

Теперь мы можем создать свои реализации:

Для тестов можно реализовать заглушку.

```python
class SmsBackend(BaseSmsBackend):
    """
    Dummy sms backend that does nothing.

    Configuration example.

    Modify your settings.py:
        SMS_SETTINGS = {
            "BACKEND": "notifications.sms.backends.dummy.SmsBackend",
        }
    """

    def send_sms(self, phone_numbers: List[str], message: str):
        pass
```

А для реального SMS провайдера подобную реализацию.

```python
class SmsBackend(BaseSmsBackend):
    """
    SMSC SMS backend class.

    Configuration example.

    Modify your settings.py:
        SMS_SETTINGS = {
            "BACKEND": "notifications.sms.backends.smsc.SmsBackend",
            "OPTIONS": {
                "SMSC_LOGIN": "your_login",  # Login from https://smsc.ru
                "SMSC_PASSWORD": "your_password",  # Password
                "SMSC_DEBUG": False,  # Debug flag
                "SMSC_SENDER": False,  # Sender for message
            }
        }

    For more setting see: `SmscConfig`
    """

    def __init__(self, **options):
        super().__init__(**options)
        config = SmscConfig(**options)
        self.client = SMSC(config=config)

    def send_sms(self, phone_numbers: List[str], message: str):
        try:
            self.client.send_sms(','.join(phone_numbers), message)
        except SmscApiException:
            raise
```

В данном примере используется сервис [СМС-центр](https://smsc.ru/) (но любая другая реализация будет похожа).

Также вам возможно понадобиться [зарегистрировать](https://smsc.ru/senders/edit/) имя отравителя. ([правила](https://smsc.ru/faq/88/kakie+suschestvuyut+ogranicheniya+na+ispolzovanie+imeni+otpravitelya+sender+id/))

На сайте у них есть [библиотека](https://smsc.ru/api/code/libraries/http_smtp/python/#menu) для python, для её использования, требуются доработки.

Добавим обработку ошибок и создадим класс настроек + небольшие доработки, результат можете посмотреть в `notifications/sms/smsc_api`.

Опишем процесс выбора конкретного адаптера из настроек проекта в `notifications/sms/backends/__init__.py`

```python
def get_sms_backend() -> _BaseSmsBackend:
    backend_import = settings.SMS_SETTINGS.get("BACKEND")
    if not backend_import:
        raise ImproperlyConfigured(
            "Please specify BACKEND in SMS_SETTINGS within your settings"
        )

    backend_cls = import_string(backend_import)
    if settings.SMS_SETTINGS.get("OPTIONS", None):
        return backend_cls(**settings.SMS_SETTINGS["OPTIONS"])
    else:
        return backend_cls(**{})
```

И наконец мы можем реализовать основной класс для SMS сообщений - `SMSMessage`

```python
class SMSMessage:
    def __init__(self, phone_numbers: List[str], message: str):
        self.phone_numbers = phone_numbers
        self.message = message
        self._backend: BaseSmsBackend = get_sms_backend()

    def send(self):
        self._backend.send_sms(phone_numbers=self.phone_numbers, message=self.message)
```

И добавим настройки в файл `settings.py`

```python
SMS_SETTINGS = {
    "BACKEND": "notifications.sms.backends.smsc.SmsBackend",  # Тут по желанию меняйте провайдера
    "OPTIONS": {
        "SMSC_LOGIN": "your_login",  # Login from https://smsc.ru
        "SMSC_PASSWORD": "your_password",  # Password
        "SMSC_DEBUG": False,  # Debug flag
        "SMSC_SENDER": False,  # Sender for message
    }
}
```

Всё, можно пользоваться.

```python
message = SMSMessage(phone_numbers=[phone], message=message_text)
message.send()
```

При необходимости заменить реального провайдера или использовать заглушки для стадии тестирования и дев окружения мы просто меняем используемый адаптер через `settings` Django или через `.env` файл.

Так же вы можете легко интегрировать в эту реализацию отправку sms с применением celery, но это уже выходит из контекста данного примера.

### Эпилог

Вы можете скачать этот пример из [репозитория](https://github.com/Sqvall/django-sms-message-example) и _пощупать_.

При запуске приложения, перейдите по `http://127.0.0.1:8000/` и вы увидите форму, где можете поэкспериментировать.

Можно зарегистрировать акк в [СМС-центр](https://smsc.ru/), они дают демо-счёт, которого хватит на отправку 3-4 смс.

**Имейте в виду, что на оператора мегафон сообщения не отправляются без зарегистрированного отправителя. 
Т.ж. правила связанные с именами отправителей могут измениться, для информации смотрите правила своего сервиса, например как [тут](https://smsc.ru/senders/edit/).**
