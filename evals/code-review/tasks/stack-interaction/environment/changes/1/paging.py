def page_offset(page, size):
    return (page - 1) * size

def page_items(items, page, size):
    offset = page_offset(page, size)
    return items[offset:offset + size]
