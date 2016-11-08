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

        with open(source) as csvFile:
            with open (target, 'w', newline='') as newFile:

                if bank == 'rabobank':
                    converter = rabobankConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
                elif bank == 'ing':
                    converter = ingConverter(csv.reader(csvFile, delimiter=';', quotechar='"'))
                else:
                    return False

                converter.setInitialBalance(initial_balance)
                converter.setFinalBalance(final_balance)
                converter.convert()

                gnucashCsv = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                gnucashCsv.writerow(['date', 'credit', 'debet', 'cumulative', 'message'])

                # converter class is iterable
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
            new_row = self.newRow(row, counter)
            if new_row:
                self.rows.append(new_row)

        self.rowcount = len(self.rows)

    def setInitialBalance(self, initial_balance):
        '''
        set the initial balance, for the balance column
        '''
        self.balance = initial_balance

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

    def newRow(self, row, counter):
        '''
        abstract method
        create a new row from an import csv row
        '''
        raise NotImplementedError('interface / abstract class!')


class rabobankConverter(abstractConverter):
    '''
    strategy converter for rabobank csvs
    '''

    def newRow(self, row, counter):
        '''
        create a new row from an import csv row
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
            ' '.join(c for c in message if c not in ';')

        return ' '.join(s.strip() for s in message if s.strip())


class ingConverter(abstractConverter):
    '''
    create a new row from an import csv row
    '''

    def newRow(self, row, counter):
        '''
        return new row from the import csv
        '''

        # skip the title row
        if counter == 0:
            return False

        new_row = []

        # date
        new_row.append(datetime.datetime.strptime(row[1], "%Y%m%d").strftime("%Y-%m-%d"))

        # amount - credit
        if row[6] == 'Bij':
            new_row.append(row[7].replace(",", "."))
            new_row.append(0)

            new_row.append(self.calculateBalance(Decimal(row[7].replace(",", ".")), "credit", counter))
        # amount - debet
        elif row[6] == 'Af':
            new_row.append(0)
            new_row.append(row[7].replace(",", "."))

            new_row.append(self.calculateBalance(Decimal(row[7].replace(",", ".")), "debet", counter))

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
        return str(round(self.balance, 2))

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''
        message = ''
        # [row[2], row[4], row[9], row[10], row[11], row[12]]
        for id, msg in enumerate(row):
            if (id == 2 or id == 4 or id == 9 or id == 10 or id == 11 or id == 12):
                message = message + ' ' + msg.strip()

        ''.join(c for c in message if c not in ';')

        return message


if __name__ == '__main__':
    converter = rabo2gnuCashConverter()
    converter.setTesting()
    converter.convert(
            "C:/home/2016/NL16INGB0007098871_01-06-2016_10-10-2016.csv",
            "C:/coding/python/fred1.csv", 
            "ing", 
            2160.86, 
            345)
