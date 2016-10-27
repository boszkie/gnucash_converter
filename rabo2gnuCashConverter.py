import csv
import datetime
from decimal import *


class rabo2gnuCashConverter:
    # rabobank csv to gnucash csv import conversion

    def convert(self, source, target, bank, initial_balance, final_balance):
        self.bank            = bank 
        self.initial_balance = initial_balance
        self.final_balance   = final_balance
        self.balance         = self.initial_balance

        with open(source) as csvFile, open (target, 'w', newline='') as newFile:

            rows = rabobankConverter(csvFile, csv.reader(csvFile, delimiter=',', quotechar='"'))

            gnucashCsv = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            while rows.nextRow():
                gnucashCsv.writerow(rows.getRow())



class rabobankConverter:
    # strategy for rabobank csvs

    def __init__(self, csvFile, reader):
            # headings
        self.pointer     = 0
        self.rowcount    = 0
        self.rows        = []

        for counter, row in enumerate(reader):
            self.rows.append(self.newRow(row, counter))

        self.rowcount = len(self.rows)

    def nextRow(self):
        if self.pointer + 1 >= self.rowcount:
            return False

        return True

    def getRow(self):
        if self.pointer == 1:
            return ['date', 'credit', 'debet', 'cumulative', 'message']

        return self.rows[self.pointer]

    def newRow(self, row, counter):
        # return a row from the csv

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
        # collect the message from all possible rows

        messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        return ' '.join(s.strip() for s in messages if s.strip())

if __name__ == '__main__':
    converter = rabo2gnuCashConverter()
    converter.convert("C:/home/2016/20160601_20160923_home.csv", "C:/coding/python/fred1.csv", "rabobank", 123, 345)
