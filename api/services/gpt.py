import logging

from g4f.client import Client

from ..models.article import Article


def get_gpt_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    client = Client()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"language": "ru"},
        )
        if response.status_code != 200:
            logging.error(
                f"GPT request failed with status code: {response.status_code}"
            )
            return "Ошибка запроса к GPT. Попробуйте позже."

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "Ошибка запроса к GPT. Попробуйте позже."


def generate_summary(text: str) -> str:
    prompt = f"""
    Попробуй обобщить весь текст в 1-2 предложения:
    {text}
    """
    return get_gpt_response(prompt)


def generate_title(articles: list[Article]) -> str:
    articles_text = "".join(article.short_text for article in articles)
    prompt = f"""
    Составь заголовок сводки для этих новостей:
    {articles_text}
    Не длиннее 255 символов! Без нумерации, кавычек
    """
    return get_gpt_response(prompt)
