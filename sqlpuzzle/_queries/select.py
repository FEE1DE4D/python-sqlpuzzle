# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sqlpuzzle._queryparts import Columns, TablesForSelect, Where, GroupBy, Having, OrderBy, Limit, IntoOutfile
from .query import Query
from .union import Union, UNION, UNION_ALL
from .selectoptions import SelectOptions, SelectForUpdate

__all__ = ('Select',)


class Select(Query):
    _queryparts = {
        'select_options': SelectOptions,
        'columns': Columns,
        'tables': TablesForSelect,
        'where': Where,
        'group_by': GroupBy,
        'having': Having,
        'order_by': OrderBy,
        'limit': Limit,
        'into_outfile': IntoOutfile,
        'select_for_update': SelectForUpdate,
    }
    _query_template = six.u(
        'SELECT%(select_options)s%(columns)s%(tables)s'
        '%(where)s%(group_by)s%(having)s'
        '%(order_by)s%(limit)s%(into_outfile)s%(select_for_update)s'
    )

    def __init__(self, *args, **kwds):
        super(Select, self).__init__()
        self.columns(*args, **kwds)

    #  It's here just for shortcut, so you can call just `sql.has('distinct')`
    #+ instead of `sql.has('select_options', 'distinct')` (programmer does not
    #+ have to know about internal implementation).
    def has(self, querypart_name, value=None):
        """Returns True if `querypart_name` with `value` is set.

        For example you can check if you already used condition by `sql.has('where')`.

        If you want to check for more information, for example if that condition
        also contain ID, you can do this by `sql.has('where', 'id')`.
        """
        if super(Select, self).has(querypart_name, value):
            return True
        if not value:
            return super(Select, self).has('select_options', querypart_name)
        return False

    def __and__(self, other):
        """UNION ALL selects."""
        return Union(self, other, UNION_ALL)

    def __or__(self, other):
        """UNION selects."""
        return Union(self, other, UNION)

    def columns(self, *args, **kwds):
        """
        columns('id', 'name', ...)
        columns(('id', 'asId'), ('name', 'asName'))
        columns({'id': 'asId', 'name': 'asName'})
        """
        self._columns.columns(*args, **kwds)
        return self

    def from_(self, *args, **kwds):
        """
        from_('user', 'country', ...)
        from_(('user', 'asUser'), ('user', 'asParent'))
        from_({'user': 'asUser', 'user', 'asParent'})
        """
        self._tables.set(*args, **kwds)
        return self

    def from_table(self, table, alias=None):
        """
        from_table('user')
        from_table('user', alias='asUser')
        """
        self._tables.set((table, alias))
        return self

    def from_tables(self, *args, **kwds):
        """
        from_tables('user', 'country', ...)
        from_tables(('user', 'asUser'), ('user', 'asParent'))
        from_tables({'user': 'asUser', 'user', 'asParent'})
        """
        self.from_(*args, **kwds)
        return self

    def join(self, table):
        """
        join('table')
        join(('table', 'asTable'))
        join({'table': 'asTable'})
        """
        self._tables.join(table)
        return self

    def inner_join(self, table):
        """
        inner_join('table')
        inner_join(('table', 'asTable'))
        inner_join({'table': 'asTable'})
        """
        self._tables.inner_join(table)
        return self

    def left_join(self, table):
        """
        left_join('table')
        left_join(('table', 'asTable'))
        left_join({'table': 'asTable'})
        """
        self._tables.left_join(table)
        return self

    def right_join(self, table):
        """
        right_join('table')
        right_join(('table', 'asTable'))
        right_join({'table': 'asTable'})
        """
        self._tables.right_join(table)
        return self

    def on(self, *args, **kwds):
        """
        on(id='another_id')
        on({'table1.id': 'table2.another_id'})
        on([('table1.id', 'table2.another_id')])
        """
        self._tables.on(*args, **kwds)
        return self

    def where(self, *args, **kwds):
        """
        where(name='Michael', country=None)
        where({'age': 20, 'enabled': True})
        where('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        where('id', range(10, 20, 2), sqlpuzzle.relations.IN)
        where([('id', 20), ('name', '%ch%', sqlpuzzle.relation.LIKE)])
        """
        self._where.where(*args, **kwds)
        return self

    def having(self, *args, **kwds):
        """
        having(name='Michael', country=None)
        having({'age': 20, 'enabled': True})
        having('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        having('id', range(10, 20, 2), sqlpuzzle.relations.IN)
        having([('id', 20), ('name', '%ch%', sqlpuzzle.relation.LIKE)])
        """
        self._having.where(*args, **kwds)
        return self

    def group_by(self, *args, **kwds):
        """
        Default ordering is ASC.
        group_by('firstOrderBy', 'secondOrderBy')
        group_by(('name', 'ASC'), ('last_login', 'DESC'))
        group_by('country', ('id', DESC))
        group_by({'name': 'asc', 'surname': 'desc'})
        """
        self._group_by.group_by(*args, **kwds)
        return self

    def order_by(self, *args, **kwds):
        """
        Default ordering is ASC.
        order_by('firstOrderBy', 'secondOrderBy')
        order_by(('name', 'ASC'), ('last_login', 'DESC'))
        order_by('country', ('id', DESC))
        order_by({'name': 'asc', 'surname': 'desc'})
        """
        self._order_by.order_by(*args, **kwds)
        return self

    def limit(self, limit, offset=None):
        self._limit.limit(limit, offset)
        return self

    def offset(self, offset):
        self._limit.offset(offset)
        return self

    def into_outfile(self, into_outfile):
        self._into_outfile.into_outfile(into_outfile)
        return self

    def fields_terminated_by(self, fields_terminated_by):
        self._into_outfile.fields_terminated_by(fields_terminated_by)
        return self

    def lines_terminated_by(self, lines_terminated_by):
        self._into_outfile.lines_terminated_by(lines_terminated_by)
        return self

    def optionally_enclosed_by(self, optionally_enclosed_by):
        self._into_outfile.optionally_enclosed_by(optionally_enclosed_by)
        return self

    # SELECT OPTIONS

    def sql_cache(self, allow=True):
        self._select_options.sql_cache(allow)
        return self

    def sql_no_cache(self, allow=True):
        self._select_options.sql_no_cache(allow)
        return self

    def all(self, allow=True):
        self._select_options.all(allow)
        return self

    def distinct(self, allow=True):
        self._select_options.distinct(allow)
        return self

    def distinctrow(self, allow=True):
        self._select_options.distinctrow(allow)
        return self

    def sql_small_result(self, allow=True):
        self._select_options.sql_small_result(allow)
        return self

    def sql_big_result(self, allow=True):
        self._select_options.sql_big_result(allow)
        return self

    def sql_buffer_result(self, allow=True):
        self._select_options.sql_buffer_result(allow)
        return self

    def sql_calc_found_rows(self, allow=True):
        self._select_options.sql_calc_found_rows(allow)
        return self

    def straight_join(self, allow=True):
        self._select_options.straight_join(allow)
        return self

    def high_priority(self, allow=True):
        self._select_options.high_priority(allow)
        return self

    def for_update(self, allow=True):
        self._select_for_update.for_update(allow)
        return self

    # Backward compatibility.

    fromTable = from_table
    fromTables = from_tables
    innerJoin = inner_join
    leftJoin = left_join
    rightJoin = right_join
    groupBy = group_by
    orderBy = order_by
    intoOutfile = into_outfile
    fieldsTerminatedBy = fields_terminated_by
    linesTerminatedBy = lines_terminated_by
    optionallyEnclosedBy = optionally_enclosed_by
    sqlCache = sql_cache
    sqlNoCache = sql_no_cache
    sqlSmallResult = sql_small_result
    sqlBigResult = sql_big_result
    sqlBufferResult = sql_buffer_result
    sqlCalcFoundRows = sql_calc_found_rows
    straightJoin = straight_join
    highPriority = high_priority
    forUpdate = for_update
