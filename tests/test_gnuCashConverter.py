from unittest import TestCase
from GnuCashConverter import *


class TestGnuCashConverter(TestCase):
    '''
    test that we consistently import a single csv row
    '''
    def testRaboConverter(self):
        csvFile = 'data/single_account.csv'

        with open(csvFile) as openCsvFile:
            row = self.extractRow(openCsvFile)

            self.assertEqual(row['date'], '2017-12-25')
            self.assertEqual(row['deposit'], 0)
            self.assertEqual(row['withdrawal'], Decimal('1800.00'))
            self.assertEqual(row['balance'], Decimal('6312.58'))
            self.assertEqual(row['message'], 'NL54RABO0143316680 RABONL2UXXX E. DE BOS EO voor de huisrekening en hypotheek bg')

    '''
    extract rows from csv
    '''
    def extractRow(self, csvFile):
        converter = rabobankConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))

        converter.setInitialBalance(123)
        converter.setFinalBalance(0)
        converter.convert()

        return converter.getRow()
