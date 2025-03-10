def test_import():
    """Simple test to ensure modules can be imported."""
    try:
        import converter
        import expander
        import llmgentool
        assert True
    except ImportError:
        assert False, "Failed to import core modules"