# result-capture-capsule

- Runs as an "automation capsule" after some other Code Ocean capsule.
- Converts a completed computation result into a data asset.
- Skips processing when `co_source_exit_code` is non-zero.
- Scans the root of the computation/results dir for the first `.json` file with a valid `DataAssetParams` model.
- Template JSON files are included with this capsule to define the data asset parameters.
- Rewrites the data asset `source` to the source computation ID.
- Creates the data asset and waits until it is ready.
- Also accepts `co_source_computation_id` from the app panel in case conversion failed previously.
