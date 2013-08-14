# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import datetime
import unittest

import sqlpuzzle
from sqlpuzzle._libs.sqlValue import SqlValue, SqlReference


class SqlValueTest(unittest.TestCase):
    def testString(self):
        self.assertEqual(str(SqlValue('Hello World!')), '"Hello World!"')

    def testUnicode(self):
        self.assertEqual(str(SqlValue(u'Hello World!')), '"Hello World!"')

    def testInteger(self):
        self.assertEqual(str(SqlValue(42)), '42')

    def testLongInteger(self):
        self.assertEqual(str(SqlValue(123456789012345)), '123456789012345')

    def testFloat(self):
        self.assertEqual(str(SqlValue(23.456)), '23.45600')

    def testBoolean(self):
        self.assertEqual(str(SqlValue(True)), '1')

    def testDate(self):
        self.assertEqual(str(SqlValue(datetime.date(2011, 5, 25))), '"2011-05-25"')

    def testDatetime(self):
        self.assertEqual(str(SqlValue(datetime.datetime(2011, 5, 25, 19, 33, 20))), '"2011-05-25T19:33:20"')

    def testListWithString(self):
        self.assertEqual(str(SqlValue(['a', 'b', 'c'])), '("a", "b", "c")')

    def testListWithInteger(self):
        self.assertEqual(str(SqlValue([12,23,34])), '(12, 23, 34)')

    def testEmptyList(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue([]))

    def testTupleWithInteger(self):
        self.assertEqual(str(SqlValue(('a', 'b', 'c'))), '("a", "b", "c")')

    def testTupleWithInteger(self):
        self.assertEqual(str(SqlValue((12,23,34))), '(12, 23, 34)')

    def testEmptyTuple(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(()))

    def testSet(self):
        self.assertEqual(str(SqlValue(set([12, 23]))), '(12, 23)')

    def testEmptySet(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(set()))

    def testFrozenSet(self):
        self.assertEqual(str(SqlValue(frozenset([12, 23]))), '(12, 23)')

    def testEmptyFrozenSet(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(frozenset()))

    def testGenerator(self):
        self.assertEqual(str(SqlValue(x for x in (12, 23, 34))), '(12, 23, 34)')

    def testXrange(self):
        self.assertEqual(str(SqlValue(xrange(5))), '(0, 1, 2, 3, 4)')

    def testNone(self):
        self.assertEqual(str(SqlValue(None)), 'NULL')

    def testSubselect(self):
        select = sqlpuzzle.selectFrom('table')
        self.assertEqual(str(SqlValue(select)), '(SELECT * FROM `table`)')



class SqlReferenceTest(unittest.TestCase):
    def testString(self):
        self.assertEqual(str(SqlReference('test')), '`test`')

    def testUnicode(self):
        self.assertEqual(str(SqlReference(u'test')), '`test`')

    def testSubselect(self):
        select = sqlpuzzle.selectFrom('table')
        self.assertEqual(str(SqlReference(select)), '(SELECT * FROM `table`)')

    def testTableColumn(self):
        self.assertEqual(str(SqlReference('table.column')), '`table`.`column`')

    def testDatabaseTableColumn(self):
        self.assertEqual(str(SqlReference('db.table.column')), '`db`.`table`.`column`')



class SecurityTest(unittest.TestCase):
    def testSingleQuotes(self):
        self.assertEqual(str(SqlValue('test\'test')), '"test\\\'test"')

    def testQuotes(self):
        self.assertEqual(str(SqlValue('test"test')), '"test\\"test"')

    def testSlash(self):
        self.assertEqual(str(SqlValue('test\\test')), '"test\\\\test"')

    def testNewLine(self):
        value = """first line
second line"""
        self.assertEqual(str(SqlValue(value)), '"first line\\nsecond line"')



testCases = (
    SqlValueTest,
    SqlReferenceTest,
    SecurityTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)