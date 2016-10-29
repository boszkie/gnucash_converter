import csv
import datetime
from decimal import *


class rabo2gnuCashConverter:
    '''
    csv to gnucash csv import conversion
    uses the rabobankConverter strategy classes to do the conversion
    '''

    testing = False

    def convert(self, source, target, bank, initial_balance, final_balance):
        '''
        manages the conversion
        '''

        with open(source) as csvFile, open (target, 'w', newline='') as newFile:

            converter = rabobankConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
            converter.setInitialBalance(initial_balance)
            converter.setFinalBalance(final_balance)
            converter.convert()

            gnucashCsv = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            gnucashCsv.writerow(['date', 'credit', 'debet', 'cumulative', 'message'])
            
            while converter.nextRow():
                if (self.testing):
                    print(converter.getRow())
                else:
                    gnucashCsv.writerow(converter.getRow())

    def setTesting(self):
        '''
        to set the conversion to print results instead of writing to a csv
        '''
        self.testing = True


class abstractConverter:
    '''
    strategy parent class with shared methods
    '''

    def __init__(self, reader):
        '''
        setup class, save csv reader
        '''
        self.reader    = reader
        self.pointer     = 0
        self.rowcount    = 0
        self.rows        = []

    def convert(self):
        '''
        extract data from the import csv into row array
        '''
        for counter, row in enumerate(self.reader):
            self.rows.append(self.newRow(row, counter))

        self.rowcount = len(self.rows)

    def setInitialBalance(self, initial_balance):
        '''
        set the initial balance, for the balance column
        '''
        self.balance = balance

    def setFinalBalance(self, final_balance):
        '''
        set the final balance to check results
        not implemented yet
        '''
        self.final_balance = final_balance
    
    def nextRow(self):
        '''
        do we have a next row for iteration
        '''
        if self.pointer >= self.rowcount:
            return False

        return True

    def getRow(self):
        '''
        get the next row
        '''
        self.pointer += 1

        return self.rows[self.pointer - 1]


class rabobankConverter(abstractConverter):
    '''
    strategy converter for rabobank csvs
    '''

    def newRow(self, row, counter):
        '''
        return new row from the import csv
        '''

        new_row = []

        # date
        # there are two dates - this one seems to be the more accurate one
        new_row.append(datetime.datetime.strptime(row[2], "%Y%m%d").strftime("%Y-%m-%d"))

        # amount - credit
        if row[3] == 'C':
            new_row.append(row[4])
            new_row.append(0)

            new_row.append(self.calculateBalance(Decimal(row[4]), "credit", counter))
        # amount - debet
        elif row[3] == 'D':
            new_row.append(0)
            new_row.append(row[4])

            new_row.append(self.calculateBalance(Decimal(row[4]), "debet", counter))

        new_row.append(self.setMessage(row))

        return new_row

    def calculateBalance(self, amount, type, counter):
        '''
        calculate the current balance
        '''

        if counter == 0:
            return self.balance
        else:
            if type == "credit":
                self.balance = Decimal(self.balance) + amount
            elif type == "debet":
                self.balance = Decimal(self.balance) - amount
        return round(self.balance, 2)

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''

        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        return ' '.join(s.strip() for s in messages if s.strip())


class ingConverter(abstractConverter):
    '''
    strategy for ing csvs
    '''

    def newRow(self, row, counter):
        '''
        return new row from the import csv
        '''

        new_row = []

        # date
        # there are two dates - this one seems to be the more accurate one
        new_row.append(datetime.datetime.strptime(row[2], "%Y%m%d").strftime("%Y-%m-%d"))

        # amount - credit
        if row[3] == 'C':
            new_row.append(row[4])
            new_row.append(0)

            new_row.append(self.calculateBalance(Decimal(row[4]), "credit", counter))
        # amount - debet
        elif row[3] == 'D':
            new_row.append(0)
            new_row.append(row[4])

            new_row.append(self.calculateBalance(Decimal(row[4]), "debet", counter))

        new_row.append(self.setMessage(row))

        return new_row

    def calculateBalance(self, amount, type, counter):
        '''
        calculate the current balance
        '''

        if counter == 0:
            return self.balance
        else:
            if type == "credit":
                self.balance = Decimal(self.balance) + amount
            elif type == "debet":
                self.balance = Decimal(self.balance) - amount
        return round(self.balance, 2)

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''

        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        return ' '.join(s.strip() for s in messages if s.strip())


if __name__ == '__main__':
    converter = rabo2gnuCashConverter()
    converter.setTesting()
    converter.convert("C:/home/2016/20160601_20160923_home.csv", "C:/coding/python/fred1.csv", "rabobank", 2608.91, 345)
