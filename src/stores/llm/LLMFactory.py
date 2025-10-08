from stores.llm import LLMEnums
from stores.llm.providers import CohereProvider, OpenAIProvider


class LLMFactory:
    def __init__(self, config: dict):
        self.config = config

    def get_llm(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_chars=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE,
            )
        elif provider == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_chars=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE,
            )

        raise ValueError(f"Invalid provider: {provider}")
