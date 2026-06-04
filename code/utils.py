import logging
import pathlib

import aind_session
import codeocean.data_asset
import pydantic
import pydantic_settings
import requests

logger = logging.getLogger(__name__)

class ComputationParams(pydantic_settings.BaseSettings):
    """Parameters passed to this capsule by Code Ocean's post-run hook or from the app-panel."""
    co_source_computation_id: pydantic.UUID4
    co_source_exit_code: int = 0

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[pydantic_settings.BaseSettings],
        init_settings: pydantic_settings.PydanticBaseSettingsSource,
        env_settings: pydantic_settings.PydanticBaseSettingsSource,
        dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
        file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            pydantic_settings.CliSettingsSource(settings_cls, cli_parse_args=True),
            init_settings,
            dotenv_settings,
            file_secret_settings,
        )

def get_data_asset_params_model(computation_id: pydantic.UUID4) -> codeocean.data_asset.DataAssetParams:
    co_client = aind_session.get_codeocean_client()
    for file in (
        item
        for item in co_client.computations.list_computation_results(computation_id=computation_id).items
        if item.path.lower().endswith(".json") and item.type != "folder"
    ):
        try:
            params = codeocean.data_asset.DataAssetParams.from_json(
                requests.get(
                    co_client
                    .computations.get_result_file_download_url(computation_id=computation_id, path=file.path)
                    .url
                ).text
            )
        except pydantic.ValidationError as e:
            logger.warning("Validation error while attempting to parse DataAssetParams from %s: %s", file.path, e)
        else:
            logger.info("Successfully parsed DataAssetParams from %s", file.path)
            source = codeocean.data_asset.Source(computation=codeocean.data_asset.ComputationSource(id=computation_id))
            params = codeocean.data_asset.DataAssetParams(**params.to_dict() | {"source": source})
            logger.info("Updated `source` in DataAssetParams to point to computation")
            return params
    raise FileNotFoundError(f"No valid DataAssetParams JSON file found among computation results for computation {computation_id}")
        
def create_data_asset(data_asset_params: codeocean.data_asset.DataAssetParams, wait_until_ready: bool = True) -> codeocean.data_asset.DataAsset:
    co_client = aind_session.get_codeocean_client()
    created_asset = co_client.data_assets.create_data_asset(data_asset_params=data_asset_params)
    logger.info("Created new data asset with ID %s", created_asset.id)
    if wait_until_ready:
        logger.info("Waiting for data asset %s to be ready...", created_asset.id)
        co_client.data_assets.wait_until_ready(created_asset.id, timeout=None)
        logger.info("Data asset is ready")
    return created_asset