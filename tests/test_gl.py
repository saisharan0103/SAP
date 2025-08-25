from erp import gl


def test_balanced_entry():
    gl.seed_chart_of_accounts()
    entry_id = gl.post_journal_entry(
        "2024-01-01",
        "Test entry",
        [
            {"account": "1000", "debit": 50},
            {"account": "2000", "credit": 50},
        ],
    )
    assert entry_id > 0
    tb = gl.trial_balance()
    assert tb["1000"] == 50
    assert tb["2000"] == -50
    assert sum(tb.values()) == 0


def test_unbalanced_raises():
    gl.seed_chart_of_accounts()
    try:
        gl.post_journal_entry(
            "2024-01-01",
            "Bad entry",
            [
                {"account": "1000", "debit": 10},
                {"account": "2000", "credit": 5},
            ],
        )
    except ValueError:
        pass
    else:
        assert False, "Should raise for unbalanced entry"
