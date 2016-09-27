#!/usr/bin/python

# rabobank csv export to gnucash csv import conversion
import csv
from decimal import *

#starting amount
cum = Decimal('2608.91')

with open('transactions29082016.txt') as csvFile, open ('gnucashFormatted.csv','w', newline='') as newFile:
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
        newrow.append(row[8])

        # amount - credit
        if row[3] == 'C':
            newrow.append(row[4])
            newrow.append('')

            # cumulative amount
            cum = Decimal(cum) + Decimal(row[4])
            newrow.append(round(cum, 2))
        # amount - debet
        elif row[3] == 'D':
            newrow.append('')
            newrow.append(row[4])

            # cumulative amount
            cum = Decimal(cum) - Decimal(row[4])
            newrow.append(round(cum, 2))

        # there are multiple columns that may hold texts
        messages = [row[6], row[7], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]

        for message in messages:
            ' '.join(c for c in messages if c not in ';')

        # join the messages array into one string
        newrow.append(''.join(s.strip() for s in messages if s.strip()))

        gnucashCsv.writerow(newrow)
