import csv
import datetime
from decimal import *
import locale


class GnuCashConverter:
    '''
    csv to gnucash csv import conversion
    uses the rabobankConverter strategy classes to do the conversion
    '''

    testing = False

    def convert(self, source, target, bank, initial_balance):
        '''
        manages the conversion

        :param source: string
        :param target: string
        :param bank: string
        :param initial_balance: string
        :return: void
        '''

        with open(source) as csvFile:
            if bank == 'rabobank':
                converter = rabobankConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
            elif bank == 'rabobank (old)':
                converter = rabobankTXTConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
            elif bank == 'ing':
                converter = ingConverter(csv.reader(csvFile, delimiter=';', quotechar='"'))
            else:
                return False

                if bank == 'rabobank':
                    converter = rabobankConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
                elif bank == 'rabobank (old)':
                    converter = rabobankTXTConverter(csv.reader(csvFile, delimiter=',', quotechar='"'))
                elif bank == 'ing':
                    converter = ingConverter(csv.reader(csvFile, delimiter=';', quotechar='"'))
                else:
                    return False

    def write(self, converted, target):
        '''
        write the extracted data to a csv

        :param converted: object
        :param target: string
        :return: void
        '''

        with open(target, 'w', newline='') as newFile:
            gnucashCsv = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            gnucashCsv.writerow(['account', 'date', 'deposit', 'withdrawal', 'balance', 'message'])

                gnucashCsv.writerow(['account', 'date', 'deposit', 'withdrawal', 'balance', 'message'])

                # converter class is iterable
                while converter.nextRow():
                    if (self.testing):
                        print(converter.getRow())
                    else:
                        parsedRow = converter.getRow()

                        gnucashCsv.writerow([
                            parsedRow['account'],
                            parsedRow['date'],
                            parsedRow['deposit'],
                            parsedRow['withdrawal'],
                            parsedRow['balance'],
                            parsedRow['message']
                        ])

    def setTesting(self):
        '''
        to set the conversion to print results instead of writing to a csv

        :return: void
        '''

        self.testing = True


class abstractConverter:
    '''
    strategy parent class with shared methods
    '''

    def __init__(self, reader):
        '''
        setup class, save csv reader

        :param reader: object
        :return void
        '''
        self.reader   = reader
        self.pointer  = 0
        self.rowcount = 0
        self.rows     = []

    def convert(self):
        '''
        extract data from the import csv into row array

        :return void
        '''

        for counter, row in enumerate(self.reader):
            new_row = self.newRow(row, counter)
            if new_row:
                self.rows.append(new_row)

        self.rowcount = len(self.rows)

    def setInitialBalance(self, initial_balance):
        '''
        set the initial balance, for the balance column

        :param initial_balance: string
        :return void
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

        :return boolean
        '''

        if self.pointer >= self.rowcount:
            return False

        return True

    def getRow(self):
        '''
        get the next row

        :return object
        '''

        self.pointer += 1

        return self.rows[self.pointer - 1]

    def newRow(self, row, counter):
        '''
        abstract method
        create a new row from an import csv row

        A row contains the following elements:
            [
                Date,
                Deposit,
                Withdrawal,
                Balance,
                Description,
            ]
        '''

        raise NotImplementedError('interface / abstract class!')


class rabobankConverter(abstractConverter):
    '''
    strategy converter for rabobank csvs
    '''

    def newRow(self, row, counter):
        '''
        create a new row from an import csv row

        A row contains the following elements:
            [
                date,
                Deposit,
                Withdrawal,
                Balance,
                Description,
            ]
        '''
        rabobankCsvDecimalSeperator = ','

        # skip the title row
        if counter == 0:
            return False

        newRow = {}

        # account
        newRow['account'] = row[0]

        # date
        newRow['date'] = row[4]

        amount = parseAmount(row[6], rabobankCsvDecimalSeperator)

        # amount - deposit
        if amount >= 0:
            newRow['deposit'] = amount
            newRow['withdrawal'] = 0

        # amount - withdrawal
        else:
            newRow['deposit'] = 0
            newRow['withdrawal'] = amount.copy_abs()

        # Balance
        newRow['balance'] = parseAmount(row[7], rabobankCsvDecimalSeperator)

        newRow['message'] = self.setMessage(row)

        return newRow

    def calculateBalance(self, amount, type, counter):
        '''
        calculate the current balance
        '''

        if counter == 0:
            return self.balance
        else:
            if type == "deposit":
                self.balance = Decimal(self.balance) + amount
            elif type == "withdrawal":
                self.balance = Decimal(self.balance) - amount

        return str(round(self.balance, 2))

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''

        messages = [
            row[8],  # Tegenrekening IBAN/BBAN
            row[12],  # BIC tegenpartij
            row[9],  # Naam tegenpartij
            row[19],  # Omschrijving-1
            row[20],  # Omschrijving-2
            # row[21],  # Omschrijving-3
            row[13],  # Code
            row[15],  # Transactiereferentie
            row[16],  # Machtigingskenmerk
            row[17],  # Incassant ID
            row[18],  # Betalingskenmerk
        ]

        return ' '.join(s.strip() for s in messages if s.strip())


