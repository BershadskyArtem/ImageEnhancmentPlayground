import pywt


def decompose(img, waveletname, levels):
    return pywt.wavedec2(img, waveletname, level=levels)

def compose(coeffecients,waveletname):
    return pywt.waverec2(coeffecients, waveletname)



