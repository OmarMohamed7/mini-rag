from stores.llm import LLMInterface
import logging

import cohere

from stores.llm.LLMEnums import COHEREEnums, DocumentTypesEnums


class CohereProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        default_input_max_chars: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        super().__init__()
        self.api_key = api_key
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.default_input_max_chars = default_input_max_chars

        self.default_generation_model_id = None
        self.default_embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=api_key)

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

        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
        )

        if not response or not response.text:
            self.logger.error("No response from generation model")
            raise ValueError("No response from generation model")

        return response.text

    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Client not initialized")
            raise ValueError("Client not initialized")

        if not self.embedding_model_id:
            self.logger.error("Embedding model not initialized")
            raise ValueError("Embedding model not initialized")

        input_type = COHEREEnums.DOCUMENT.value
        if document_type == DocumentTypesEnums.QUERY.value:
            input_type = COHEREEnums.QUERY.value

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("No response from embedding model")
            raise ValueError("No response from embedding model")

        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt),
        }
