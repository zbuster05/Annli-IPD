from __future__ import division

_expr_codes = [
    'POP_TOP','ROT_TWO','ROT_THREE','ROT_FOUR','DUP_TOP',
    'BUILD_LIST','BUILD_MAP','BUILD_TUPLE','BUILD_SET',
    'BUILD_CONST_KEY_MAP', 'BUILD_STRING',
    'LOAD_CONST','RETURN_VALUE','STORE_SUBSCR', 'STORE_MAP',
    'LIST_TO_TUPLE', 'LIST_EXTEND', 'SET_UPDATE', 'DICT_UPDATE', 'DICT_MERGE',
    'COPY', 'RESUME', 'UNARY_POSITIVE','UNARY_NEGATIVE','UNARY_NOT',
    'UNARY_INVERT','BINARY_POWER','BINARY_MULTIPLY',
    'BINARY_DIVIDE','BINARY_FLOOR_DIVIDE','BINARY_TRUE_DIVIDE',
    'BINARY_MODULO','BINARY_ADD','BINARY_SUBTRACT',
    'BINARY_LSHIFT','BINARY_RSHIFT','BINARY_AND','BINARY_XOR',
    'BINARY_OR',
    'BINARY_OP',
    'MAKE_FUNCTION',
    'STORE_NAME',
    'LOAD_NAME',
    # 'CALL_FUNCTION',
]

_values_codes = _expr_codes + ['LOAD_NAME']

import six

def _get_opcodes(codeobj):
    """_get_opcodes(codeobj) -> [opcodes]
    Extract the actual opcodes as a list from a code object
    >>> c = compile("[1 + 2, (1,2)]", "", "eval")
    >>> _get_opcodes(c)
    [100, 100, 103, 83]
    """
    import dis
    if hasattr(dis, 'get_instructions'):
        return [ins.opcode for ins in dis.get_instructions(codeobj)]
    i = 0
    opcodes = []
    s = codeobj.co_code
    while i < len(s):
        code = six.indexbytes(s, i)
        opcodes.append(code)
        if code >= dis.HAVE_ARGUMENT:
            i += 3
        else:
            i += 1
    return opcodes

def test_expr(expr, allowed_codes):
    """test_expr(expr, allowed_codes) -> codeobj
    Test that the expression contains only the listed opcodes.
    If the expression is valid and contains only allowed codes,
    return the compiled code object. Otherwise raise a ValueError
    """
    import dis
    allowed_codes = [dis.opmap[c] for c in allowed_codes if c in dis.opmap]
    try:
        c = compile(expr, "", "exec")
    except SyntaxError:
        raise ValueError("%r is not a valid expression" % expr)
    codes = _get_opcodes(c)
    for code in codes:
        if code not in allowed_codes:
            raise ValueError("opcode %s not allowed" % dis.opname[code])
    return c

def const(expr):
    """const(expression) -> value
    Safe Python constant evaluation
    Evaluates a string that contains an expression describing
    a Python constant. Strings that are not valid Python expressions
    or that contain other code besides the constant raise ValueError.
    Examples:
        >>> const("10")
        10
        >>> const("[1,2, (3,4), {'foo':'bar'}]")
        [1, 2, (3, 4), {'foo': 'bar'}]
        >>> const("[1]+[2]")
        Traceback (most recent call last):
        ...
        ValueError: opcode BINARY_ADD not allowed
    """

    c = test_expr(expr, _const_codes)
    return exec(c)

import traceback

def expr(expr):
    """expr(expression) -> value
    Safe Python expression evaluation
    Evaluates a string that contains an expression that only
    uses Python constants. This can be used to e.g. evaluate
    a numerical expression from an untrusted source.
    Examples:
        >>> expr("1+2")
        3
        >>> expr("[1,2]*2")
        [1, 2, 1, 2]
        >>> expr("__import__('sys').modules")
        Traceback (most recent call last):
        ...
        ValueError: opcode LOAD_NAME not allowed
    """
    try: 
        c = test_expr(expr, _expr_codes)
        return True
    except:
        traceback.print_exc()
        return False
    
    # return exec(c)

# program = R"""
# def AdamK5NoNoise(mymoves, othermoves, currentRound):
#   king_start = [False, True, True, False, True, True, True, False]
#   pawn_start = [True, False, True, True, True, True, True, False]
#   if len(othermoves) < 8:
#     return pawn_start[len(othermoves)]
#   if othermoves[0:8] == pawn_start:
#     return True
#   if othermoves[0:8] == king_start:
#     if len(othermoves) == 8:
#       return False
#     if othermoves[8] == False:
#       return False
#     return True
#   else:
#     return True
# """

# program = R"""
# open("./password.txt", "w")
# """


# expr(program)
