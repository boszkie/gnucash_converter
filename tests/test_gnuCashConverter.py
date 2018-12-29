from unittest import TestCase
from GnuCashConverter import *


class TestGnuCashConverter(TestCase):
    '''
    test that we consistently import a single csv row
    '''

    csv_file = 'data/single_account.csv'

    def testRaboConverter(self):
        '''
        test extraction of data from the csv

        :return: void
        '''

        converter = self.prepareConverter()
        row = converter.getRow()

        self.assertEqual(row['date'], '2017-12-25')
        self.assertEqual(row['deposit'], 0)
        self.assertEqual(row['withdrawal'], Decimal('1800.00'))
        self.assertEqual(row['balance'], Decimal('6312.58'))
        self.assertEqual(row['message'], 'NL54RABO0143316680 RABONL2UXXX E. DE BOS EO voor de huisrekening en hypotheek bg')

    def prepareConverter(self):
        '''
        setup the converter with dummy csv

        :return: object
        '''

        with open(self.csv_file) as open_csv_file:
            converter = rabobankConverter(csv.reader(open_csv_file, delimiter=',', quotechar='"'))

            converter.setInitialBalance(123)
            converter.convert()

            return converter

    def testWriting(self):
        converted = self.prepareConverter()
        GnuCashConverter.write(converted, 'test.csv')