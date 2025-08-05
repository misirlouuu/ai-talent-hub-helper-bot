# llm_client.py

import openai

class OpenRouterClient:
    def __init__(self, api_key, model="anthropic/claude-3-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    def generate_answer(self, question, context=""):
        openai.api_key = self.api_key
        openai.api_base = self.base_url

        system_prompt = (
            "Ты — цифровой помощник приёмной комиссии AI Talent Hub университета ИТМО. "
            "Твоя задача — помогать абитуриентам разобраться в двух магистратурных направлениях: "
            "«AI» (техническое) и «AI Product» (продуктовое). Отвечай на русском языке.\n\n"
            "Если пользователь задаёт вопрос, отвечай чётко и по существу, используя контекст с сайта или учебных планов. "
            "Если пользователь описывает свой бэкграунд — помоги выбрать подходящее направление и обоснуй выбор. "
            "При необходимости предложи 3–4 подходящих курса.\n\n"
            "Если информации недостаточно — честно скажи, что не можешь ответить точно. Пиши понятно, дружелюбно и без канцелярщины."
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{context}\n\nВопрос: {question}"}
                ],
                temperature=0.4,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Ошибка модели: {e}"
