from unittest import TestCase
from GnuCashConverter import *

class TestGnuCashConverter(TestCase):
    '''
    test that we consistently import a single csv row
    '''
    def testRaboConverter(self):
        csvFile = 'data/single_account.csv'

        with open(csvFile) as openCsvFile:
            converter = rabobankConverter(csv.reader(openCsvFile, delimiter=',', quotechar='"'))

            converter.setInitialBalance(123)
            converter.setFinalBalance(0)
            converter.convert()

        while converter.nextRow():
            row = converter.getRow()

            # date
            self.assertEqual(row[0], '2017-12-25')
            # credit
            self.assertEqual(row[1], 0)
            # debet
            self.assertEqual(row[2], Decimal('1800.00'))
            # balance
            self.assertEqual(row[3], Decimal('6312.58'))
            # message
            self.assertEqual(row[4], 'NL54RABO0143316680 RABONL2UXXX E. DE BOS EO voor de huisrekening en hypotheek bg')