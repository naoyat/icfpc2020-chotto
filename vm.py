
import sys
import os
import re
import click
from traceback import print_exception


def is_reg(token):
    # return isinstance(token, tuple) and token[0] == 'x'
    return isinstance(token, str) and token.startswith(':')


class ConsCell :
    def __init__(self, car, cdr):
        self.first = car
        self.rest = cdr

    def car(self):
        return self.first

    def cdr(self):
        return self.rest

    def repr_sub(self):
        # if isinstance(self.first, tuple):
        #     s = str(self.first)
        # else:
        try:
            s = '%s' % str(self.first)
        except Exception:
            s = '?%s?' % type(self.first)
        # if len(s) > 20:
        #     return s + ' ...'

        # if isinstance(self.rest, tuple):
        #     s += ' . %s' % str(self.rest)
        if isinstance(self.rest, ConsCell):
            s += ' ' + self.rest.repr_sub()
        elif self.rest == 'nil':
            pass
        else:
            s += ' . %s' % str(self.rest)
        return s

    def __repr__(self):
        return '(' + self.repr_sub() + ')'


FnInc = lambda x: x+1  #5. Successor
FnDec = lambda x: x-1  #6. Predecessor

#def FnSum2(x):
#    return lambda y: x+y

FnAdd = lambda x: lambda y:x+y  #7. Sum

FnMul = lambda x: lambda y:x*y  #9. Product