class rabobankTXTConverter(abstractConverter):
    '''
    strategy converter for rabobank cvs
    '''

    def newRow(self, row, counter):
        '''
        create a new row from an import csv row
        '''

        new_row = []

        # date
        # there are two dates - this one seems to be the more accurate one
        new_row.append(datetime.datetime.strptime(row[2], "%Y%m%d").strftime("%Y-%m-%d"))

        # amount - deposit
        if row[3] == 'C':
            new_row.append(row[4])
            new_row.append(0)

            new_row.append(self.calculateBalance(Decimal(row[4]), "deposit", counter))
        # amount - withdrawal
        elif row[3] == 'D':
            new_row.append(0)
            new_row.append(row[4])

            new_row.append(self.calculateBalance(Decimal(row[4]), "withdrawal", counter))

        new_row.append(self.setMessage(row))

        return new_row

    def calculateBalance(self, amount, type, counter):
        '''
        calculate the current balance
        '''

        if counter == 0:
            return self.balance
        else:
            if type == "deposit":
                self.balance = Decimal(self.balance) + amount
            elif type == "withdrawal":
                self.balance = Decimal(self.balance) - amount

        return str(round(self.balance, 2))

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''

        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        return ' '.join(s.strip() for s in messages if s.strip())


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

        # amount - deposit
        if row[6] == 'Bij':
            new_row.append(row[7].replace(",", "."))
            new_row.append(0)

            new_row.append(self.calculateBalance(Decimal(row[7].replace(",", ".")), "deposit", counter))
        # amount - withdrawal
        elif row[6] == 'Af':
            new_row.append(0)
            new_row.append(row[7].replace(",", "."))

            new_row.append(self.calculateBalance(Decimal(row[7].replace(",", ".")), "withdrawal", counter))

        new_row.append(self.setMessage(row))

        return new_row

    def calculateBalance(self, amount, type, counter):
        '''
        calculate the current balance
        '''

        if counter == 0:
            return self.balance
        else:
            if type == "deposit":
                self.balance = Decimal(self.balance) + amount
            elif type == "withdrawal":
                self.balance = Decimal(self.balance) - amount

        return str(round(self.balance, 2))

    def setMessage(self, row):
        '''
        collect the message from all possible rows
        '''

        message = []

        for id, msg in enumerate(row):
            if (id == 2 or id == 4 or id == 9 or id == 10 or id == 11 or id == 12):
                message.append(msg.strip())

        return ''.join(c for c in message)


def parseAmount(amount, amountSeperator):
    '''
    Turn the amount as string into a decimal with the correct decimal seperator.
    It uses the system locale to do this.

    Return amount as Decimal if successful or None if not successful
    '''

    localeSeperator = locale.localeconv()['decimal_point']
    amountDecimal = None

    if amountSeperator == localeSeperator:
        amountDecimal = Decimal(amount)

    # Replace comma seperator to point seperator
    if amountSeperator == ',':
        amountPointSeperator = amount.replace(",", ".")
        amountPointSeperator = amountPointSeperator.replace(
            ".", "", amountPointSeperator.count(".")-1)

        amountDecimal = Decimal(amountPointSeperator)

    # Replace point seperator to point seperator
    if amountSeperator == '.':
        amountCommaSeperator = amount.replace(".", ",")
        amountCommaSeperator = amountCommaSeperator.replace(
            ",", "", amountCommaSeperator.count(","-1))

        amountDecimal = Decimal(amountCommaSeperator)

    return amountDecimal

def parseAmount(amount, amountSeperator):
    '''
    Turn the amount as string into a decimal with the correct decimal seperator.
    It uses the system locale to do this.

    Return amount as Decimal if successful or None if not successful
    '''

    localeSeperator = locale.localeconv()['decimal_point']
    amountDecimal = None

    if amountSeperator == localeSeperator:
        amountDecimal = Decimal(amount)

    # Replace comma seperator to point seperator
    if amountSeperator == ',':
        amountPointSeperator = amount.replace(",", ".")
        amountPointSeperator = amountPointSeperator.replace(
            ".", "", amountPointSeperator.count(".")-1)

        amountDecimal = Decimal(amountPointSeperator)

    # Replace point seperator to point seperator
    if amountSeperator == '.':
        amountCommaSeperator = amount.replace(".", ",")
        amountCommaSeperator = amountCommaSeperator.replace(
            ",", "", amountCommaSeperator.count(","-1))

        amountDecimal = Decimal(amountCommaSeperator)

    return amountDecimal

if __name__ == '__main__':
    converter = GnuCashConverter()
    # converter.setTesting()
    converter.convert(
#            "test.csv",
#            "result2.csv", 
#            "ing", 
#            121212, 
#            345)
            "test.csv",
            "tests/data/single_account.csv",
            "result.csv",
            "rabobank",
            123234)
