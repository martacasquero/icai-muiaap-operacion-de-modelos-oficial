import json
from pathlib import Path

import pytest
from test_artifact import WINE_SAMPLE
from test_predict_file import write_bundle, write_input

from model_packaging.artifact import load_model_bundle
from model_packaging.predict_file import predict_file


def test_load_rejects_an_incompatible_preprocessing_version(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    write_bundle(bundle_path)
    manifest_path = bundle_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["preprocessing_version"] = "wine-red-features-v0"
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="preprocessing_version"):
        load_model_bundle(bundle_path)


def test_load_rejects_a_missing_model(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    write_bundle(bundle_path)
    (bundle_path / "model.joblib").unlink()

    with pytest.raises(FileNotFoundError):
        load_model_bundle(bundle_path)


def test_predict_file_rejects_an_out_of_range_value(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle"
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "predictions.csv"
    write_bundle(bundle_path)
    row = {
        "sample_id": "red-001",
        **{key: str(value) for key, value in WINE_SAMPLE.items()},
        "ph": "9.0",
    }
    write_input(input_path, rows=[row])

    with pytest.raises(ValueError, match="ph"):
        predict_file(input_path, output_path, bundle_path)

    assert not output_path.exists()
