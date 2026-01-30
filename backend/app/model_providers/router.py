import os
from fastapi import APIRouter
from .settings import model_provider_settings
from app.model_providers.models import ModelProviderRead, ModelProviderType, ModelRead

router = APIRouter(prefix="/model-providers", tags=["model-providers"])

@router.get("/", response_model=list[ModelProviderRead])
async def get_model_providers() -> list[ModelProviderRead]:
    """List all model providers."""
    model_providers = []
    if model_provider_settings.openai_api_key:
        model_providers.append(ModelProviderRead(name=ModelProviderType.openai))
    if model_provider_settings.deepseek_api_key:
        model_providers.append(ModelProviderRead(name=ModelProviderType.deepseek))
    if model_provider_settings.anthropic_api_key:
        model_providers.append(ModelProviderRead(name=ModelProviderType.anthropic))
    if model_provider_settings.google_api_key:
        model_providers.append(ModelProviderRead(name=ModelProviderType.google))
    
    return list(model_providers)


@router.get("/models", response_model=list[ModelRead])
async def get_models() -> list[ModelRead]:
    """List all models available."""
    models = []
    if model_provider_settings.openai_api_key:
        models.extend([ModelRead(name="gpt-4o-mini", providers=[ModelProviderType.openai], id="gpt-4o-mini", chef="OpenAI", chefSlug="openai")])
    if model_provider_settings.deepseek_api_key:
        models.extend([
            ModelRead(name="deepseek-chat", providers=[ModelProviderType.deepseek], id="deepseek-chat", chef="DeepSeek", chefSlug="deepseek"),
            ModelRead(name="deepseek-reasoner", providers=[ModelProviderType.deepseek], id="deepseek-reasoner", chef="DeepSeek", chefSlug="deepseek"),
        ])
    if model_provider_settings.anthropic_api_key:
        models.extend([
            ModelRead(name="claude-haiku-4-5", providers=[ModelProviderType.anthropic], id="claude-haiku-4-5", chef="Anthropic", chefSlug="anthropic"),
            ModelRead(name="claude-sonnet-4-5", providers=[ModelProviderType.anthropic], id="claude-sonnet-4-5", chef="Anthropic", chefSlug="anthropic"),
            ModelRead(name="claude-opus-4-5", providers=[ModelProviderType.anthropic], id="claude-opus-4-5", chef="Anthropic", chefSlug="anthropic"),
        ])
    if model_provider_settings.google_api_key:
        models.extend([
            ModelRead(name="gemini-3-flash-preview", providers=[ModelProviderType.google], id="gemini-3-flash-preview", chef="Google", chefSlug="google"),
            ModelRead(name="gemini-3-pro-preview", providers=[ModelProviderType.google], id="gemini-3-pro-preview", chef="Google", chefSlug="google"),
        ])
        
    return list(models)