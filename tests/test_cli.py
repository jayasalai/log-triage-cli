from logtriage.cli import run

def test_cli_runs_on_sample(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("2026-06-05 09:14:02 INFO server started\n")
    exit_code = run([str(log)])
    assert exit_code == 0

def test_cli_returns_1_on_errors(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("2026-06-05 09:16:45 ERROR database failed\n")
    exit_code = run([str(log)])
    assert exit_code == 1