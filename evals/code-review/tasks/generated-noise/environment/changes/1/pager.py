def paginate(items, page, size):
    """Return one page of items. `page` is 1-indexed."""
    start = page * size
    return items[start:start + size]
