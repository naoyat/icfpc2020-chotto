import numpy as np
import sys


def pp_rows(rows):
    def conv(row):
        return ''.join("#" if c==1 else '.' for c in row)

    for row in rows:
        print(conv(row))


def pp_cols(cols):
    height = len(cols)
    width = len(cols[0])
    rows = [ [cols[r][c] for r in range(height) ] for c in range(width)]
    pp_rows(rows)


def read_number(chunk, W, H):
    # print('read_number. W=%d H=%d, %d' % (W, H, chunk[0][0]))
    assert chunk[0][0] == 0
    assert H >= 2 and W >= 2
    assert H == W or H == W+1

    for r in range(1,H):
        if chunk[0][r] == 0:
            return None
    for c in range(1,W):
        if chunk[c][0] == 0:
            return None

    val = 0
    m = 1
    for r in range(1,H):
        for c in range(1,W):
            val += m * chunk[c][r]
            m *= 2

    if H == W+1:
        # Negative Number
        val = -val

    return val


def is_bordered(chunk):
    W = len(chunk)
    H = len(chunk[0])
    for c in range(W):
        if chunk[c][0] == 0: return False
        if chunk[c][-1] == 0: return False
    for r in range(H):
        if chunk[0][r] == 0: return False
        if chunk[-1][r] == 0: return False
    return True


def unwrap_border(chunk):
    W = len(chunk)
    H = len(chunk[0])
    inside = []
    for c in range(1,W-1):
        col = [1-v for v in chunk[c][1:-1]]
        inside.append(col)
    assert len(inside) == len(chunk) - 2
    assert len(inside[0]) == len(chunk[0]) - 2
    return inside


