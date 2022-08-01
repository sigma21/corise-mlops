from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from model import NewsCategoryClassifier


GLOBAL_CONFIG = {
    "model": {
        "featurizer": {
            "sentence_transformer_model": "all-mpnet-base-v2",
            "sentence_transformer_embedding_dim": 768
        },
        "classifier": {
            "serialized_model_path": "../data/news_classifier.joblib"
        }
    },
    "service": {
        "log_destination": "../data/logs.out"
    }
}

class PredictRequest(BaseModel):
    source: str
    url: str
    title: str
    description: str


class PredictResponse(BaseModel):
    scores: dict
    label: str


app = FastAPI()
classifier = NewsCategoryClassifier(GLOBAL_CONFIG)


@app.on_event("startup")
def startup_event():
    """
        [TO BE IMPLEMENTED]
        1. Initialize the `NewsCategoryClassifier` instance to make predictions online. You should pass any relevant config parameters from `GLOBAL_CONFIG` that are needed by NewsCategoryClassifier 
        2. Open an output file to write logs, at the destination specified by GLOBAL_CONFIG['service']['log_destination']
        
        Access to the model instance and log file will be needed in /predict endpoint, make sure you
        store them as global variables
    """
    classifier = NewsCategoryClassifier(GLOBAL_CONFIG)
    # TODO! log file
    logger.info("Setup completed")


@app.on_event("shutdown")
def shutdown_event():
    # clean up
    """
        [TO BE IMPLEMENTED]
        1. Make sure to flush the log file and close any file pointers to avoid corruption
        2. Any other cleanups
    """
    logger.info("Shutting down application")


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # get model prediction for the input request
    # construct the data to be logged
    # construct response
    """
        [TO BE IMPLEMENTED]
        1. run model inference and get model predictions for model inputs specified in `request`
        2. Log the following data to the log file (the data should be logged to the file that was opened in `startup_event`, and writes to the path defined in GLOBAL_CONFIG['service']['log_destination'])
        {
            'timestamp': <YYYY:MM:DD HH:MM:SS> format, when the request was received,
            'request': dictionary representation of the input request,
            'prediction': dictionary representation of the response,
            'latency': time it took to serve the request, in millisec
        }
        3. Construct an instance of `PredictResponse` and return
    """
    pred = classifier.predict_label(request.description)[0]
    pred_proba = classifier.predict_proba(request.description)[0]

    class_names = classifier.pipeline.classes_
    scores = dict(zip(class_names, pred_proba))

    response_model = {
        "scores": dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)),
        "label": pred
    }

    return response_model


@app.get("/")
def read_root():
    return {"Hello": "World"}
