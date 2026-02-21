from logger.logger import get_logger
from config.settings import MIN_CONFIDENCE
from config.settings import MIN_SOURCES
from config.settings import DISTANCE_THRESHOLD

logger = get_logger("guardtrail.logs")

def validate_distance_index(D, I):
    if I is None or len(I) == 0 or I[0][0] == -1:
        return False
    return True
    
def return_with_confidence(response: dict, confidence):
    logger.info(f"Answer confidence: {confidence}")

    if confidence < MIN_CONFIDENCE:
        return _reject("Low confidence")
    
    if response.get("sources", 0) < MIN_SOURCES:
        return _reject("Low document coverage")
    
    response["confidence"] = confidence
    return response

def _reject(reason):
    logger.warning(f"Response rejected: {reason}")
    return {
        "answer": f"I could not find reliable information in the documents.",
        "confidence": 0,
        "sources": 0
    }