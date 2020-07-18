#!/usr/bin/env python
from unittest import TestCase, main, skip

from vm import VM, tokenize


class TestVMEval(TestCase):

    def setUp(self):
        self.vm = VM()

    def check(self, line, expected):
        tokens = tokenize(line)
        actual, _ = self.vm.eval(tokens)
        assert actual == expected

    def test_05_Successor(self):
        self.check('ap inc 0', 1)
        self.check('ap inc 1', 2)
        self.check('ap inc 2', 3)
        self.check('ap inc 3', 4)

        self.check('ap inc 300', 301)
        self.check('ap inc 301', 302)

        self.check('ap inc -1', 0)
        self.check('ap inc -2', -1)
        self.check('ap inc -3', -2)

    def test_06_Predecessor(self):
        self.check('ap dec 1', 0)
        self.check('ap dec 2', 1)
        self.check('ap dec 3', 2)
        self.check('ap dec 4', 3)

        self.check('ap dec 1024', 1023)

        self.check('ap dec 0', -1)
        self.check('ap dec -1', -2)
        self.check('ap dec -2', -3)

    def test_07_Sum(self):
        self.check('ap ap add 1 2', 3)
        self.check('ap ap add 2 1', 3)
        self.check('ap ap add 0 1', 1)
        self.check('ap ap add 2 3', 5)
        self.check('ap ap add 3 5', 8)

    def test_08_Variables(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 1100)
        self.vm.bind(2, 1200)
        self.check('ap ap add 0 x0', 1000)
        self.check('ap ap add 0 x1', 1100)
        self.check('ap ap add 0 x2', 1200)
        self.check('ap ap add x0 0', 1000)
        self.check('ap ap add x1 0', 1100)
        self.check('ap ap add x2 0', 1200)
        self.check('ap ap add x0 x1', 2100)
        self.check('ap ap add x1 x0', 2100)

    def test_09_Product(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 2000)
        self.check('ap ap mul 4 2', 8)
        self.check('ap ap mul 3 4', 12)
        self.check('ap ap mul 3 -2', -6)
        self.check('ap ap mul x0 x1', 1000 * 2000)
        self.check('ap ap mul x0 0', 0)
        self.check('ap ap mul x0 1', 1000)

    def test_10_Integer_Division(self):
        self.vm.bind(0, 1000)
        self.check('ap ap div 4 2', 2)
        self.check('ap ap div 4 3', 1)
        self.check('ap ap div 4 4', 1)
        self.check('ap ap div 4 5', 0)
        self.check('ap ap div 5 2', 2)
        self.check('ap ap div 6 -2', -3)
        self.check('ap ap div 5 -3', -1)
        self.check('ap ap div -5 3', -1)
        self.check('ap ap div -5 -3', 1)
        self.check('ap ap div x0 1', 1000)

    def test_11_Equality_and_Booleans(self):
        self.vm.bind(0, 1000)
        self.check('ap ap eq x0 x0', 't')
        self.check('ap ap eq 0 -2', 'f')
        self.check('ap ap eq 0 -1', 'f')
        self.check('ap ap eq 0 0', 't')
        self.check('ap ap eq 0 1', 'f')
        self.check('ap ap eq 0 2', 'f')

        self.check('ap ap eq 1 -1', 'f')
        self.check('ap ap eq 1 0', 'f')
        self.check('ap ap eq 1 1', 't')
        self.check('ap ap eq 1 2', 'f')
        self.check('ap ap eq 1 3', 'f')

        self.check('ap ap eq 2 0', 'f')
        self.check('ap ap eq 2 1', 'f')
        self.check('ap ap eq 2 2', 't')
        self.check('ap ap eq 2 3', 'f')
        self.check('ap ap eq 2 4', 'f')

        self.check('ap ap eq 19 20', 'f')
        self.check('ap ap eq 20 20', 't')
        self.check('ap ap eq 21 20', 'f')

        self.check('ap ap eq -19 -20', 'f')
        self.check('ap ap eq -20 -20', 't')
        self.check('ap ap eq -21 -20', 'f')

    def test_12_Strict_Less_Than(self):
        self.check('ap ap lt 0 -1', 'f')
        self.check('ap ap lt 0 0', 'f')
        self.check('ap ap lt 0 1', 't')
        self.check('ap ap lt 0 2', 't')

        self.check('ap ap lt 1 0', 'f')
        self.check('ap ap lt 1 1', 'f')
        self.check('ap ap lt 1 2', 't')
        self.check('ap ap lt 1 3', 't')

        self.check('ap ap lt 2 1', 'f')
        self.check('ap ap lt 2 2', 'f')
        self.check('ap ap lt 2 3', 't')
        self.check('ap ap lt 2 4', 't')

        self.check('ap ap lt 19 20', 't')
        self.check('ap ap lt 20 20', 'f')
        self.check('ap ap lt 21 20', 'f')

        self.check('ap ap lt -19 -20', 'f')
        self.check('ap ap lt -20 -20', 'f')
        self.check('ap ap lt -21 -20', 't')

    @skip
    def test_13(self):
        pass

    @skip
    def test_14(self):
        pass

    @skip
    def test_15(self):
        pass

    def test_16_Negate(self):
        self.check('ap neg 0', 0)
        self.check('ap neg 1', -1)
        self.check('ap neg -1', 1)
        self.check('ap neg 2', -2)
        self.check('ap neg -2', 2)

    def test_17_Function_Application(self):
        self.vm.bind(0, 1000)
        self.check('ap inc ap inc 0', 2)
        self.check('ap inc ap inc ap inc 0', 3)
        self.check('ap inc ap dec x0', 1000)
        self.check('ap dec ap inc x0', 1000)
        self.check('ap dec ap ap add x0 1', 1000)
        self.check('ap ap add ap ap add 2 3 4', 9)
        self.check('ap ap add 2 ap ap add 3 4', 9)
        self.check('ap ap add ap ap mul 2 3 4', 10)
        self.check('ap ap mul 2 ap ap add 3 4', 14)
        # inc   =   ap add 1
        # dec   =   ap add ap neg 1

    def test_18_S_Combinator(self):
        self.check('ap ap ap s add inc 1', 3)
        self.check('ap ap ap s mul ap add 1 6', 42)

    def test_19_C_Combinator(self):
        self.check('ap ap ap c add 1 2', 3)

    def test_20_B_Combinator(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 1100)
        self.vm.bind(2, 1200)
        self.check('ap ap ap b x0 x1 x2', (1000, [(1100, [1200])]))
        self.check('ap ap ap b inc dec x0', 1000)

    def test_21_True__K_Combinator(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 2000)
        self.check('ap ap t x0 x1', 1000)
        self.check('ap ap t 1 5', 1)
        self.check('ap ap t t i', 't')
        self.check('ap ap t t ap inc 5', 't')
        self.check('ap ap t ap inc 5 t', 6)

    def test_22_False(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 2000)
        self.check('ap ap f x0 x1', 2000)
        # self.check('ap s t', 'f')

    def test_23_Power_of_Two(self):
        self.check('ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 0', 1)
        self.check('ap ap ap ap c ap eq 0 1 0 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0', 1)
        self.check('ap ap ap ap eq 0 0 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0', 1)
        self.check('ap ap t 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 0', 1)

        self.check('ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap ap ap c ap eq 0 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap ap ap eq 0 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap f 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap ap b pwr2 ap add -1 1', 2)
        self.check('ap ap mul 2 ap pwr2 ap ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap ap ap c ap eq 0 1 ap ap add -1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap ap ap eq 0 ap ap add -1 1 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap ap ap eq 0 0 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1', 2)
        self.check('ap ap mul 2 ap ap t 1 ap ap ap b ap mul 2 ap ap b pwr2 ap add -1 ap ap add -1 1', 2)
        self.check('ap ap mul 2 1', 2)

        self.check('ap ap ap s ap ap c ap eq 0 1 ap ap b ap mul 2 ap ap b pwr2 ap add -1 2', 4)

        self.check('ap pwr2 0', 1)
        self.check('ap pwr2 1', 2)
        self.check('ap pwr2 2', 4)
        self.check('ap pwr2 3', 8)
        self.check('ap pwr2 4', 16)
        self.check('ap pwr2 5', 32)
        self.check('ap pwr2 6', 64)
        self.check('ap pwr2 7', 128)
        self.check('ap pwr2 8', 256)

    def test_24_I_Combinator(self):
        self.vm.bind(0, 1000)
        self.check('ap i x0', 1000)
        self.check('ap i 1', 1)
        self.check('ap i i', 'i')
        self.check('ap i add', 'add')
        self.check('ap i ap add 1', ('add', [1]))

    @skip
    def test_25_Cons__or_Pair(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 1100)
        self.vm.bind(2, 1200)
        self.check('ap ap ap cons x0 x1 x2', ((1200, [1000]), [1100]))

    def test_26_Car__First(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 1100)
        self.vm.bind(2, 1200)
        self.check('ap car ap ap cons x0 x1', 1000)
        self.check('ap car x2', (1200, ['t']))

    def test_27_Cdr__Tail(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 1100)
        self.vm.bind(2, 1200)
        self.check('ap cdr ap ap cons x0 x1', 1100)
        self.check('ap cdr x2', (1200, ['f']))

    def test_28_Nil__Empty_List(self):
        self.check('ap nil x0', 't')

    def test_29_Is_Nil__Is_Empty_List(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 2000)
        self.check('ap isnil nil', 't')
        self.check('ap isnil ap ap cons x0 x1', 'f')

    @skip
    def test_30(self):
        pass

    @skip
    def test_31(self):
        pass

    @skip
    def test_32(self):
        pass

    @skip
    def test_33(self):
        pass

    @skip
    def test_34(self):
        pass

    @skip
    def test_35(self):
        pass

    @skip
    def test_36(self):
        pass

    def test_37_Is_0(self):
        self.vm.bind(0, 1000)
        self.vm.bind(1, 2000)
        self.check('ap ap ap if0 0 x0 x1', 1000)
        self.check('ap ap ap if0 1 x0 x1', 2000)

    @skip
    def test_38(self):
        pass

    @skip
    def test_39(self):
        pass

    @skip
    def test_40(self):
        pass

    @skip
    def test_41(self):
        pass

    @skip
    def test_42(self):
        pass
