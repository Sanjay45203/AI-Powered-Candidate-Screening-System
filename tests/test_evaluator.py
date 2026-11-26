from src.recruitment.evaluator import evaluate_candidate

def test_evaluator_output():
    result = evaluate_candidate("Python SQL data analysis", "Python SQL analyst")
    assert 0 <= result["score"] <= 100
    assert "matched_terms" in result and "review_note" in result
