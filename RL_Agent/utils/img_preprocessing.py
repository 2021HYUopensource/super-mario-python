import cv2
import numpy as np

def make_stack(imgs):

    dsts = []
    for src in imgs:

        src = src[20:, :]
        cv2.imwrite("cut_img.jpg",src)
        dst = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
        cv2.imwrite("grayscale_img.jpg", dst)
        dst = cv2.resize(dst ,(84,84),interpolation=cv2.INTER_AREA)
        cv2.imwrite("resize_img.jpg", dst)
        dst = dst.astype(float) / 255.0
        dsts.append(dst)

    stack = np.stack([i for i in dsts],axis=-1)

    return stack