import csv
import datetime
from decimal import *


class rabo2gnuCashConverter:
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
        # convert the input data into a csv row

        new_row = []

        # date
        # there are two dates - this one seems to be the more accurate one
        new_row.append(datetime.datetime.strptime(row[2], "%Y%m%d").strftime("%Y-%m-%d"))

        # amount - credit
        if row[3] == 'C':
            new_row.append(row[4])
            new_row.append(0)

            new_row.append(self.setBalance(Decimal(row[4]), "credit", counter))
        # amount - debet
        elif row[3] == 'D':
            new_row.append(0)
            new_row.append(row[4])

            new_row.append(self.setBalance(Decimal(row[4]), "debet", counter))

        # join the messages array into one string
        new_row.append(self.setMessage(row))

        return new_row

    def setBalance(self, amount, type, counter):
        # calculate the current balance

        if counter == 0:
            return self.balance
        else:
            if type == "credit":
                self.balance = Decimal(self.balance) + amount
            elif type == "debet":
                self.balance = Decimal(self.balance) - amount
        return round(self.balance, 2)

    def setMessage(self, row):
        # get the message from all possible rows

        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        return ' '.join(s.strip() for s in messages if s.strip())
