def test_import():
    """Test that modules can be imported directly."""
    import src.converter as converter
    import src.expander as expander
    import src.llmgentool as llmgentool

    assert converter is not None
    assert expander is not None
    assert llmgentool is not None
