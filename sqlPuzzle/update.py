# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import exceptions
import query


class Update(query.Query):
    def __init__(self, table=None):
        """
        Initialization of Update.
        """
        query.Query.__init__(self)
        self.table(table)
        self.__allowUpdateAll = False
    
    def __str__(self):
        """
        Print query.
        """
        update = "UPDATE %s SET %s" % (
            str(self._tables),
            str(self._values),
        )
        if self._conditions.isSet(): update = "%s %s" % (update, self._conditions)
        elif not self.__allowUpdateAll: raise exceptions.ConfirmUpdateAllException()
        
        return update
    
    def _typeOfQuery(self):
        return 'UPDATE'
    
    def allowUpdateAll(self):
        self.__allowUpdateAll = True
    
    def forbidUpdateAll(self):
        self.__allowUpdateAll = False
    
    def table(self, table):
        """
        Set table.
        """
        self._tables.set(table)
        return self
    
    def set(self, *args, **kwds):
        """
        Set columns and values.
        """
        self._values.set(*args, **kwds)
        return self
    
    def where(self, *args, **kwds):
        """
        Set condition(s) to query.
        """
        self._conditions.where(*args, **kwds)
        return self
