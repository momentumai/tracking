def get_results(visitor_future, cat_future, content_future):

    visitor = visitor_future.get_result()
    cat_future.get_result()

    if content_future:
        content_future.get_result()

    return visitor