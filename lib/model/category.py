from lib.model.db.category import Category


def get_or_insert_async(category_map):
    return Category.get_or_insert_async(category_map)
