from g4f.client import Client

from ..models.article import Article


def query_gpt(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    client = Client()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generate_summary(text: str) -> str:
    prompt = f"""
    Попробуй обобщить весь текст в 1-2 предложения:
    {text}
    """
    return query_gpt(prompt)


def generate_title(articles: list[Article]) -> str:
    articles_text = "".join(article.short_text for article in articles)
    prompt = f"""
    Составь заголовок сводки для этих новостей:
    {articles_text}
    Не длиннее 255 символов! Без нумерации, кавычек
    """
    return query_gpt(prompt)
