# Janscas 2014
# Code to generate pagineted results on a query
# Can only perform equality filters
# Returns the cursor.urlsafe of the Previous and Next buttons on your page.
# -------------------------------------------------------------------------


def return_query_page(cls, size=10, bookmark=None, is_prev=None, equality_filters=None, orders=None):
    """
    Generate a paginated result on any class
    Param cls: The ndb model class to query
    Param size: The size of the results
    Param bokkmark: The urlsafe cursor of the previous queris. First time will be None
    Param is_prev: If your requesting for a next result or the previous ones
    Param equal_filters: a dictionary of {'property': value} to apply equality filters only
    Param orders: a dictionary of {'property': '-' or ''} to order the results like .order(cls.property)
    Return: a tuple (list of results, Previous cursor bookmark, Next cursor bookmark)
    """
    if bookmark:
        cursor = ndb.Cursor(urlsafe=bookmark)
    else:
        is_prev = None
        cursor = None

    q = cls.query()
    try:
        for prop, value in equality_filters.iteritems():
            q = q.filter(cls._properties[prop] == value)

        q_forward = q.filter()
        q_reverse = q.filter()

        for prop, value in orders.iteritems():
            if value == '-':
                q_forward = q_forward.order(-cls._properties[prop])
                q_reverse = q_reverse.order(cls._properties[prop])
            else:
                q_forward = q_forward.order(cls._properties[prop])
                q_reverse = q_reverse.order(-cls._properties[prop])
    except:
        return None
    if is_prev:
        qry = q_reverse
        new_cursor = cursor.reversed() if cursor else None
    else:
        qry = q_forward
        new_cursor = cursor if cursor else None

    results, new_cursor, more = qry.fetch_page(size, start_cursor=new_cursor)
    if more and new_cursor:
        more = True
    else:
        more = False

    if is_prev:
        prev_bookmark = new_cursor.reversed().urlsafe() if more else None
        next_bookmark = bookmark
        results.reverse()
    else:
        prev_bookmark = bookmark
        next_bookmark = new_cursor.urlsafe() if more else None

    return results, prev_bookmark, next_bookmark