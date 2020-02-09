#!/bin/python

import fileinput
import sys
import csv

last = None
lin = 0
buff = []
dataPos = 0
stdin = fileinput.input()
reader = csv.reader(stdin)

def printBuff(typ, buff):
    if not buff:
        return

    sys.stdout.write(typ)
    sys.stdout.write(': ')
    sys.stdout.write(' '.join(buff))
    sys.stdout.write('\n')

def getNextOfType(oldTyp, reader):
    for _ in range(0, 1000):
        row = next(reader)
        time, typ, data = row

        if typ == oldTyp:
            return row

    raise RuntimeError('Failed to get next.')

for line in reader:
    time, typ, data = line

    lin += 1

    #if typ not in ['TX', 'RX']:
    if typ not in ['TX']:
        sys.stderr.write('Skipping line {}.\n'.format(lin))
        continue

    assert(data == '0x01')

    # Count
    counterRow = getNextOfType(typ, reader)
    counterTime, counterTyp, counterData = counterRow
    assert(counterTyp == typ)

    # Action
    actionRow = getNextOfType(typ, reader)
    actionTime, actionTyp, actionData = actionRow
    assert(actionTyp == typ)

    # Payload count
    payloadCountRow = getNextOfType(typ, reader)
    payloadCountTime, payloadCountTyp, payloadCountData = payloadCountRow
    assert(payloadCountTyp == typ)

    payloadCountInDec = int(payloadCountData, 16)

    for i in range(0, payloadCountInDec):
        payloadRow = getNextOfType(typ, reader)
        payloadTime, payloadTyp, payloadData = payloadRow

    # check 1
    check1Row = getNextOfType(typ, reader)
    check1Time, check1Typ, check1Data = check1Row

    # check 2
    check2Row = getNextOfType(typ, reader)
    check2Time, check2Typ, check2Data = check2Row

    # last byte
    endRow = getNextOfType(typ, reader)
    endTime, endTyp, endData = endRow
    assert(endData == '0x04')
