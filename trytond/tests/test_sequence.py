# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import datetime
from trytond.tests.test_tryton import install_module, with_transaction
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.exceptions import UserError


class SequenceTestCase(unittest.TestCase):
    'Test Sequence'

    @classmethod
    def setUpClass(cls):
        install_module('tests')

    @with_transaction()
    def test_incremental(self):
        'Test incremental'
        pool = Pool()
        Sequence = pool.get('ir.sequence')

        sequence, = Sequence.create([{
                    'name': 'Test incremental',
                    'code': 'test',
                    'prefix': '',
                    'suffix': '',
                    'type': 'incremental',
                    }])
        self.assertEqual(sequence.number_next, 1)
        self.assertEqual(Sequence.get_id(sequence), '1')

        Sequence.write([sequence], {
                'number_increment': 10,
                })
        self.assertEqual(sequence.number_next, 2)
        self.assertEqual(Sequence.get_id(sequence), '2')
        self.assertEqual(Sequence.get_id(sequence), '12')

        Sequence.write([sequence], {
                'padding': 3,
                })
        self.assertEqual(sequence.number_next, 22)
        self.assertEqual(Sequence.get_id(sequence), '022')

    @with_transaction()
    def test_decimal_timestamp(self):
        'Test Decimal Timestamp'
        pool = Pool()
        Sequence = pool.get('ir.sequence')

        sequence, = Sequence.create([{
                    'name': 'Test decimal timestamp',
                    'code': 'test',
                    'prefix': '',
                    'suffix': '',
                    'type': 'decimal timestamp',
                    }])
        timestamp = Sequence.get_id(sequence)
        self.assertEqual(timestamp, str(sequence.last_timestamp))

        self.assertEqual(sequence.number_next, None)

        self.assertNotEqual(Sequence.get_id(sequence), timestamp)

        next_timestamp = Sequence._timestamp(sequence)
        self.assertRaises(UserError, Sequence.write, [sequence], {
                'last_timestamp': next_timestamp + 100,
                })

    @with_transaction()
    def test_hexadecimal_timestamp(self):
        'Test Hexadecimal Timestamp'
        pool = Pool()
        Sequence = pool.get('ir.sequence')

        sequence, = Sequence.create([{
                    'name': 'Test hexadecimal timestamp',
                    'code': 'test',
                    'prefix': '',
                    'suffix': '',
                    'type': 'hexadecimal timestamp',
                    }])
        timestamp = Sequence.get_id(sequence)
        self.assertEqual(timestamp,
            hex(int(sequence.last_timestamp))[2:].upper())

        self.assertEqual(sequence.number_next, None)

        self.assertNotEqual(Sequence.get_id(sequence), timestamp)

        next_timestamp = Sequence._timestamp(sequence)
        self.assertRaises(UserError, Sequence.write, [sequence], {
                'last_timestamp': next_timestamp + 100,
                })

    @with_transaction()
    def test_prefix_suffix(self):
        'Test prefix/suffix'
        pool = Pool()
        Sequence = pool.get('ir.sequence')

        sequence, = Sequence.create([{
                    'name': 'Test incremental',
                    'code': 'test',
                    'prefix': 'prefix/',
                    'suffix': '/suffix',
                    'type': 'incremental',
                    }])
        self.assertEqual(Sequence.get_id(sequence),
            'prefix/1/suffix')

        Sequence.write([sequence], {
                'prefix': '${year}-${month}-${day}/',
                'suffix': '/${day}.${month}.${year}',
                })
        with Transaction().set_context(date=datetime.date(2010, 8, 15)):
            self.assertEqual(Sequence.get_id(sequence),
                '2010-08-15/2/15.08.2010')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(SequenceTestCase)
