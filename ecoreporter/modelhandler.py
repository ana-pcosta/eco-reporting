from typing import Literal
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain


class ModelHandler:
    def __init__(self, model_provider: Literal["openai"] = "openai"):
        self.model_provider = model_provider
        if self.model_provider == "openai":
            self.model = self._setup_openai_model()

    def generate_response(self, prompt):
        response = self.model.invoke(prompt)

        return response

    def _setup_openai_model(self):
        # define underlying LLM
        model = ChatOpenAI(model="gpt-4o-mini")
        return model
