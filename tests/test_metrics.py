from src.recruitment.metrics import calculate_time_savings

def test_99_5_percent_example():
    assert calculate_time_savings(1000, 5)["time_reduction_percent"] == 99.5
