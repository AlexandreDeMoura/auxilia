from fastapi import APIRouter

from app.model_providers.catalog import MODELS
from app.model_providers.models import ModelProviderType
from app.model_providers.schemas import ModelProviderResponse, ModelResponse

from .settings import model_provider_settings


router = APIRouter(prefix="/model-providers", tags=["model-providers"])


@router.get("/", response_model=list[ModelProviderResponse])
async def get_model_providers() -> list[ModelProviderResponse]:
    """List all model providers."""
    model_providers = []
    if model_provider_settings.openai_api_key:
        model_providers.append(ModelProviderResponse(
            name=ModelProviderType.openai))
    if model_provider_settings.deepseek_api_key:
        model_providers.append(ModelProviderResponse(
            name=ModelProviderType.deepseek))
    if model_provider_settings.anthropic_api_key:
        model_providers.append(ModelProviderResponse(
            name=ModelProviderType.anthropic))
    if model_provider_settings.google_api_key:
        model_providers.append(ModelProviderResponse(
            name=ModelProviderType.google))

    return list(model_providers)


@router.get("/models", response_model=list[ModelResponse])
async def get_models() -> list[ModelResponse]:
    """List all models available."""
    return [
        ModelResponse(
            id=model.name,
            name=model.display_name,
            chef=model.chef,
            chefSlug=model.chef_slug,
            providers=[ModelProviderType(model.provider)],
            supports_thinking=model.supports_thinking,
            supports_thinking_effort=model.supports_thinking_effort,
        )
        for model in MODELS
    ]
