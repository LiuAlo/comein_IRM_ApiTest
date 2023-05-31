def my_assert(condition, content=None):
    try:
        assert condition
    except AssertionError as e:
        if content is None:
            print(e)
        else:
            print(content)
