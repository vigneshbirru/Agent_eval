
import os
import time
from pydantic import BaseModel
from groq import Groq, AsyncGroq
from deepeval.models import DeepEvalBaseLLM
import asyncio
import random
import re
from groq import APIStatusError

class GroqModel(DeepEvalBaseLLM):
    max_retries = 4

    def __init__(self, model_name="qwen/qwen3.8-27b"):
        self.model_name = model_name
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"], max_retries=0)
        self.async_client = AsyncGroq(
            api_key=os.environ["GROQ_API_KEY"],
            max_retries=0,
        )

    def load_model(self):
        return self.client

    def get_model_name(self):
        return self.model_name

    @staticmethod
    def clean_json_output(output: str) -> str:
        output = output.strip()
        output = re.sub(r"^```(?:json)?\s*", "", output, flags=re.IGNORECASE)
        output = re.sub(r"\s*```$", "", output)

        start = output.find("{")
        end = output.rfind("}")
        if start >= 0 and end > start:
            output = output[start : end + 1]

        return output.strip()

    @staticmethod
    def _retry_delay(exc: APIStatusError, attempt: int) -> float:
        retry_after = exc.response.headers.get("retry-after")
        if retry_after is not None:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                pass
        return 2**attempt + random.random()

    def generate(
        self,
        prompt: str,
        schema: type[BaseModel] | None = None,
    ):
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                break
            except APIStatusError as exc:
                if exc.status_code != 429 or attempt == self.max_retries:
                    raise
                time.sleep(self._retry_delay(exc, attempt))

        output = response.choices[0].message.content or ""

        if schema is not None:
            return schema.model_validate_json(self.clean_json_output(output))

        return output

    async def a_generate(
        self,
        prompt: str,
        schema: type[BaseModel] | None = None,
    ):
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.async_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                break
            except APIStatusError as exc:
                if exc.status_code != 429 or attempt == self.max_retries:
                    raise
                await asyncio.sleep(self._retry_delay(exc, attempt))

        output = response.choices[0].message.content or ""

        if schema is not None:
            return schema.model_validate_json(self.clean_json_output(output))

        return output
