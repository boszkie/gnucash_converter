import csv
from decimal import *

class rabo2gnuCash:
    # rabobank csv to gnucash csv import conversion

    def convert(self, source, target, initial_balance, final_balance):
        self.initial_balance = initial_balance
        self.final_balance = final_balance
        self.balance = self.initial_balance

        with open(source) as csvFile, open (target,'w', newline='') as newFile:

            originalCsv  = csv.reader(csvFile, delimiter=',', quotechar='"')
            gnucashCsv   = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # headings
            gnucashCsv.writerow(['date', 'credit', 'debet', 'cumulative', 'message'])

            for counter, row in enumerate(originalCsv):

                gnucashCsv.writerow(self.newRow(row, counter))

    def newRow(self, row, counter):
        new_row = []

        # date
        # there are two dates - this one seems to be the more accurate one
        new_row.append(row[7])

        # amount - credit
        if row[3] == 'C':
            new_row.append(row[4])
            new_row.append('')

            # cumulative amount
            if counter == 0:
                new_row.append(self.balance)
            else:
                self.balance = Decimal(self.balance) + Decimal(row[4])
                new_row.append(round(self.balance, 2))
        # amount - debet
        elif row[3] == 'D':
            new_row.append('')
            new_row.append(row[4])

            # cumulative amount
            if counter == 0:
                new_row.append(self.balance)
            else:
                self.balance = Decimal(self.balance) - Decimal(row[4])
                new_row.append(round(self.balance, 2))

        # there are multiple columns that may hold texts
        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        # join the messages array into one string
        new_row.append(''.join(s.strip() for s in messages if s.strip()))

        return new_row

if __name__ == '__main__':
    test = rabo2gnuCash()
    test.convert('C:\\home\\2016\\20160601_20160923_home.csv', 'C:\\coding\\python\\test.csv', 123, 1234)
