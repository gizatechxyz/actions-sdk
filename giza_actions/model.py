from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import onnxruntime as ort
from giza import API_HOST
from giza.client import ApiClient, ModelsClient, VersionsClient
from giza.utils.enums import VersionStatus


class GizaModel:
    def __init__(
        self,
        model_path: Optional[str] = None,
        id: Optional[int] = None,
        version: Optional[int] = None,
        output_path: Optional[str] = None,
    ):
        if model_path is None and id is None and version is None:
            raise ValueError("Either model_path or id and version must be provided.")

        if model_path is None and (id is None or version is None):
            raise ValueError("Both id and version must be provided.")

        if model_path and (id or version):
            raise ValueError("Either model_path or id and version must be provided.")

        if model_path:
            self.session = ort.InferenceSession(model_path)
        elif id and version:
            self.model_client = ModelsClient(API_HOST)
            self.version_client = VersionsClient(API_HOST)
            self.api_client = ApiClient(API_HOST)
            self._get_credentials()
            self._download_model(id, version, output_path)
            self.session = None

    def _download_model(self, model_id: int, version_id: int, output_path: str):
        version = self.version_client.get(model_id, version_id)

        if version.status != VersionStatus.COMPLETED:
            raise ValueError(f"Model version status is not completed {version.status}")

        print("ONNX model is ready, downloading! ✅")
        onnx_model = self.api_client.download_original(model_id, version.version)

        model_name = version.original_model_path.split("/")[-1]
        save_path = Path(output_path) / model_name

        with open(save_path, "wb") as f:
            f.write(onnx_model)

        print(f"ONNX model saved at: {save_path}")
        self.session = ort.InferenceSession(save_path)
        print("Model ready for inference with ONNX Runtime! ✅")

    def _get_credentials(self):
        self.api_client.retrieve_token()
        self.api_client.retrieve_api_key()

    def predict(self, inputs, verifiable: bool = False):
        if verifiable:
            # Generate Cairo inputs file
            # inputs_gen(inputs)
            # convert(input_file='data.csv', output_file='data.cairo', input_format='csv', output_format='cairo')
            # Run CairoVM inference
            # preds = self.session.run(None, inputs)[0]
            raise NotImplementedError("Verifiable inference is not yet implemented.")
        else:
            if self.session is None:
                raise ValueError("Session is not initialized.")
            preds = self.session.run(None, inputs)[0]
        return preds


def model(func: Callable, id: int, version: int):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
