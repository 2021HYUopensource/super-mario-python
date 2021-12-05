import cv2
import numpy as np

def make_stack(imgs):

    dsts = []
    for src in imgs:

        dst = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
        dst = dst[40:, :]
        dst = cv2.resize(dst ,(84,84),interpolation=cv2.INTER_AREA)
        dst = dst.astype(float) / 255.0
        dsts.append(dst)

    stack = np.stack([i for i in dsts],axis=-1)

    return stack

def prep(src):

    dst = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    dst = dst[40:, :]
    dst = cv2.resize(dst ,(84,84),interpolation=cv2.INTER_AREA)
    dst = np.expand_dims(dst, axis=2)
    dst = dst.astype(float) / 255.0

    return dst