from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image


processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")


def model_pipeline(text: str, image: Image):

    encoding = processor(image, text, return_tensors="pt")
    outputs = model(**encoding)
    logist_output = outputs.logits
    idx = logist_output.argmax(-1).item()

    return model.config.id2label[idx]
