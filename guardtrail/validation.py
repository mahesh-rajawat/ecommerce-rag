from logger.logger import get_logger
from config.settings import MIN_CONFIDENCE
from config.settings import MIN_SOURCES
from config.settings import DISTANCE_THRESHOLD

logger = get_logger("guardtrail.logs")

def validate_distance_index(D, I):
    if I is None or len(I) == 0 or I[0][0] == -1:
        return False
    return True

def validate_retirived_docs(distances, indexes:list, documents:list, company, domain):
    if indexes is None or len(indexes) == 0 or indexes[0][0] == -1:
        return False
    
    safe_docs = []
    safe_indexes = []
    safe_dis = []
    
    for dis, idx in zip(distances[0], indexes[0]):
        if idx < 0 or idx >= len(documents):
            continue
        
        doc = documents[idx]

        if doc.get("company") == company and doc.get("document") == domain:
            safe_docs.append(doc)
            safe_indexes.append(idx)
            safe_dis.append(dis)
        else:
            logger.info(f"SECURITY ALERT: Unauthorized data access attempt for {company}")
    
    return safe_dis, safe_indexes, safe_docs
    
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