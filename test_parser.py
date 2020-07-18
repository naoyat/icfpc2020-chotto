#!/usr/bin/env python
from unittest import TestCase, main, skip

from parser import parse_data
from dataio.png import read_from_png
import sys
import re


def autoline(s):
    items = []
    for item in re.split(r' +', s):
        try:
            val = int(item)
            items.append(val)
        except Exception:
            items.append(item)
    return items


def autolines(txt):
    return [autoline(line) for line in txt.split('\n')]


class TestParser(TestCase):
    def sub(self, id, expected=None):
        d = read_from_png('img/message%d.png' % id)
        actual = parse_data(d)
        if actual != expected:
            sys.stderr.write('Case #%d: FAILED\n' % id)
            sys.stderr.write('  Expected: %s\n' % expected)
            sys.stderr.write('    Actual: %s\n' % actual)
        # expected = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[]]
        assert actual == expected

    def test_parse_message_01_Numbers(self):
        self.sub(1, [[0],[1],[2],[3],[4],[5],[6],[7],[8],[]])

    def test_parse_message_02_Numbers_cont(self):
        self.sub(2, [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 506,507,508,509,510,511,512,513,514, 65535,65536,65537]])

    def test_parse_message_03_Negative_Numbers(self):
        self.sub(3, [[4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17, -510,-511,-512,-513,-514, -65535,-65536,-65537]])

    def test_parse_message_04_Equality(self):
        self.sub(4, [
            ['='],
            [0,'=',0],
            [1,'=',1],
            [2,'=',2],
            [3,'=',3],
            [],
            [10,'=',10],
            [11,'=',11],
            [],
            [-1,'=',-1],
            [-2,'=',-2],
            [],
        ])

    def test_parse_message_05_Successor(self):
        self.sub(5, [
            ['inc'],
            ['ap','inc',0,'=',1],
            ['ap','inc',1,'=',2],
            ['ap','inc',2,'=',3],
            ['ap','inc',3,'=',4],
            [],
            ['ap','inc',300,'=',301],
            ['ap','inc',301,'=',302],
            [],
            ['ap','inc',-1,'=',0],
            ['ap','inc',-2,'=',-1],
            ['ap','inc',-3,'=',-2],
            [],
        ])

    def test_parse_message_06_Predecessor(self):
        self.sub(6,[
            ['dec'],
            ['ap','dec',1,'=',0],
            ['ap','dec',2,'=',1],
            ['ap','dec',3,'=',2],
            ['ap','dec',4,'=',3],
            [],
            ['ap','dec',1024,'=',1023],
            [],
            ['ap','dec',0,'=',-1],
            ['ap','dec',-1,'=',-2],
            ['ap','dec',-2,'=',-3],
            [],
        ])

    def test_parse_message_07_Sum(self):
        self.sub(7, [
            ['add'],
            ['ap', 'ap', 'add', 1, 2, '=', 3],
            ['ap', 'ap', 'add', 2, 1, '=', 3],
            ['ap', 'ap', 'add', 0, 1, '=', 1],
            ['ap', 'ap', 'add', 2, 3, '=', 5],
            ['ap', 'ap', 'add', 3, 5, '=', 8],
            [],
        ])

    def test_parse_message_08_Variables(self):
        self.sub(8, [
            ['x0', 'x1', 'x2', 'x3', 'x4'],
            ['ap', 'ap', 'add', 0, 'x0', '=', 'x0'],
            ['ap', 'ap', 'add', 0, 'x1', '=', 'x1'],
            ['ap', 'ap', 'add', 0, 'x2', '=', 'x2'],
            [],
            ['ap', 'ap', 'add', 'x0', 0, '=', 'x0'],
            ['ap', 'ap', 'add', 'x1', 0, '=', 'x1'],
            ['ap', 'ap', 'add', 'x2', 0, '=', 'x2'],
            [],
            ['ap', 'ap', 'add', 'x0', 'x1', '=', 'ap', 'ap', 'add', 'x1', 'x0'],
            [],
        ])

    def test_parse_message_09_Product(self):
        self.sub(9, [
            ['mul'],
            ['ap', 'ap', 'mul', 4, 2, '=', 8],
            ['ap', 'ap', 'mul', 3, 4, '=', 12],
            ['ap', 'ap', 'mul', 3, -2, '=', -6],
            ['ap', 'ap', 'mul', 'x0', 'x1', '=', 'ap', 'ap', 'mul', 'x1', 'x0'],
            ['ap', 'ap', 'mul', 'x0', 0, '=', 0],
            ['ap', 'ap', 'mul', 'x0', 1, '=', 'x0'],
            [],
        ])

    def test_parse_message_10_Integer_Division(self):
        self.sub(10, [
            ['div'],
            ['ap', 'ap', 'div', 4, 2, '=', 2],
            ['ap', 'ap', 'div', 4, 3, '=', 1],
            ['ap', 'ap', 'div', 4, 4, '=', 1],
            ['ap', 'ap', 'div', 4, 5, '=', 0],
            ['ap', 'ap', 'div', 5, 2, '=', 2],
            ['ap', 'ap', 'div', 6, -2, '=', -3],
            ['ap', 'ap', 'div', 5, -3, '=', -1],
            ['ap', 'ap', 'div', -5, 3, '=', -1],
            ['ap', 'ap', 'div', -5, -3, '=', 1],
            ['ap', 'ap', 'div', 'x0', 1, '=', 'x0'],
            [],
        ])

    def test_parse_message_11_Equality_and_Booleans(self):
        self.sub(11, [
            ['eq'],
            ['ap', 'ap', 'eq', 'x0', 'x0', '=', 't'],
            ['ap', 'ap', 'eq', 0, -2, '=', 'f'],
            ['ap', 'ap', 'eq', 0, -1, '=', 'f'],
            ['ap', 'ap', 'eq', 0, 0, '=', 't'],
            ['ap', 'ap', 'eq', 0, 1, '=', 'f'],
            ['ap', 'ap', 'eq', 0, 2, '=', 'f'],
            [],
            ['ap', 'ap', 'eq', 1, -1, '=', 'f'],
            ['ap', 'ap', 'eq', 1, 0, '=', 'f'],
            ['ap', 'ap', 'eq', 1, 1, '=', 't'],
            ['ap', 'ap', 'eq', 1, 2, '=', 'f'],
            ['ap', 'ap', 'eq', 1, 3, '=', 'f'],
            [],
            ['ap', 'ap', 'eq', 2, 0, '=', 'f'],
            ['ap', 'ap', 'eq', 2, 1, '=', 'f'],
            ['ap', 'ap', 'eq', 2, 2, '=', 't'],
            ['ap', 'ap', 'eq', 2, 3, '=', 'f'],
            ['ap', 'ap', 'eq', 2, 4, '=', 'f'],
            [],
            ['ap', 'ap', 'eq', 19, 20, '=', 'f'],
            ['ap', 'ap', 'eq', 20, 20, '=', 't'],
            ['ap', 'ap', 'eq', 21, 20, '=', 'f'],
            [],
            ['ap', 'ap', 'eq', -19, -20, '=', 'f'],
            ['ap', 'ap', 'eq', -20, -20, '=', 't'],
            ['ap', 'ap', 'eq', -21, -20, '=', 'f'],
            [],
        ])

    def test_parse_message_12_Strict_Less_Than(self):
        self.sub(12, [
            ['lt'],
            ['ap', 'ap', 'lt', 0, -1, '=', 'f'],
            ['ap', 'ap', 'lt', 0, 0, '=', 'f'],
            ['ap', 'ap', 'lt', 0, 1, '=', 't'],
            ['ap', 'ap', 'lt', 0, 2, '=', 't'],
            [],
            ['ap', 'ap', 'lt', 1, 0, '=', 'f'],
            ['ap', 'ap', 'lt', 1, 1, '=', 'f'],
            ['ap', 'ap', 'lt', 1, 2, '=', 't'],
            ['ap', 'ap', 'lt', 1, 3, '=', 't'],
            [],
            ['ap', 'ap', 'lt', 2, 1, '=', 'f'],
            ['ap', 'ap', 'lt', 2, 2, '=', 'f'],
            ['ap', 'ap', 'lt', 2, 3, '=', 't'],
            ['ap', 'ap', 'lt', 2, 4, '=', 't'],
            [],
            ['ap', 'ap', 'lt', 19, 20, '=', 't'],
            ['ap', 'ap', 'lt', 20, 20, '=', 'f'],
            ['ap', 'ap', 'lt', 21, 20, '=', 'f'],
            [],
            ['ap', 'ap', 'lt', -19, -20, '=', 'f'],
            ['ap', 'ap', 'lt', -20, -20, '=', 'f'],
            ['ap', 'ap', 'lt', -21, -20, '=', 't'],
            [],
        ])

    def test_parse_message_13_Modulate(self):
        self.sub(13, [
            ['mod'],
            ['ap', 'mod', 0, '=', ],
            ['ap', 'mod', 1, '=', ],
            ['ap', 'mod', -1, '=', ],
            ['ap', 'mod', 2, '=', ],
            ['ap', 'mod', -2, '=', ],
            [],
            ['ap', 'mod', 16, '=', ],
            ['ap', 'mod', -16, '=', ],
            [],
            ['ap', 'mod', 255, '=', ],
            ['ap', 'mod', -255, '=', ],
            ['ap', 'mod', 256, '=', ],
            ['ap', 'mod', -256, '=', ],
            [],
        ])

    def test_parse_message_14_Demodulate(self):
        self.sub(14, [
            ['dem'],
            ['ap', 'dem', 'ap', 'mod', 'x0', '=', 'x0'],
            ['ap', 'mod', 'ap', 'dem', 'x0', '=', 'x0'],
        ])

    @skip
    def test_parse_message_15_Send(self):
        self.sub(15, [
            ['send'],
            ['ap', 'send', 'x0', '=', 'x1'],
            ['humans', 'x0', 'aliens'],
            ['humans', '~~', 'ap', 'mod', 'x0', 'aliens'],
            ['humans', 'x0', 'aliens'],
            ['humans', 'x1', 'aliens'],
            ['humans', 'ap', 'mod', 'x1', '~~', 'aliens'],
            ['humans', 'x1', 'aliens'],
        ])

    def test_parse_message_16_Negate(self):
        self.sub(16, [
            ['neg'],
            ['ap', 'neg', 0, '=', 0],
            ['ap', 'neg', 1, '=', -1],
            ['ap', 'neg', -1, '=', 1],
            ['ap', 'neg', 2, '=', -2],
            ['ap', 'neg', -2, '=', 2],
            [],
        ])

    def test_parse_message_17_Function_Application(self):
        self.sub(17, [
            ['ap'],
            ['ap', 'inc', 'ap', 'inc', 0, '=', 2],
            ['ap', 'inc', 'ap', 'inc', 'ap', 'inc', 0, '=', 3],
            ['ap', 'inc', 'ap', 'dec', 'x0', '=', 'x0'],
            ['ap', 'dec', 'ap', 'inc', 'x0', '=', 'x0'],
            ['ap', 'dec', 'ap', 'ap','add', 'x0', 1, '=', 'x0'],
            ['ap', 'ap', 'add', 'ap', 'ap', 'add', 2, 3, 4, '=', 9],
            ['ap', 'ap', 'add', 2, 'ap', 'ap', 'add', 3, 4, '=', 9],
            ['ap', 'ap', 'add', 'ap', 'ap', 'mul', 2, 3, 4, '=', 10],
            ['ap', 'ap', 'mul', 2, 'ap', 'ap', 'add', 3, 4, '=', 14],
            ['inc', '=', 'ap', 'add', 1],
            ['dec', '=', 'ap', 'add', 'ap', 'neg', 1],
            [],
        ])

    def test_parse_message_18_S_Combinator(self):
        self.sub(18, [
            ['s'],
            ['ap', 'ap', 'ap', 's', 'x0', 'x1', 'x2', '=', 'ap', 'ap', 'x0', 'x2', 'ap', 'x1', 'x2'],
            ['ap', 'ap', 'ap', 's', 'add', 'inc', 1, '=', 3],
            ['ap', 'ap', 'ap', 's', 'mul', 'ap', 'add', 1, 6, '=', 42],
            [],
        ])

    def test_parse_message_19_C_Combinator(self):
        self.sub(19, [
            ['c'],
            ['ap', 'ap', 'ap', 'c', 'x0', 'x1', 'x2', '=', 'ap', 'ap', 'x0', 'x2', 'x1'],
            ['ap', 'ap', 'ap', 'c', 'add', 1, 2, '=', 3],
            [],
        ])

    def test_parse_message_20_B_Combinator(self):
        self.sub(20, [
            ['b'],
            ['ap', 'ap', 'ap', 'b', 'x0', 'x1', 'x2', '=', 'ap', 'x0', 'ap', 'x1', 'x2'],
            ['ap', 'ap', 'ap', 'b', 'inc', 'dec', 'x0', '=', 'x0'],
            [],
        ])

    def test_parse_message_21_True_K_Combinator(self):
        self.sub(21, [
            ['t'],
            ['ap', 'ap', 't', 'x0', 'x1', '=', 'x0'],
            ['ap', 'ap', 't', 1, 5, '=', 1],
            ['ap', 'ap', 't', 't', 'i', '=', 't'],
            ['ap', 'ap', 't', 't', 'ap', 'inc', 5, '=', 't'],
            ['ap', 'ap', 't', 'ap', 'inc', 5, 't', '=', 6],
            [],
        ])

    def test_parse_message_22_False(self):
        self.sub(22, [
            ['f'],
            ['ap', 'ap', 'f', 'x0', 'x1', '=', 'x1'],
            ['f', '=', 'ap', 's', 't'],
        ])

    def test_parse_message_23_Power_of_Two(self):
        self.sub(23, [
            ['pwr2'],
            autoline('pwr2   =   ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1'),
            autoline('ap pwr2 0   =   ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 0'),
            autoline('ap pwr2 0   =   ap ap ap ap c ap eq 0 1 0 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0'),
            autoline('ap pwr2 0   =   ap ap ap ap eq 0 0 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0'),
            autoline('ap pwr2 0   =   ap ap t 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0'),
            autoline('ap pwr2 0   =   1'),
            autoline('ap pwr2 1   =   ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap ap ap c ap eq 0 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap ap ap eq 0 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap f 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap ap b pwr2 ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap pwr2 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap ap ap c ap eq 0 1 ap ap add -1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap ap ap eq 0 ap ap add -1 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap ap ap eq 0 0 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 ap ap t 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1'),
            autoline('ap pwr2 1   =   ap ap mul 2 1'),
            autoline('ap pwr2 1   =   2'),
            autoline('ap pwr2 2   =   ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 2'),
            [],
            autoline('ap pwr2 2   =   4'),
            autoline('ap pwr2 3   =   8'),
            autoline('ap pwr2 4   =   16'),
            autoline('ap pwr2 5   =   32'),
            autoline('ap pwr2 6   =   64'),
            autoline('ap pwr2 7   =   128'),
            autoline('ap pwr2 8   =   256'),
            [],
        ])


    def test_parse_message_24_I_Combinator(self):
        # i(x) = x  ; identity
        self.sub(24, [
            ['i'],
            ['ap', 'i', 'x0', '=', 'x0'],
            ['ap', 'i', 1, '=', 1],
            ['ap', 'i', 'i', '=', 'i'],
            ['ap', 'i', 'add', '=', 'add'],
            ['ap', 'i', 'ap', 'add', 1, '=', 'ap', 'add', 1],
            [],
        ])

    def test_parse_message_25_Cons__or_Pair(self):
        self.sub(25, [
            ['cons'],
            ['ap', 'ap', 'ap', 'cons', 'x0', 'x1', 'x2', '=', 'ap', 'ap', 'x2', 'x0', 'x1'],
        ])


    def test_parse_message_26_Car__First(self):
        self.sub(26, [
            ['car'],
            ['ap', 'car', 'ap', 'ap', 'cons', 'x0', 'x1', '=', 'x0'],
            ['ap', 'car', 'x2', '=', 'ap', 'x2', 't'],
        ])

    def test_parse_message_27_Cdr__Tail(self):
        self.sub(27, [
            ['cdr'],
            ['ap', 'cdr', 'ap', 'ap', 'cons', 'x0', 'x1', '=', 'x1'],
            ['ap', 'cdr', 'x2', '=', 'ap', 'x2', 'f'],
        ])

    def test_parse_message_28_Nil__Empty_List(self):
        self.sub(28, [
            ['nil'],
            ['ap', 'nil', 'x0', '=', 't'],
        ])

    def test_parse_message_29_Is_Nil__Is_Empty_List(self):
        self.sub(29, [
            ['isnil'],
            ['ap', 'isnil', 'nil', '=', 't'],
            ['ap', 'isnil', 'ap', 'ap', 'cons', 'x0', 'x1', '=', 'f'],
        ])

    def test_parse_message_30_List_Construction_Syntax(self):
        self.sub(30, [
            ['(', ',', ')'],
            ['(', ')', '=', 'nil'],
            ['(', 'x0', ')',
             '=', 'ap', 'ap', 'cons', 'x0', 'nil'],
            ['(', 'x0', ',', 'x1', ')',
             '=', 'ap', 'ap', 'cons', 'x0', 'ap', 'ap', 'cons', 'x1', 'nil'],
            ['(', 'x0', ',', 'x1', ',', 'x2', ')',
             '=', 'ap', 'ap', 'cons', 'x0', 'ap', 'ap', 'cons', 'x1', 'ap', 'ap', 'cons', 'x2', 'nil'],
            ['(', 'x0', ',', 'x1', ',', 'x2', ',', 'x5', ')',
             '=', 'ap', 'ap', 'cons', 'x0', 'ap', 'ap', 'cons', 'x1', 'ap', 'ap', 'cons', 'x2', 'ap', 'ap', 'cons', 'x5', 'nil'],
            [],
        ])

    def test_parse_message_31_Vector(self):
        self.sub(31, [
            ['vec'],
            ['vec', '=', 'cons'],
        ])

    def test_parse_message_32_Draw(self):
        self.sub(32, [
            ['draw'],
            ['ap', 'draw', '(', ')', '='],
            ['ap', 'draw', '(', 'ap', 'ap', 'vec', 1, 1, ')', '='],
            ['ap', 'draw', '(', 'ap', 'ap', 'vec', 1, 2, ')', '='],
            ['ap', 'draw', '(', 'ap', 'ap', 'vec', 2, 5, ')', '='],
            ['ap', 'draw', '(', 'ap', 'ap', 'vec', 1, 2, ',',
                                'ap', 'ap', 'vec', 3, 1, ')', '='],
            ['ap', 'draw', '(', 'ap', 'ap', 'vec', 5, 3, ',',
                                'ap', 'ap', 'vec', 6, 3, ',',
                                'ap', 'ap', 'vec', 4, 4, ',',
                                'ap', 'ap', 'vec', 6, 4, ',',
                                'ap', 'ap', 'vec', 4, 5, ')', '='],
            [],
        ])

    def test_parse_message_33_Checkerboard(self):
        self.sub(33, [
            ['checkerboard'],
            autoline('checkerboard = ap ap s ap ap b s ap ap c ap ap b c ap ap b ap c ap c ap ap s ap ap b s ap ap b ap b ap ap s i i lt eq ap ap s mul i nil ap ap s ap ap b s ap ap b ap b cons ap ap s ap ap b s ap ap b ap b cons ap c div ap c ap ap s ap ap b b ap ap c ap ap b b add neg ap ap b ap s mul div ap ap c ap ap b b checkerboard ap ap c add 2'),
            autoline('ap ap checkerboard 7 0   ='), #    |picture1|
            autoline('ap ap checkerboard 13 0   ='), #   |picture2|
        ])

    def test_parse_message_34_Multiple_Draw(self):
        self.sub(34, [
            ['multipledraw'],
            ['ap', 'multipledraw', 'nil', '=', 'nil'],
            ['ap', 'multipledraw', 'ap', 'ap', 'cons', 'x0', 'x1', '=', 'ap', 'ap', 'cons', 'ap', 'draw', 'x0', 'ap', 'multipledraw', 'x1'],
        ])

    def test_parse_message_35_Modulate_List(self):
        self.sub(35, [
            ['mod', 'cons'],
            ['ap', 'mod', 'nil', '=', ], # '[nil]'],
            ['ap', 'mod', 'ap', 'ap', 'cons', 'nil', 'nil', '=', ], # '[ap', 'ap', 'cons', 'nil', 'nil]'],
            ['ap', 'mod', 'ap', 'ap', 'cons', 0, 'nil', '=', ], #'[ap', 'ap', 'cons', 0, 'nil]'],
            ['ap', 'mod', 'ap', 'ap', 'cons', 1, 2, '=', ], #'[ap', 'ap', 'cons', 1, '2]'],
            ['ap', 'mod', 'ap', 'ap', 'cons', 1, 'ap', 'ap', 'cons', 2, 'nil', '=', ], #'[ap', 'ap', 'cons', 1, 'ap', 'ap', 'cons', 2, 'nil]'],
            ['ap', 'mod', '(', 1, ',', 2, ')', '=', ], #'[(', 1, ',', 2, ')]'],
            ['ap', 'mod', '(', 1, ',', '(', 2, ',', 3, ')', ',', 4, ')', '=', ], #'[(', 1, ',', '(', 2, ',', 3, ')', ',', 4, ')]'],
            [],
        ])

    def test_parse_message_36_Send(self):
        self.sub(36, [
            [':1678847'],
            ['ap', 'send', '(', 0, ')', '=', '(', 1, ',', ':1678847', ')'],
        ])

    def test_parse_message_37_Is_0(self):
        self.sub(37, [
            ['if0'],
            ['ap', 'ap', 'ap', 'if0', 0, 'x0', 'x1', '=', 'x0'],
            ['ap', 'ap', 'ap', 'if0', 1, 'x0', 'x1', '=', 'x1'],
        ])

    def test_parse_message_38_Interact(self):
        self.sub(38, [
            ['interact'],
            autoline('ap modem x0 = ap dem ap mod x0'),
            autoline('ap ap f38 x2 x0 = ap ap ap if0 ap car x0 ( ap modem ap car ap cdr x0 , ap multipledraw ap car ap cdr ap cdr x0 ) ap ap ap interact x2 ap modem ap car ap cdr x0 ap send ap car ap cdr ap cdr x0'),
            # autoline('ap ap ap interact x2 x4 x3 = ap ap f38 x2 ap ap x2 x4 x3'),
            autoline('ap ap ap interact x2 x4 x5 = ap ap f38 x2 ap ap x2 x4 x5'),
        ])

    def test_parse_message_39_Interaction_Protocol(self):
        self.sub(39, [
            ['interact'],
            autoline('ap ap ap interact x0 nil ap ap vec 0 0 = ( x16 , ap multipledraw x64 )'),
            autoline('ap ap ap interact x0 x16 ap ap vec x1 x2 = ( x17 , ap multipledraw x65 )'),
            autoline('ap ap ap interact x0 x17 ap ap vec x3 x4 = ( x18 , ap multipledraw x66 )'),
            autoline('ap ap ap interact x0 x18 ap ap vec x5 x6 = ( x19 , ap multipledraw x67 )'),
            [],
        ])

    def test_parse_message_40_Stateless_Drawing_Protocol(self):
        self.sub(40, [
            ['ap', 'interact', 'statelessdraw'],
            autoline('ap ap statelessdraw x0 x1 = ( 0 , nil , ( ( x1 ) ) )'),
            autoline('statelessdraw = ap ap c ap ap b b ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c ap ap b cons ap ap c cons nil nil'),
            autoline('ap ap ap interact statelessdraw nil ap ap vec 1 0 = ( nil , (   ) )'),  # [1,0]
            autoline('ap ap ap interact statelessdraw nil ap ap vec 2 3 = ( nil , (   ) )'),  # [2,3]
            autoline('ap ap ap interact statelessdraw nil ap ap vec 4 1 = ( nil , (   ) )'),  # [4,1]
            [],
        ])

    def test_parse_message_41_Stateful_Drawing_Protocol(self):
        self.sub(41, [
            ['ap', 'interact', ':67108929'],
            autoline('ap ap :67108929 x0 x1 = ( 0 , ap ap cons x1 x0 , ( ap ap cons x1 x0 ) )'),
            autoline(':67108929 = ap ap b ap b ap ap s ap ap b ap b ap cons 0 ap ap c ap ap b b cons ap ap c cons nil ap ap c cons nil ap c cons'),
            autoline('ap ap ap interact :67108929 nil ap ap vec 0 0 = ( ( ap ap vec 0 0 ) , (    ) )'),  # [0,0]
            autoline('ap ap ap interact :67108929 ( ap ap vec 0 0 ) ap ap vec 2 3 = ( x2 , (    ) )'),  # [0,0;2,3]
            autoline('ap ap ap interact :67108929 x2 ap ap vec 1 2 = ( x3 , (   ) )'),  # [0,0;2,3;1,2]
            autoline('ap ap ap interact :67108929 x3 ap ap vec 3 2 = ( x4 , (   ) )'),  # [0,0;2,3;1,2;3,2]
            autoline('ap ap ap interact :67108929 x4 ap ap vec 4 0 = ( x5 , (   ) )'),  # [0,0;2,3;1,2;3,2;4,0]
            [],
        ])

    def test_parse_message_42_Galaxy(self):
        self.sub(42, [
            ['ap', 'interact', 'galaxy', '=', ],
        ])


if __name__ == '__main__':
    main()
