
from click.testing import CliRunner

from hts_synth.hts_synth import cli


class TestCliInterface:
    """Test suite for the hts-synth CLI interface."""

    def setup_method(self):
        """Set up the test runner."""
        self.runner: CliRunner = CliRunner() # pyright: ignore[reportUninitializedInstanceVariable]

    def test_cli_help_shows_available_options(self):
        """Test CLI help to understand available parameters."""
        result = self.runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "--help" in result.output

        # Print help output for debugging - this will help us see actual parameters
        print("\n" + "=" * 50)
        print("CLI HELP OUTPUT:")
        print("=" * 50)
        print(result.output)
        print("=" * 50)

    def test_cli_default_execution(self):
        """Test CLI with no parameters."""
        result = self.runner.invoke(cli)

        # Check if it runs without error or shows help
        assert result.exit_code in [0, 2]  # 0 for success, 2 for missing required args
        assert result.output  # Should produce some output

        if result.exit_code != 0:
            # If it failed, it should show usage information
            assert "Usage:" in result.output or "Error:" in result.output

    def test_cli_invalid_option(self):
        """Test CLI with an invalid option."""
        result = self.runner.invoke(cli, ["--invalid-option"])

        assert result.exit_code != 0
        assert (
            "no such option" in result.output.lower()
            or "unrecognized" in result.output.lower()
            or "invalid" in result.output.lower()
        )
