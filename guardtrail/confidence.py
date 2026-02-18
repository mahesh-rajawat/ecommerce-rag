from logs.logger import get_logger
from config.settings import MIN_CONFIDENCE
from config.settings import MIN_SOURCES
from config.settings import DISTANCE_THRESHOLD

logger = get_logger("guardtrail.logs")

    
def return_with_confidence(answer, confidence, sources):
    logger.info(f"Answer confidence: {confidence}")

    if confidence < MIN_CONFIDENCE:
        return _reject("Low confidence")
    
    if sources < MIN_SOURCES:
        return _reject("Low document coverage")
    
    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }

def _reject(reason):
    logger.warning(f"Response rejected: {reason}")
    return {
        "answer": f"I could not find reliable information in the documents.",
        "confidence": 0,
        "sources": 0
    }