def read_chunk(chunk, height):
    W = len(chunk)
    H = len(chunk[0])
    assert H >= height
    if H > height:
        for c in range(W):
            chunk[c] = chunk[c][:height]
        H = height

    # print(' read_chunk(%dx%d)' % (H, W))
    # pp_cols(chunk)

    if W <= 1:
        return None

    if chunk[0][0] == 0 and (H == W or H == W+1):
        v = read_number(chunk, W, H)
        if v is not None:
            return v

    if H == W == 2:
        if chunk == [[1,1], [1,0]]:
            return 'ap'
        elif chunk == [[1,1], [1,1]]:
            return 'i'  #24. I Combinator

    if H == W == 3 and chunk[0] == [1,1,1] and chunk[1][0] == chunk[2][0] == 1:
        if chunk == [[1,1,1], [1,0,1], [1,0,1]]:
            return '='  #4. Equality
        elif chunk == [[1,1,1], [1,0,0], [1,1,0]]:
            return 't'  #11. Booleans / #21. True (K Combinator)
        elif chunk == [[1,1,1], [1,0,0], [1,0,1]]:
            return 'f'  #11. Booleans / #22. False
        elif chunk == [[1,1,1], [1,0,0], [1,1,1]]:
            return 'neg'  #16. Negate
        elif chunk == [[1,1,1], [1,1,1], [1,1,0]]:
            return 's'  #18. S Combinator
        elif chunk == [[1,1,1], [1,0,1], [1,1,0]]:
            return 'c'  #19. C Combinator
        elif chunk == [[1,1,1], [1,1,1], [1,0,0]]:
            return 'b'  #19. B Combinator
        elif chunk == [[1,1,1], [1,0,1], [1,1,1]]:
            return 'nil'  #28. Nil (Empty List)
        elif chunk == [[1,1,1], [1,1,1], [1,1,1]]:
            return 'isnil'  #29. Is Nil (Is Empty List)

    if H == 5 and W == 3:
        if chunk == [[0,0,1,0,0], [0,1,1,1,0], [1,1,1,1,1]]:
            return '('  #30. List Construction Syntax
        elif chunk == [[1,1,1,1,1], [0,1,1,1,0], [0,0,1,0,0]]:
            return ')'  #30.

    if H == 5 and W == 2:
        if chunk == [[1,1,1,1,1], [1,1,1,1,1]]:
            return ','  #30.

    if H == W == 4 and chunk[0] == [1,1,1,1] and chunk[1][0] == chunk[2][0] == chunk[3][0] == 1:
        if chunk == [[1,1,1,1], [1,1,0,0], [1,0,0,1], [1,0,1,1]]:
            return 'inc'  #5. Successor
        elif chunk == [[1,1,1,1], [1,1,0,0], [1,0,1,1], [1,0,0,1]]:
            return 'dec'  #6. Predecessor
        elif chunk == [[1,1,1,1], [1,1,1,1], [1,0,0,0], [1,1,1,1]]:
            return 'add'  #7. Sum
        elif chunk == [[1,1,1,1], [1,0,0,0], [1,1,1,1], [1,0,0,0]]:
            return 'mul'  #9. Product
        elif chunk == [[1,1,1,1], [1,0,1,0], [1,0,0,0], [1,0,1,0]]:
            return 'div'  #10. Integer Division
        elif chunk == [[1,1,1,1], [1,0,0,1], [1,0,0,1], [1,0,0,1]]:
            return 'eq'  #11. Equality
        elif chunk == [[1,1,1,1], [1,0,0,0], [1,0,0,1], [1,0,1,1]]:
            return 'lt'  #12. Strict Less-Than
        elif chunk == [[1,1,1,1], [1,0,1,0], [1,1,0,1], [1,0,1,0]]:
            return 'mod'  #13. Modulate
        elif chunk == [[1,1,1,1], [1,1,0,1], [1,0,1,0], [1,1,0,1]]:
            return 'dem'  #14. Demodulate
        elif chunk == [[1,1,1,1], [1,0,1,0], [1,1,0,1], [1,1,1,0]]:
            return 'send'  #15. Send

    if H == W == 5:
        if chunk == [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1]]:
            return 'cons'  #25. Cons (or Pair)
        elif chunk == [[1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1], [1,1,0,0,1], [1,1,1,1,1]]:
            return 'car'  #26. Car (First)
        elif chunk == [[1,1,1,1,1], [1,1,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,1,1,1,1]]:
            return 'cdr'  #27. Cdr (Tail)

        elif chunk == [[1,1,1,1,1], [1,0,0,1,0], [1,0,1,1,1], [1,0,1,0,1], [1,0,1,0,1]]:
            return 'if0'  #37. Is 0

    if H == W == 6:
        if chunk == [[1,1,1,1,1,1], [1,1,0,0,0,0], [1,0,1,0,0,0], [1,0,0,1,0,0], [1,0,0,0,1,0], [1,0,0,0,0,1]]:
            return 'vec'  #31. Vector
        elif chunk == [[1,1,1,1,1,1], [1,0,0,0,0,1], [1,0,0,0,0,1], [1,0,0,0,0,1], [1,0,0,0,0,1], [1,1,1,1,1,1]]:
            return 'draw'  #32. Draw
        elif chunk == [[1,1,1,1,1,1], [1,0,1,0,1,0], [1,1,0,1,0,1], [1,0,1,0,1,0], [1,1,0,1,0,1], [1,0,1,0,1,0]]:
            return 'checkerboard'  #33. Checkerboard
        elif chunk == [[1,1,1,1,1,1], [1,0,0,0,0,1], [1,0,1,1,0,1], [1,0,1,1,0,1], [1,0,0,0,0,1], [1,1,1,1,1,1]]:
            return 'interact'  #38. Interact
        elif chunk == [[1,1,1,1,1,1], [1,0,0,0,1,0], [1,0,0,0,0,1], [1,0,0,0,0,1], [1,0,0,0,1,0], [1,0,0,0,1,0]]:
            return 'modem'
        elif chunk == [[1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,0], [1,1,1,1,0,0], [1,1,1,0,0,0], [1,1,0,0,1,0]]:
            return ':1678847'
        elif chunk == [[1,1,1,1,1,1], [1,0,0,1,0,1], [1,1,1,1,0,1], [1,0,1,1,1,1], [1,0,1,0,0,1], [1,1,1,1,1,1]]:
            return 'f38'

    if H == W == 7:
        if chunk == [[1,1,1,1,1,1,1], [1,0,0,1,0,0,1], [1,0,0,1,0,0,1], [1,1,1,1,1,1,1], [1,0,0,1,0,0,1], [1,0,0,1,0,0,1], [1,1,1,1,1,1,1]]:
            return 'multipledraw'
        elif chunk == [[1,1,1,1,1,1,1], [1,0,0,0,0,0,0], [1,0,0,0,0,1,0], [1,0,0,0,0,0,0], [1,0,0,0,0,0,0], [1,1,0,0,0,0,0], [1,0,0,0,0,0,0]]:
            return 'statelessdraw'
        elif chunk == [[1,1,1,1,1,1,1], [1,1,1,0,0,0,0], [1,0,0,0,0,0,0], [1,0,0,0,0,1,0], [1,0,0,0,0,0,0], [1,0,0,0,0,0,0], [1,0,0,0,0,0,0]]:
            return ':67108929'
        elif chunk == [[0,0,0,1,1,0,0], [0,0,1,0,0,1,0], [1,0,1,1,0,0,1], [1,0,1,0,1,0,1], [1,0,0,1,1,0,1], [0,1,0,0,1,0,0], [0,0,1,1,0,0,0]]:
            return 'galaxy'
        elif chunk == [[0,0,0,0,0,1,0], [0,0,0,0,0,1,0], [1,1,1,1,1,1,0], [0,0,1,1,1,1,1], [1,1,1,1,1,1,0], [0,0,0,0,0,1,0], [0,0,0,0,0,1,0]]:
            return 'humans'
        elif chunk == [[0,0,0,1,1,0,1], [0,1,1,1,1,1,0], [0,1,0,0,0,1,1], [1,1,0,0,1,1,0], [0,1,0,0,0,1,1], [0,1,1,1,1,1,0], [0,0,0,1,1,0,1]]:
            return 'aliens'

    if H == W and H >= 4 and is_bordered(chunk):
        # sys.stderr.write('[%d x %d, bordered]\n' % (H, W))
        #8. Variables
        # unwrap border
        inside = unwrap_border(chunk)

        if H >= 6 and is_bordered(inside):
            ininside = unwrap_border(inside)
            v = read_chunk(ininside, H-4)
            if v is not None:
                return 'pwr%s' % v

        v = read_chunk(inside, H-2)
        if v is not None:
            return 'x%s' % v

    return None


