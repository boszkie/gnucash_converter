from unittest import TestCase
from GnuCashConverter import *


class TestGnuCashConverter(TestCase):
    '''
    test that we consistently import a single csv row
    '''

    csv_file = 'tests/data/single_account.csv'

    def testRaboConverter(self):
        '''
        test extraction of data from the csv

        :return: void
        '''

        converter = self.prepareConverter()
        row = converter.getRow()

        self.assertEqual(row['date'], '2017-12-01')
        self.assertEqual(row['deposit'], 0)
        self.assertEqual(row['withdrawal'], Decimal('38.16'))
        self.assertEqual(row['balance'], Decimal('4664.10'))
        self.assertEqual(row['message'], 'Tegenrekening IBAN/BBAN BIC tegenpartij Naam tegenpartij Omschrijving-1 Omschrijving-2 Code Transactiereferentie Machtigingskenmerk Incassant ID Betalingskenmerk')

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
