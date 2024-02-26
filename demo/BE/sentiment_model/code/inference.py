import json
import logging
import os

import numpy as np
import torch
from constants import constants
from sagemaker_inference import encoder
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import TextClassificationPipeline


def model_fn(model_dir: str) -> TextClassificationPipeline:
    """Create our inference task as a delegate to the model.

    Args:
        model_dir (str): model directory location for the model to load

    Returns:
        TextClassificationPipeline for the inference

    This runs only once per one worker
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        device_id = 0 if torch.cuda.is_available() else -1
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        return TextClassificationPipeline(model=model, tokenizer=tokenizer, device=device_id, return_all_scores=True)
    except Exception:
        logging.error(f"Failed to load model from: {model_dir}")
        raise


def infer_sentence(tc_pipeline: TextClassificationPipeline, sentence: str, accept: str, is_batch: bool) -> dict:
    """Make predictions against the model and returns a dictionary.

    Args:
        tc_pipeline: A pipeline for inference loaded into memory
        sentence (str): the input sentence.
        accept (str): accept header expected by the client.
        is_batch(bool): whether the inference is for batch

    Returns:
        dict: the output dictionary of inference

    """
    # We are passing the sentence to the pipeline and getting predictions from it of the form
    # [[{'label': 'LABEL_0', 'score': 7.95125961303711e-05},{'label': 'LABEL_1', 'score': 0.9999204874038696}]]

    predictions = tc_pipeline(sentence)[0]
    output = {}
    if is_batch:
        output["sentence"] = sentence
    output[constants.PROBABILITIES] = [x["score"] for x in predictions]
    if accept.endswith(constants.VERBOSE_EXTENSION):
        labels = [x["label"] for x in predictions]
        output[constants.LABELS] = labels
        predicted_label_idx = np.argmax(output[constants.PROBABILITIES])
        output[constants.PREDICTED_LABEL] = output[constants.LABELS][predicted_label_idx]
        # The output over here will be of form
        # {'probabilities': [7.95125961303711e-05, 0.9999204874038696],'labels': ['LABEL_0', 'LABEL_1'],
        # 'predicted_label': 'LABEL_1'}
    return output


def transform_fn(tc_pipeline: TextClassificationPipeline, input_data: object, content_type: str, accept: str) -> object:
    """Make predictions against the model and return a serialized response.

    The function signature conforms to the SM contract

    Args:
        tc_pipeline: A pipeline for inference loaded into memory
        input_data (obj): the request data.
        content_type (str): the request content type.
        accept (str): accept header expected by the client.

    Returns:
        obj: the serialized prediction result or a tuple of the form
            (response_data, content_type)

    """
    if content_type == constants.REQUEST_CONTENT_TYPE:
        sentence = input_data.decode(constants.STR_DECODE_CODE)
        try:
            output = infer_sentence(tc_pipeline, sentence, accept, False)
            accept = accept.replace(constants.VERBOSE_EXTENSION, "")
            return encoder.encode(output, accept)
        except Exception:
            logging.exception("Failed to do inference")
            raise

    elif content_type == constants.BATCH_REQUEST_CONTENT_TYPE:
        sentences = input_data.split("\n")
        try:
            # We are passing the sentence to the pipeline and getting predictions from it of the form
            # [[{'label': 'LABEL_0', 'score': 7.95125961303711e-05},{'label': 'LABEL_1', 'score': 0.9999204874038696}]]
            output_arr = []
            for sentence in sentences:
                output = infer_sentence(tc_pipeline, sentence, accept, True)
                output_arr.append(output)
            accept = accept.replace(constants.VERBOSE_EXTENSION, "")
            return encoder.encode(output_arr, accept)
        except Exception:
            logging.exception("Failed to do inference")
            raise

    raise ValueError('{{"error": "unsupported content type {}"}}'.format(content_type or "unknown"))
