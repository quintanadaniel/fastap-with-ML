import io
import logging
import os

from PIL import Image
from ddtrace import tracer

from model import model_pipeline
from fastapi import FastAPI, UploadFile
from utils.datadog_client import DatadogClient


client_datadog = DatadogClient()
client_datadog.client_initialize()

app = FastAPI()


logging.basicConfig(
    filename=os.path.join(os.getcwd(), "logs", "logfile.log"),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    logger.info("reading endpoint read_root")
    client_datadog.send_metrics_incremental("image_detector_read_root.increment")
    return {"hello": "world"}


@app.post("/ask")
def ask(text: str, image: UploadFile):
    logger.info(f"Received request with text: {text}")
    with tracer.trace("ask.endpoint", service="image-detector", resource="ask") as span:
        span.set_tag("request.text", text)
        try:
            content = image.file.read()
            with tracer.trace("ask.image_processing", service="image-detector"):
                image = Image.open(io.BytesIO(content))
            with tracer.trace("ask.model_inference", service="image-detector"):
                result = model_pipeline(text, image)
            client_datadog.send_metrics_incremental("image-detector.ask_endpoint.calls")
            return {"answer": result}

        except Exception as err:
            logger.error(f"error {err} in endpoint ask")
            span.set_tag("error", True)
            span.set_tag("error.message", str(err))
            raise
