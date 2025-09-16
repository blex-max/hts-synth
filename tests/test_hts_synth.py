import random

from click.testing import CliRunner

from hts_synth.hts_synth import cli


def test_hello_world(monkeypatch):
    random.seed(42)

    runner = CliRunner()
    result = runner.invoke(cli, ["--length=20"])
    assert result.exit_code == 0
    assert result.output == "GACAGGTACAAGAAGGAGTA\nPKriXrefSFPLBYtCRGSE\n"
