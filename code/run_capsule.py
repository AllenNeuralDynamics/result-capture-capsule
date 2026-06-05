import logging

import utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, force=True)

def main():
    computation_params = utils.ComputationParams()
    if computation_params.co_source_exit_code != 0:
        logger.warning(f"Source computation {computation_params.co_source_computation_id} exited with exit code {computation_params.co_source_exit_code}.")
    data_asset_params = utils.get_data_asset_params_model(computation_params.co_source_computation_id)
    utils.create_data_asset(data_asset_params)

if __name__ == "__main__": 
    main()