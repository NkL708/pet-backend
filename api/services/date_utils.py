from datetime import date, datetime, timedelta

import pytz

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
SERVER_TIMEZONE_NAME = "Asia/Novosibirsk"
SERVER_TIMEZONE = pytz.timezone(SERVER_TIMEZONE_NAME)


def get_current_datetime(timezone: str = SERVER_TIMEZONE_NAME) -> datetime:
    return datetime.now(pytz.timezone(timezone))


def get_yesterday_date(current_datetime: datetime) -> date:
    return (current_datetime - timedelta(days=1)).date()


def published_on_specific_date(published_date: str, target_date: date) -> bool:
    article_datetime = datetime.strptime(published_date, DATE_FORMAT)
    article_datetime = article_datetime.astimezone(
        pytz.timezone(SERVER_TIMEZONE_NAME)
    )
    article_date = article_datetime.date()

    return article_date == target_date
