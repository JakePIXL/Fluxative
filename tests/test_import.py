

def test_import():
    """Test that modules can be imported directly."""
    import converter
    import expander
    import llmgentool

    assert converter is not None
    assert expander is not None
    assert llmgentool is not None
