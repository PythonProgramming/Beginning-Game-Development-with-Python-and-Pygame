def alpha_blend(src, dst):
    return src * src.a + dst * (1.0—src.a)
