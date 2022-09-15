from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

int_or_none = lambda V: int(V) if V or V == 0 else None

export_digits = lambda S: ''.join([n for n in S if n.isdigit()])


def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    """
    reference: https://github.com/python/cpython/blob/main/Lib/difflib.py#L688
    """

    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]