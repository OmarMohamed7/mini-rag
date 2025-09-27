from stores.llm import LLMInterface
from openai import OpenAI
import logging

from stores.llm.LLMEnums import OPENAIEnums


class OpenAIProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        api_url: str = None,
        default_input_max_chars: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        super().__init__()
        self.api_key = api_key
        self.api_url = api_url
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.default_input_max_chars = default_input_max_chars

        self.default_generation_model_id = None
        self.default_embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key=api_key, api_url=api_url)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[: self.default_input_max_chars].strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list,
        max_output_tokens: int,
        temperature: float,
    ):
        if not self.client:
            self.logger.error("Client not initialized")
            raise ValueError("Client not initialized")

        if not self.generation_model_id:
            self.logger.error("Generation model not initialized")
            raise ValueError("Generation model not initialized")

        max_output_tokens = (
            max_output_tokens or self.default_generation_max_output_tokens
        )

        temperature = temperature or self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OPENAIEnums.USER.value)
        )

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature,
        )

        if (
            not response
            or not response.choices
            or len(response.choices) == 0
            or not response.choices[0].message.content
        ):
            self.logger.error("No response from generation model")
            raise ValueError("No response from generation model")

        if (
            not response
            or not response.choices
            or len(response.choices) == 0
            or not response.choices[0].message.content
        ):
            self.logger.error("No response from generation model")
            raise ValueError("No response from generation model")

        return response.choices[0].message.content

    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Client not initialized")
            raise ValueError("Client not initialized")

        response = self.client.embeddings.create(
            input=text, model=self.embedding_model_id
        )
        if (
            not response
            or not response.data
            or len(response.data) == 0
            or not response.data[0].embedding
        ):
            self.logger.error("No response from embedding model")
            raise ValueError("No response from embedding model")

        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: OPENAIEnums):
        return {
            "role": role.value,
            "content": self.process_text(prompt),
        }
