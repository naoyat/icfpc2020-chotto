
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


def tokenize(line):
    tokens = []
    for token in line.split(' '):
        t = token[0]
        try:
            # if t == 't':
            #     token = True
            # elif t == 'f':
            #     token = False
            if t == ':' or t == 'x':
                token = ':' + token[1:]
                # token = ('x', int(token[1:]))
            elif t == '-' or t in '0123456789':
                token = int(token)
            elif t == 'g' and token == 'galaxy':
                token = ':galaxy'
            else:
                pass
        except Exception:
            pass
        tokens.append(token)
    return tokens


class VM :
    def __init__(self):
        self.reg = {}

    def load(self, src):
        self.code = []
        with open(src, 'r') as fp:
            for row in fp:
                row = row.rstrip()
                # tokens = tokenize(row)
                self.code.append(row)
                # e = evaluate(tokens)
                # print(e)

    def bind(self, reg, val):
        self.reg[reg] = val
        return val  # just for debug

    def define(self, reg, uneval):
        self.reg[reg] = ('thunk', uneval)
        return uneval  # just for debug

    # b, c, s が未実装
    def apply(self, op, arg, verbose=False):
        if isinstance(op, str):
            if op == 'neg':
                return -arg
            elif op == 'inc':
                return arg + 1
            elif op == 'dec':
                return arg - 1
            elif op == 'pwr2':
                return 2 ** arg

            if op == 'nil':
                return 't'  # for any arg
            if op == 'isnil':
                return 't' if arg == 'nil' else 'f'

            if op == 'if0':
                return 't' if arg == 0 else 'f'

            if op == 'car':
                if isinstance(arg, ConsCell):
                    return arg.car()
                else:
                    return self.apply(arg, 't')  # ap car x2 = ap x2 t
            elif op == 'cdr':
                if isinstance(arg, ConsCell):
                    return arg.cdr()
                else:
                    return self.apply(arg, 'f')  # ap cdr x2 = ap x2 f

            if op == 'i':
                if verbose: print('** I Combinator, 0=%s' % (arg,))
                return arg

            if op == 's' and arg == 't':
                return 'f'

            return (op, [arg])
            # if op == 'cons':
            #     return ('cons', arg)
        elif isinstance(op, tuple):  # (op0, [args])
            assert len(op) == 2 and isinstance(op[1], list)
            op0 = op[0]
            args = op[1] + [arg]
            if len(args) == 2:
                x, y = args
                if op0 == 'cons':
                    return ConsCell(x, y)
                elif op0 == 'add':
                    if type(x) is int and type(y) is int:
                        return x + y
                    else:
                        if verbose: print('add %s %s; operands must be int' % (x, y))
                        return 0
                elif op0 == 'mul':
                    if type(x) is int and type(y) is int:
                        return x * y
                    else:
                        if verbose: print('mul %s %s; operands must be int' % (x, y))
                        return 0
                elif op0 == 'div':
                    if type(x) is int and type(y) is int:
                        pm = 1
                        if x < 0:
                            pm = -pm
                            x = -x
                        if y < 0:
                            pm = -pm
                            y = -y
                        return (x // y) * pm
                    else:
                        if verbose: print('div %s %s; operands must be int' % (x, y))
                        return 0
                elif op0 == 'lt':
                    if type(x) is int and type(y) is int:
                        return 't' if x < y else 'f'
                    else:
                        if verbose: print('lt %s %s; operands must be int' % (x, y))
                        return 'f'
                elif op0 == 'eq':
                    return 't' if x == y else 'f'
                elif op0 == 't':  # K x y = x
                    if verbose: print('** K Combinator, 0=%s | 1=%s' % (x, y))
                    return x
                elif op0 == 'f':  # f x y = y
                    if verbose: print('** False., 0=%s | 1=%s' % (x, y))
                    return y

            if len(args) == 3:
                x, y, z = args
                if op0 == 's':  # S x y z = ((x z) (y z))
                    if verbose: print('** S Combinator, 0=%s | 1=%s | 2=%s' % (x, y, z))
                    return self.apply(self.apply(x,z), self.apply(y,z))
                elif op0 == 'c':  # C x y z = x z y
                    if verbose: print('** C Combinator, 0=%s | 1=%s | 2=%s' % (x, y, z))
                    # return self.apply(self.apply(x,z), y)
                    return self.apply((x, [z]), y)
                elif op0 == 'b':  # B x y z = x (y z)
                    if verbose: print('** B Combinator, 0=%s | 1=%s | 2=%s' % (x, y, z))
                    return self.apply(x, self.apply(y, z))
                elif op0 == 'if0':  # if0 x y z = (x == 0 ? y : z)
                    return y if x == 0 else z

            return (op0, args)
        elif op is None:
            if verbose: print('op is None')
            return None
        else:
            if verbose: print('Unknown op; %s | %s' % (op, arg))
            # return ('?', [op, arg])
            return (op, [arg])

    def eval(self, tokens, ix=0, verbose=False):
        if ix == len(tokens):
            return (None, ix)

        head = tokens[ix]
        if is_reg(head):
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
        elif head == 'ap':
            if verbose: print('  ap at ix=%d ...' % (ix,))# tokens[ix+1:]))
            op, next = self.eval(tokens, ix+1, verbose=verbose)
            if verbose: print('    op=%s; next=%d ...' % (op, next))#, tokens[next:]))
            arg, next = self.eval(tokens, next, verbose=verbose)
            if verbose: print('    arg=%s; next=%d ...' % (arg, next))#, tokens[next:]))
            val = self.apply(op, arg, verbose=verbose)
            if verbose: print('    apply %s %s -> val=%s' % (op, arg, val))
            return (val, next)
        else:
            return (head, ix+1)

    def run(self, verbose=False):
        for line_no, line in enumerate(self.code, start=1):
            print('LINE %d:' % line_no)
            print('   ', line)
            tokens = tokenize(line)
            if verbose: print('  =', tokens)
            try:
                e, _ix = self.eval(tokens, 0, verbose=verbose)
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
def main(src, eval):
    sys.setrecursionlimit(20000)

    vm = VM()
    if eval:
        tokens = tokenize(eval)
        v, _ = vm.eval(tokens)
        print(v)
    else:
        vm.load(src)
        vm.run()
        v, _ = vm.eval([':galaxy'])
        print('galaxy =', v)


if __name__ == '__main__':
    main()
