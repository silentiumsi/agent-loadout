def paginate(items, page, size):
    """Return one page of items. `page` is 1-indexed."""
    start = (page - 1) * size
    return items[start:start + size]
