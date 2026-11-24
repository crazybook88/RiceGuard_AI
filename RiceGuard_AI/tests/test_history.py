from utils import history_manager as hm

RESULT = {"predicted_class": "Brown Spot", "confidence": 0.9, "is_low_confidence": False, "is_mock": True}


def test_missing_file_returns_empty(tmp_path):
    assert hm.read_history(tmp_path / "x.csv").empty


def test_append_and_clear(tmp_path):
    p = tmp_path / "h.csv"
    hm.append_record("a.jpg", RESULT, p)
    hm.append_record("b.jpg", RESULT, p)
    assert len(hm.read_history(p)) == 2
    hm.clear_history(p)
    assert hm.read_history(p).empty

# TODO (Member 6): corrupted-CSV and wrong-schema cases.
