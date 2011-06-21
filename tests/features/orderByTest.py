# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.features.orderBy


class OrderByTest(unittest.TestCase):
    def setUp(self):
        self.orderBy = sqlPuzzle.features.orderBy.OrderBy()

    def tearDown(self):
        self.orderBy = sqlPuzzle.features.orderBy.OrderBy()



class BaseTest(OrderByTest):
    def testIsNotSet(self):
        self.assertEqual(self.orderBy.isSet(), False)
    
    def testIsSet(self):
        self.orderBy.orderBy('id')
        self.assertEqual(self.orderBy.isSet(), True)
    
    def testSimply(self):
        self.orderBy.orderBy('id')
        self.assertEqual(str(self.orderBy), 'ORDER BY `id`')
    
    def testMoreColumns(self):
        self.orderBy.orderBy('id', ['name', 'desc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `id`, `name` DESC')
    
    def testASC(self):
        self.orderBy.orderBy(['name', 'asc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `name`')
    
    def testDESC(self):
        self.orderBy.orderBy(['name', 'desc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `name` DESC')



class BackQuotesTest(OrderByTest):
    def testColumnNameAsTableAndColumn(self):
        self.orderBy.orderBy('table.column')
        self.assertEqual(str(self.orderBy), 'ORDER BY `table`.`column`')
    
    def testColumnNameAsTableAndColumnWithDotInName(self):
        self.orderBy.orderBy('table.`column.`')
        self.assertEqual(str(self.orderBy), 'ORDER BY `table`.`column.`')



class GroupingTest(OrderByTest):
    def testMoreSameColumnsPrintAsOne(self):
        self.orderBy.orderBy('col', 'col')
        self.assertEqual(str(self.orderBy), 'ORDER BY `col`')
    
    def testMoreSameColumnsWithDiffAscPrintAsOne(self):
        self.orderBy.orderBy('col', ('col', 'DESC'))
        self.assertEqual(str(self.orderBy), 'ORDER BY `col` DESC')



class ExceptionsTest(OrderByTest):
    def testNameAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.orderBy.orderBy, 42)
    
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.orderBy.orderBy, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.orderBy.orderBy, True)
    
    def testNotAscOrDescException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.orderBy.orderBy, ('col', 'AAA'))



testCases = (
    BaseTest,
    BackQuotesTest,
    GroupingTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
