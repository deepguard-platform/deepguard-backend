def majority_voting(results: list[dict]) -> dict:
    total = len(results)
    fake_votes = sum(1 for r in results if r["score"] >= 0.5)
    real_votes = total - fake_votes
    if fake_votes > real_votes:
        label, votes = "fake", fake_votes
    elif real_votes > fake_votes:
        label, votes = "real", real_votes
    else:
        average = sum(r["score"] for r in results) / total
        label = "fake" if average >= 0.5 else "real"
        votes = fake_votes if label == "fake" else real_votes
    return {"label": label, "confidence": round(votes / total, 4)}


def weighted_averaging(results: list[dict]) -> dict:
    total_weight = sum(r["weight"] for r in results)
    fake_probability = sum(r["score"] * r["weight"] for r in results) / total_weight
    label = "fake" if fake_probability >= 0.5 else "real"
    confidence = fake_probability if label == "fake" else 1 - fake_probability
    return {
        "label": label,
        "confidence": round(confidence, 4),
        "fake_probability": round(fake_probability, 4),
    }


def run_ensemble(results: list[dict]) -> dict:
    if not results:
        raise ValueError("No model results to combine")
    strategies = {
        "majority_voting": majority_voting(results),
        "weighted_averaging": weighted_averaging(results),
    }
    final = strategies["weighted_averaging"]
    return {
        "verdict": final["label"],
        "confidence": final["confidence"],
        "default_strategy": "weighted_averaging",
        "strategies": strategies,
    }
