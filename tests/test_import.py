def test_import():
    """Test that modules can be imported directly."""
    import src.converter as converter
    import src.expander as expander
    import src.fluxative as fluxative

    assert converter is not None
    assert expander is not None
    assert fluxative is not None
