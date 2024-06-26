def pytest_itemcollected(item):
    """
    Customize the node IDs for collected pytest items based on docstrings or class names.

    Args:
        item (pytest.Item): Pytest item representing a test function or method.

    Returns:
        None
    """
    try:
        # Retrieve the parent and node objects
        par = item.parent.obj if hasattr(item, 'parent') and item.parent else None
        node = item.obj if hasattr(item, 'obj') and item.obj else None
        
        # Determine the prefix and suffix for the node ID
        pref = par.__doc__.strip() if par and par.__doc__ else par.__class__.__name__ if par else None
        suf = node.__doc__.strip() if node and node.__doc__ else node.__name__ if node else None
        
        # Construct the node ID if either prefix or suffix is available
        if pref or suf:
            item._nodeid = ' '.join(filter(None, (pref, suf)))
    except Exception as e:
        print(f"Error customizing node ID for item: {e}")

