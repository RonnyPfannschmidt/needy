"""Test version handling."""

import needy


def test_version_is_string() -> None:
    """Test that __version__ is a string."""
    assert isinstance(needy.__version__, str)
    assert len(needy.__version__) > 0


def test_version_not_unknown() -> None:
    """Test that __version__ is not the fallback value."""
    assert needy.__version__ != "0.0+unknwon.error"