def intdiv(x, y):
    sgn = 1
    if x < 0:
        sgn = -sgn
        x = -x
    if y < 0:
        sgn = -sgn
        y = -y
    return (x // y) * sgn

FnDiv = lambda x: sys.stdout.write('[DIV1]') and (lambda y: sys.stdout.write('[DIV]') and intdiv(x,y))  #10. Integer Division

FnTrue = lambda x: lambda y: x  #21. True (K Combinator)
FnFalse = lambda x: lambda y: y  #22 False

FnEq = lambda x: lambda y:FnTrue if x==y else FnFalse  #11. Equality and Booleans
FnLt = lambda x: lambda y:FnTrue if x<y else FnFalse  #12. Strict Less-Than
FnMod = lambda x: [x]  #13. Modulate
FnDem = lambda x: x[0]  #14. Demodulate

#15

FnNeg = lambda x: -x  #16. Negate

FnAp = lambda f: lambda a: f(a)  #17. Function Application

FnSCombinator = lambda x: lambda y: lambda z: x(z)(y(z))  #18. S Combinator
FnCCombinator = lambda x: lambda y: lambda z: x(z)(y)  #19. C Combinator
FnBCombinator = lambda x: lambda y: lambda z: x(y(z))  #20. B Combinator

FnPwr2 = lambda x: 2**x  #23. Power of Two
FnICombinator = lambda x: x  #24. I Combinator

FnCons = lambda x: lambda y: ConsCell(x,y)  #25. Cons (or Pair)
FnCar = lambda x: x.car() if isinstance(x,ConsCell) else x(FnTrue)  #26. Car (First)
FnCdr = lambda x: x.cdr() if isinstance(x,ConsCell) else x(FnFalse)  #27. Cdr (Tail)

FnNil = lambda x: FnTrue  #28. Nil (Empty List)

FnIsNil = lambda x: FnTrue if x==FnNil else FnFalse  #29. Is Nil (Is Empty List)
FnIf0 = lambda x: FnTrue if x==0 else FnFalse  #37. Is 0



def is_function(x):
    return type(x) is type(FnAp)


# def tokenize(line):
#     tokens = []
#     for token in line.split(' '):
#         tokens.append(token)
#     return tokens


def translate(token):
    try:
        if isinstance(token, int):
            pass
        elif token[0] in ':x':
            token = ':' + token[1:]
            # token = ('x', int(token[1:]))
        elif token[0] in '-0123456789':
            token = int(token)
        elif token == 'galaxy':
            token = ':galaxy'

        elif token == 'inc':
            token = FnInc
        elif token == 'dec':
            token = FnDec
        elif token == 'add':
            token = FnAdd
        elif token == 'mul':
            token = FnMul
        elif token == 'div':
            token = FnDiv
        elif token == 't':
            token = FnTrue
        elif token == 'f':
            token = FnFalse
        elif token == 'eq':
            token = FnEq
        elif token == 'lt':
            token = FnLt
        elif token == 'mod':
            token = FnMod
        elif token == 'dem':
            token = FnDem
        elif token == 'neg':
            token = FnNeg
        # elif token == 'ap':
        #     token = FnAp
        elif token == 's':
            token = FnSCombinator
        elif token == 'c':
            token = FnCCombinator
        elif token == 'b':
            token = FnBCombinator
        elif token == 'pwr2':
            token = FnPwr2
        elif token == 'i':
            token = FnICombinator
        elif token == 'cons':
            token = FnCons
        elif token == 'car':
            token = FnCar
        elif token == 'cdr':
            token = FnCdr
        elif token == 'nil':
            token = FnNil
        elif token == 'isnil':
            token = FnIsNil
        elif token == 'if0':
            token = FnIf0
        else:
            pass
    except Exception:
        pass
    return token


class VM:
    def __init__(self):
        self.reg = {}

    def load(self, src):
        self.code = []
        with open(src, 'r') as fp:
            for row in fp:
                row = row.rstrip()
                self.code.append(row)
                # e = evaluate(tokens)
                # print(e)

    def bind(self, reg, val):
        if isinstance(reg, int):
            reg = ':%d' % reg
        self.reg[reg] = val
        return val  # just for debug

    def define(self, reg, uneval):
        self.reg[reg] = ('thunk', uneval)
        return uneval  # just for debug

    # def apply(self, op, arg, verbose=False):
    #     if is_function(op):
    #         return op(arg)
    #     elif op is None:
    #         if verbose: print('op is None')
    #         return None
    #     else:
    #         if verbose: print('Unknown op; %s | %s' % (op, arg))
    #         # return ('?', [op, arg])
    #         return (op, [arg])

    def eval(self, tokens, ix=0, verbose=False):
        if ix == len(tokens):
            return (None, ix)

        head = translate(tokens[ix])
        if verbose: print('EVAL #%d %s...' % (ix, head))
        if is_reg(head):
            reg = head
            # reg_id = tokens[ix][1]
            if len(tokens)-ix >= 3 and tokens[ix+1] == '=':
                # let reg = evaluated rest
                val, next = self.eval(tokens, ix+2, verbose=verbose)
                return (self.bind(reg, val), next)
                # self.define(reg, tokens[ix+2:])
                # return ('def<%s>' % reg, len(tokens))
            else:
                val = self.reg.get(reg, FnNil)  #'undef<%s>' % reg)
                if verbose: print('  reg<%s> =' % reg, val)
                if isinstance(val, tuple) and val[0] == 'thunk':
                    # if verbose:
                    # if verbose: print('  evaluate thunk<%s>=%s' % (reg, val[1]))
                    print('[EVAL %s]' % reg)
                    self.reg[reg] = 'rec<%s>' % reg
                    val, _ = self.eval(val[1], 0, verbose=verbose)
                    self.reg[reg] = val
                return (val, ix+1)
        elif head == 'ap':  #is_function(head):
            op, next = self.eval(tokens, ix+1, verbose=verbose)
            arg, next = self.eval(tokens, next, verbose=verbose)
            if verbose: print('apply', op, arg)
            return op(arg), next
        else:
            return (head, ix+1)

    def eval__(self, tokens, verbose=False):
        L = len(tokens)

        val = FnICombinator

        till = 0
        for ix, head in enumerate(tokens):
            if isinstance(head, int):
                return head, ix+1
            elif is_reg(head):
                reg = head
                # reg_id = tokens[ix][1]
                if len(tokens)-ix >= 3 and tokens[ix+1] == '=':
                    # let reg = evaluated rest
                    # val, next = self.eval(tokens, ix+2, verbose=verbose)
                    # return (self.bind(reg, val), next)
                    self.define(reg, tokens[ix+2:])
                    return ('def<%s>' % reg, len(tokens))
                else:
                    val = self.reg.get(reg, 'undef<%s>' % reg)
                    if verbose: print('  reg<%s> =' % reg, val)
                    if isinstance(val, tuple) and val[0] == 'thunk':
                        # if verbose:
                        # if verbose: print('  evaluate thunk<%s>=%s' % (reg, val[1]))
                        print('[EVAL %s]' % reg)
                        self.reg[reg] = 'rec<%s>' % reg
                        val, _ = self.eval(val[1], 0, verbose=verbose)
                        self.reg[reg] = val
                    return (val, ix+1)
            elif head == FnAp:  #is_function(head):
                op, next = self.eval(tokens, ix+1, verbose=verbose)
                return head(op), next
            else:
                return (head, ix+1)

    def run(self, verbose=False):
        for line_no, line in enumerate(self.code, start=1):
            print('LINE %d:' % line_no)
            print('   ', line)
            tokens = line.split(' ')
            if verbose:
                print('  =', tokens)
                translated_tokens = [translate(token) for token in tokens]
                print('  =', translated_tokens)
            try:
                e, _ix = self.eval(tokens, verbose=verbose)
                print('  =', e)
            except Exception:
                type, value, tb = sys.exc_info()
                print('  =>', 'ERROR')
                print_exception(type, value, tb, file=sys.stdout)
            print()

        # print('reg:', self.reg)
        if verbose:
            for k, v in self.reg.items():
                print('\t', k, ':', v)


@click.command()
@click.option('-s', '--src', type=click.Path(), default='galaxy.txt')
@click.option('-e', '--eval', type=str, required=False)
@click.option('-v', '--verbose', is_flag=True, default=False)
def main(src, eval, verbose):
    sys.setrecursionlimit(20000)

    vm = VM()
    if eval:
        tokens = eval.split(' ')
        if verbose: print(tokens)
        v, _ = vm.eval(tokens, verbose=verbose)
        print(v)
    else:
        vm.load(src)
        vm.run()
        v, _ = vm.eval([':galaxy'], verbose=verbose)
        print('galaxy =', v)


if __name__ == '__main__':
    main()
