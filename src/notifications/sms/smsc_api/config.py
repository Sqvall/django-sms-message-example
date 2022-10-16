from dataclasses import dataclass


@dataclass
class SmscConfig:
    # Константы для настройки библиотеки
    SMSC_LOGIN: str  # логин клиента
    SMSC_PASSWORD: str  # пароль
    SMSC_POST: bool = False  # использовать метод POST
    SMSC_HTTPS: bool = False  # использовать HTTPS протокол
    SMSC_DEBUG: bool = False  # флаг отладки
    SMSC_CHARSET: str = "utf-8"  # кодировка сообщения (windows-1251 или koi8-r), по умолчанию используется utf-8
    # отправитель для оператора, если указано `False`, то отправка будет от стандартного отправителя SMSC сервиса,
    # не все операторы сотовой связи это допускают и сообщение может быть отклонено.
    SMSC_SENDER: str = False

    # Константы для отправки SMS по SMTP
    SMTP_FROM: str = "api@smsc.ru"  # e-mail адрес отправителя
    SMTP_SERVER: str = "send.smsc.ru"  # адрес smtp сервера
    SMTP_LOGIN: str = ""  # логин для smtp сервера
    SMTP_PASSWORD: str = ""  # пароль для smtp сервера
