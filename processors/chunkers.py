from math import floor, ceil

def char_chunks(txt, length=200, overlap=20, separators=[' ', '\n'], verbose=True):
    """ specified length and overlap are minimal, as they might increase slightly
    due to searching for separator characters """
    L = len(txt)
    n = (L-overlap)/(length-overlap)
    over = [(n1*length-L)/(n1-1) for n1 in [ceil(n),ceil(n)+1] if n1 != 1]
    if verbose: print(L, n, over)
    out, mi = [], []
    i = 0
    while True:
        j = min(i + length, L)
        while j < L and txt[j] not in separators:
            j += 1
        if verbose: print(f"{j-i} →", repr(txt[i:j]) )
        out.append(txt[i:j])
        mi.append(len(out[-1]))
        if j == L:
            break
        k = j - overlap
        while txt[k-1] not in separators and k > i:
            k -= 1
        i = k
    nc = len(out)
    mi0 = sum(mi[:-1])/(nc-1) if nc > 1 else mi[-1]
    return out, mi[-1]/mi0  

def char_chunks_it(txt, length=200, overlap=20, separators=[' ', '\n'], verbose=True):
    """ Iterative version of the above, to minizime the discrepancy of the last chunk. """
    out, mi = char_chunks(txt, length, overlap, separators, verbose=verbose)
    if mi < 0.95:
        while mi < 0.95:
            n = (len(txt)-overlap)/(length-overlap)
            if round(n) >= n:
                delta_o = min(4, max(1, round(overlap/10)))
                delta_l = 0
            else:
                delta_o = 0 # 1?
                delta_l = max(1, round(length/100))            
            overlap += delta_o
            length += delta_l
            if verbose: print(f"{mi:.4f} → new length: {length} overlap: {overlap}")
            out, mi = char_chunks(txt, length, overlap, separators, verbose=verbose)
    if True: print(f"{mi:.4f} final length: {length}, overlap: {overlap}")
    return out

def word_split(txt, separators=[' ','\n']):
    """ Split a text into a list of words, as defined by separators. """
    input = []
    output = [txt]
    for s in separators:
        input = [o for o in output if o != '']
        output = []
        for chunk in input:
            output += chunk.split(s)
    return output

def word_chunks(txt, length=60, overlap=6, separators=[' ', '\n']):
    """ Get word lengths, and proceed with char splitter based on means.
    Older approach, when the specified length is maximal, while overlap minimal."""
    words = word_split(txt, separators)
    mean = sum(len(w) for w in words)/len(words)  
    length = round(mean*length)
    overlap = round(mean*overlap)
    L = len(txt)
    n = (L-overlap)/(length-overlap)
    #print(mean, length, overlap, n)
    i = 0
    out = []
    while True:
        j = min(i + length, L)
        if j == L:
            out.append(txt[i:j])
            break
        while txt[j] not in separators and j > i:
            j -= 1
        out.append(txt[i:j])
        k = j - overlap
        while txt[k-1] not in separators and k > i:
            k -= 1
        i = k
    return out