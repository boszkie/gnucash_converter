#!/usr/bin/python

# rabobank csv export to gnucash csv import conversion
import csv
from decimal import *

class rabo2gnucashconverter:
    #starting amount
    #cum = Decimal('2608.91')

    def convert(self, source, target, startCum, finishCum):
        self.startCum = startCum
        self.finishCum = finishCum

        self.balance = self.startCum

        with open(source) as csvFile, open (target,'w', newline='') as newFile:
            originalCsv  = csv.reader(csvFile, delimiter=',', quotechar='"')
            gnucashCsv   = csv.writer(newFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # headings
            gnucashCsv.writerow(['date', 'credit', 'debet', 'cumulative', 'message'])

            # go thru the csv row by row
            for row in originalCsv:

                # array to formatted values for each row
                newrow = []

                # date
                # there are two dates - this one seems to be the more accurate one
                newrow.append(row[7])

                # amount - credit
                if row[3] == 'C':
                    newrow.append(row[4])
                    newrow.append('')

                    # cumulative amount
                    self.balance = Decimal(self.balance) + Decimal(row[4])
                    newrow.append(round(self.balance, 2))
                # amount - debet
                elif row[3] == 'D':
                    newrow.append('')
                    newrow.append(row[4])

                    # cumulative amount
                    self.balance = Decimal(self.balance) - Decimal(row[4])
                    newrow.append(round(self.balance, 2))

                # there are multiple columns that may hold texts
                messages = [row[5], row[6], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

                for message in messages:
                    ' '.join(c for c in messages if c not in ';')

                # join the messages array into one string
                newrow.append(''.join(s.strip() for s in messages if s.strip()))

                gnucashCsv.writerow(newrow)

test = rabo2gnucashconverter()
test.convert('C:\\home\\2016\\20160601_20160923_home.csv', 'C:\\coding\\python\\test.csv', 123, 1234)