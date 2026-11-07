import pytest

from app.services.ensemble import majority_voting, run_ensemble, weighted_averaging


def result(name, score, weight=1.0):
    return {"model_name": name, "score": score, "weight": weight}


def test_majority_voting_fake():
    out = majority_voting([result("a", 0.9), result("b", 0.8), result("c", 0.1)])
    assert out["label"] == "fake"
    assert out["confidence"] == pytest.approx(0.6667, abs=1e-3)


def test_weighted_averaging_uses_weights():
    out = weighted_averaging([result("a", 0.9, 0.8), result("b", 0.1, 0.2)])
    assert out["label"] == "fake"
    assert out["confidence"] == pytest.approx(0.74, abs=1e-3)


def test_run_ensemble_returns_both_strategies():
    out = run_ensemble([result("a", 0.2), result("b", 0.3)])
    assert out["verdict"] == "real"
    assert set(out["strategies"]) == {"majority_voting", "weighted_averaging"}


def test_run_ensemble_empty_raises():
    with pytest.raises(ValueError):
        run_ensemble([])