def read_bunch(bunch, ignore_unknown=True):
    # print('')
    # print('read_bunch')
    # pp_rows(bunch)

    W = len(bunch)
    if W == 0:
        return []

    L = len(bunch[0])
    res = []
    chunk = []
    height = 0
    for c in range(L):
        col = []
        for r in range(W):
            b = bunch[r][c]
            col.append(b)
            if b > 0 and r+1 > height:
                height = r+1
        s = sum(col)
        if s == 0:  # empty
            if chunk:
                res.append( read_chunk(chunk, height) )
                chunk = []
                height = 0
        else:
            chunk.append(col)
    if chunk:
        res.append( read_chunk(chunk, height) )

    if ignore_unknown:
        res = [item for item in res if item is not None]

    return res


def parse(rows):
    # print(rows)
    R = len(rows)
    res = []
    bunch = []
    for i in range(R):
        s = sum(rows[i])
        if s == 0: # empty
            if bunch:
                res.append(read_bunch(bunch))
                bunch = []
        else:
            bunch.append( rows[i] )
    if bunch:
        res.append(read_bunch(bunch))
    return res


def parse_data(d):
    H, W = d.shape
    rows = [d[r, 1:-1] for r in range(1, H - 1)]
    return parse(rows)

#p = parse(sr.rows)
# sr.show(p) #print(p)
#for row in p:
#    print(sr.conv(row))
#print(p)