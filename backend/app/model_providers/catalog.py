from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.model_providers.settings import model_provider_settings


class ModelProvider(BaseModel):
    name: str
    api_key: str


class Model(BaseModel):
    name: str
    provider: str
    display_name: str
    chef: str
    chef_slug: str
    supports_thinking: bool
    supports_thinking_effort: bool


ANTHROPIC_LEGACY_THINKING = {"type": "enabled", "budget_tokens": 1024}
ANTHROPIC_THINKING_BY_EFFORT: dict[str, dict[str, Any]] = {
    "low": {"type": "enabled", "budget_tokens": 512},
    "medium": {"type": "enabled", "budget_tokens": 1024},
    "high": {"type": "enabled", "budget_tokens": 4096},
}

GOOGLE_LEGACY_THINKING_BUDGET = -1
GOOGLE_THINKING_BUDGET_BY_EFFORT: dict[str, int] = {
    "low": 2048,
    "medium": 8192,
    "high": -1,
}


LLM_PROVIDERS: list[ModelProvider] = []
MODELS: list[Model] = []

if model_provider_settings.openai_api_key:
    LLM_PROVIDERS.append(ModelProvider(
        name="openai", api_key=model_provider_settings.openai_api_key))
    MODELS.append(Model(
        name="gpt-4o-mini",
        provider="openai",
        display_name="GPT-4o mini",
        chef="OpenAI",
        chef_slug="openai",
        supports_thinking=False,
        supports_thinking_effort=False,
    ))

if model_provider_settings.deepseek_api_key:
    LLM_PROVIDERS.append(ModelProvider(
        name="deepseek", api_key=model_provider_settings.deepseek_api_key))
    MODELS.append(Model(
        name="deepseek-v4-flash",
        provider="deepseek",
        display_name="DeepSeek v4 Flash",
        chef="DeepSeek",
        chef_slug="deepseek",
        supports_thinking=False,
        supports_thinking_effort=False,
    ))
    MODELS.append(Model(
        name="deepseek-v4-pro",
        provider="deepseek",
        display_name="DeepSeek v4 Pro",
        chef="DeepSeek",
        chef_slug="deepseek",
        supports_thinking=False,
        supports_thinking_effort=False,
    ))
    MODELS.append(Model(
        name="deepseek-chat",
        provider="deepseek",
        display_name="DeepSeek Chat",
        chef="DeepSeek",
        chef_slug="deepseek",
        supports_thinking=False,
        supports_thinking_effort=False,
    ))
    MODELS.append(Model(
        name="deepseek-reasoner",
        provider="deepseek",
        display_name="DeepSeek Reasoner",
        chef="DeepSeek",
        chef_slug="deepseek",
        supports_thinking=True,
        supports_thinking_effort=False,
    ))

if model_provider_settings.anthropic_api_key:
    LLM_PROVIDERS.append(ModelProvider(
        name="anthropic", api_key=model_provider_settings.anthropic_api_key))
    MODELS.append(Model(
        name="claude-haiku-4-5",
        provider="anthropic",
        display_name="Claude Haiku 4.5",
        chef="Anthropic",
        chef_slug="anthropic",
        supports_thinking=True,
        supports_thinking_effort=True,
    ))
    MODELS.append(Model(
        name="claude-sonnet-4-6",
        provider="anthropic",
        display_name="Claude Sonnet 4.6",
        chef="Anthropic",
        chef_slug="anthropic",
        supports_thinking=True,
        supports_thinking_effort=True,
    ))
    MODELS.append(Model(
        name="claude-opus-4-6",
        provider="anthropic",
        display_name="Claude Opus 4.6",
        chef="Anthropic",
        chef_slug="anthropic",
        supports_thinking=True,
        supports_thinking_effort=True,
    ))

if model_provider_settings.google_api_key:
    LLM_PROVIDERS.append(ModelProvider(
        name="google", api_key=model_provider_settings.google_api_key))
    MODELS.append(Model(
        name="gemini-3-flash-preview",
        provider="google",
        display_name="Gemini 3 Flash Preview",
        chef="Google",
        chef_slug="google",
        supports_thinking=True,
        supports_thinking_effort=True,
    ))
    MODELS.append(Model(
        name="gemini-3-pro-preview",
        provider="google",
        display_name="Gemini 3 Pro Preview",
        chef="Google",
        chef_slug="google",
        supports_thinking=True,
        supports_thinking_effort=True,
    ))


class ChatModelFactory:

    def create(self, provider: str, model_id: str, api_key: str, effort: str | None = None):
        match provider:
            case "openai":
                return ChatOpenAI(model=model_id, api_key=api_key)
            case "deepseek":
                return ChatDeepSeek(
                    model=model_id,
                    api_key=api_key,
                    extra_body=self._resolve_deepseek_thinking(effort),
                )
            case "anthropic":
                thinking = self._resolve_anthropic_thinking(effort)
                if thinking is None:
                    return ChatAnthropic(
                        model=model_id,
                        temperature=1,
                        max_tokens=2048,
                        streaming=True,
                        timeout=None,
                        max_retries=2,
                        api_key=api_key,
                    )
                return ChatAnthropic(
                    model=model_id,
                    temperature=1,
                    max_tokens=2048,
                    streaming=True,
                    timeout=None,
                    thinking=thinking,
                    max_retries=2,
                    api_key=api_key,
                )
            case "google":
                include_thoughts, thinking_budget = self._resolve_google_thinking(effort)
                return ChatGoogleGenerativeAI(
                    model=model_id,
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    streaming=True,
                    include_thoughts=include_thoughts,
                    thinking_budget=thinking_budget,
                    api_key=api_key,
                )
            case _:
                raise ValueError(f"Provider {provider} not supported")

    def _resolve_deepseek_thinking(self, effort: str | None) -> dict[str, dict[str, str]]:
        if effort in {"on", "low", "medium", "high"}:
            return {"thinking": {"type": "enabled"}}
        return {"thinking": {"type": "disabled"}}

    def _resolve_anthropic_thinking(self, effort: str | None) -> dict[str, Any] | None:
        if effort is None:
            return ANTHROPIC_LEGACY_THINKING
        if effort == "off":
            return None
        if effort == "on":
            return ANTHROPIC_THINKING_BY_EFFORT["medium"]
        return ANTHROPIC_THINKING_BY_EFFORT.get(effort, ANTHROPIC_THINKING_BY_EFFORT["medium"])

    def _resolve_google_thinking(self, effort: str | None) -> tuple[bool, int]:
        if effort is None:
            return True, GOOGLE_LEGACY_THINKING_BUDGET
        if effort == "off":
            return False, 0
        if effort == "on":
            return True, GOOGLE_THINKING_BUDGET_BY_EFFORT["medium"]
        return True, GOOGLE_THINKING_BUDGET_BY_EFFORT.get(effort, GOOGLE_THINKING_BUDGET_BY_EFFORT["medium"])
