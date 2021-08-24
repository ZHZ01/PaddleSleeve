#   Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module provides the implementation for denoising methods.
"""
from __future__ import division

import logging
from collections import Iterable
import cv2
import numpy as np
import paddle
from .base import Denoise
from PIL import Image
from paddle.vision.transforms import functional as F

class GaussianBlur(Denoise):
    """
    This class implements denoise method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(GaussianBlur, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)

        for step in range(steps):
            kernel_size = step * 2 + 1
            if kernel_size == 1:
                continue
            img = cv2.GaussianBlur(denoising_image, (kernel_size, kernel_size), 0)
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising

class MedianBlur(Denoise):
    """
    This class implements MedianBlur method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(MedianBlur, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)

        for step in range(steps):
            kernel_size = step * 2 + 1
            if kernel_size == 1:
                continue
            img = cv2.medianBlur(denoising_image, kernel_size)
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising

class BoxFilter(Denoise):
    """
    This class implements BoxFilter method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(BoxFilter, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)

        for step in range(steps):
            kernel_size = step * 2 + 1
            if kernel_size == 1:
                continue
            img = cv2.boxFilter(src=denoising_image, ddepth=-1, ksize=(kernel_size, kernel_size), normalize=True)
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising


class BilateralFilter(Denoise):
    """
    This class implements BilateralFilter method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(BilateralFilter, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = denoising.input
        denoising_image = np.transpose(denoising_image, (1, 2, 0))
        denoising_image = (denoising_image * 255).astype(np.uint8)
        denoising_image = Image.fromarray(denoising_image)
        denoising_image = cv2.cvtColor(np.asarray(denoising_image), cv2.COLOR_RGB2BGR)

        for step in range(steps):
            img = cv2.bilateralFilter(denoising_image, 1, 50, 50)
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising

class MeanFilter(Denoise):
    """
    This class implements MeanFilter method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model to be attacked.
            support_targeted(Does): this attack method support targeted.
        """
        super(MeanFilter, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)

        for step in range(steps):
            kernel_size = step * 2 + 1
            if kernel_size == 1:
                continue
            img = cv2.blur(denoising_image, (kernel_size, kernel_size))
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising


class PixelDeflection(Denoise):
    """
    This class implements PixelDeflection method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(PixelDeflection, self).__init__(model)

    def _apply(self,
               denoising,
               steps=5,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.

        Returns:
            denoising(denoising): The denoising object.
        """

        # denoising_image = ndarray2opencv(denoising.input)
        denoising_image = denoising.input
        for i in range(steps):
            if i == 0:
                continue
            img = self.pixel_deflection(denoising_image, i / 100)
            # img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(np.expand_dims(img, axis=0)))
            if denoising.try_accept_the_example(img, img_label):
                return denoising

        return denoising

    def pixel_deflection(self, img, proportion):
        """
        add pixel deflection
        :param img:
        :param proportion: scale factor of number of defelctions (number of exchanged pixels)
                        with a hyper-parameter of window size set to 10 following the setting
                        of the original codes.
        :return:  pixel deflection of the given image
        Codes: https://github.com/iamaaditya/pixel-deflection
        Cite:
            Prakash, Aaditya, et al. "Deflecting adversarial attacks with pixel deflection."
            Proceedings of the IEEE conference on computer vision and pattern recognition. 2018.
        """
        C, H, W = img.shape
        # compute the number of pixels to be deflected
        deflections = int(proportion * H * W)
        window = 10
        while deflections > 0:
            # for consistency, when we deflect the given pixel from all the three channels.
            for c in range(C):
                x, y = np.random.randint(0, H - 1), np.random.randint(0, W - 1)
                while True:  # this is to ensure that PD pixel lies inside the image
                    a, b = np.random.randint(-1 * window, window), np.random.randint(-1 * window, window)
                    if x + a < H and x + a > 0 and y + b < W and y + b > 0: break
                # calling pixel deflection as pixel swap would be a misnomer,
                # as we can see below, it is one way copy
                img[c, x, y] = img[c, x + a, y + b]
            deflections -= 1
        return img


class JPEGCompression(Denoise):
    """
    This class implements JPEGCompression method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(JPEGCompression, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)
        # the maximum compression rate is 20, this different from other methods, better modify this in future work
        newstep = steps * 2
        for step in range(newstep):
            # the maximum compression rate is 100 - 19 * 5
            rate = 100 - step * 5
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), rate]
            result, encimg = cv2.imencode('.jpg', denoising_image, encode_param)
            decimg = cv2.imdecode(encimg, 1)
            img = opencv2ndarray(decimg)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising

        return denoising

class DCTCompression(Denoise):
    """
    This class implements DCTCompress method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(DCTCompression, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
            sigma: noise level
            psize: dct patch size 8 or 16, according to the paper:
            Yu, Guoshen, and Guillermo Sapiro. "DCT image denoising: a simple and effective
            image denoising algorithm." Image Processing On Line 1 (2011): 292-296.
        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)
        newsteps = steps * 2
        for patch_size in range(2):
            psize = (patch_size + 1) * 8
            for step in range(newsteps):
                sigma = step * 5
                img = np.zeros(denoising_image.shape, np.uint8)
                cv2.xphoto.dctDenoising(denoising_image, img, sigma, psize)
                # img = self.dct_denoise(denoising_image)
                img = opencv2ndarray(img)
                img_label = np.argmax(self.model.predict(img))
                if denoising.try_accept_the_example(np.squeeze(img), img_label):
                    return denoising
        return denoising

    # def dct_denoise(self, img):
    #     # must convert to float32
    #     img = np.float32(img) / 255.0
    #     # must use one channel for each time
    #     img_b = img[:, :, 0]
    #     img_g = img[:, :, 1]
    #     img_r = img[:, :, 2]
    #     # perform dct on each colour channel
    #     dct_b = cv2.dct(img_b)
    #     dct_g = cv2.dct(img_g)
    #     dct_r = cv2.dct(img_r)
    #     # perform inversedct on each dct channel
    #     img_b = cv2.idct(dct_b)
    #     img_g = cv2.idct(dct_g)
    #     img_r = cv2.idct(dct_r)
    #     img[:, :, 0] = img_b
    #     img[:, :, 1] = img_g
    #     img[:, :, 2] = img_r
    #     img = img * 255
    #     # convert back to uint8
    #     img = np.uint8(img)
    #     return img

class PCACompression(Denoise):
    """
    This class implements PCACompress method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(PCACompression, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = ndarray2opencv(denoising.input)
        # the maximum compression rate is 20, this different from other methods, better modify this in future work
        newsteps = steps * 2
        stride = int(denoising.input.shape[1] / newsteps)
        for step in range(newsteps):
            # the maximum compression rate is 100 - 19 * 5
            dim = denoising.input.shape[1] - stride * step
            img = self.pca_denoise(denoising_image, dim)
            img = opencv2ndarray(img)
            img_label = np.argmax(self.model.predict(img))
            if denoising.try_accept_the_example(np.squeeze(img), img_label):
                return denoising
        return denoising

    def pca_denoise(self, img, dim):
        """
        Apply PCA on the img and then convert it back
        :param img: the input image to be denoised, type: opencv
        :param dim: the dimension of the result after reduced, the less the dim, the more damage to the image
        :return: the denoise result
        """
        # must use one channel for each time
        img_b = img[:, :, 0]
        img_g = img[:, :, 1]
        img_r = img[:, :, 2]
        # perform pca on each colour channel
        mean, eig = cv2.PCACompute(img_b, mean=None, maxComponents = dim)
        pca_b = cv2.PCAProject(img_b, mean, eig)
        img_b = cv2.PCABackProject(pca_b, mean, eig)

        mean, eig = cv2.PCACompute(img_g, mean=None, maxComponents = dim)
        pca_g = cv2.PCAProject(img_g, mean, eig)
        img_g = cv2.PCABackProject(pca_g, mean, eig)


        mean, eig = cv2.PCACompute(img_r, mean=None, maxComponents = dim)
        pca_r = cv2.PCAProject(img_r, mean, eig)
        img_r = cv2.PCABackProject(pca_r, mean, eig)

        img[:, :, 0] = img_b
        img[:, :, 1] = img_g
        img[:, :, 2] = img_r
        return img

class GaussianNoise(Denoise):
    """
    This class implements GaussianNoise method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(GaussianNoise, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
        Returns:
            denoising(denoising): The denoising object.
        """

        h, w = denoising.input.shape[1:]
        area = h * w
        newsteps = steps * 10
        # the number of pixels with noise to be added
        pixel_num = int(area / newsteps)
        img = denoising.input.copy()
        for i in range(newsteps):
            if i == 0:
                continue
            img = self.gaussian_noise(img, 0, i / 100)
            img_label = np.argmax(self.model.predict(np.expand_dims(img, axis=0)))
            if denoising.try_accept_the_example(img, img_label):
                return denoising
        return denoising

    def gaussian_noise(self, img, mean, var):
        """
        Add gaussian noise on the input image
        :param img:
        :param mean:
        :param var:
        :return:
        """
        g_noise = np.random.normal(mean, var ** 0.5, img.shape)
        img = img + g_noise
        img = np.clip(img, 0, 1)
        return img

class SaltPepperNoise(Denoise):
    """
    This class implements Salt and Pepper Noise method.
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(SaltPepperNoise, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
        Returns:
            denoising(denoising): The denoising object.
        """

        h, w = denoising.input.shape[1:]
        newsteps = steps * 10
        for i in range(newsteps):
            if i == 0:
                continue
            img = self.salt_pepper_noise(denoising.input, i / 100, h, w)
            img_label = np.argmax(self.model.predict(np.expand_dims(img, axis=0)))
            if denoising.try_accept_the_example(img, img_label):
                return denoising
        return denoising

    def salt_pepper_noise(self, img, proportion, h, w):
        """
        Apply random noise on the input image with a pre-defined threshold
        :param img: the input image to be added noise, type: opencv
        :param proportion: the proportion of the added noise on the image
        :param h: the height of the image
        :param w: the weight of the image
        :return: the image with salt and pepper noises added (denoising by adding more noise)
        """
        threshold = proportion / 2
        for i in range(h):
            for j in range(w):
                random_number = np.random.random()
                if random_number < threshold:
                    img[:, i, j] = 1
                elif random_number > 1 - threshold:
                    img[:, i, j] = 0
        return img

class ResizePadding(Denoise):
    """
    This class implements Resize and Padding method.
    cite:
    Xie, Cihang, et al. "Mitigating adversarial effects through randomization." arXiv preprint arXiv:1711.01991 (2017).
    """
    def __init__(self, model):
        """
        Args:
            model: An instance of a paddle model.
        """
        super(ResizePadding, self).__init__(model)

    def _apply(self,
               denoising,
               steps=10,
               ):
        """
        Apply the denoising method.
        Args:
            denoising: The denoising object.
            steps: The number of denosing iteration.
        Returns:
            denoising(denoising): The denoising object.
        """

        denoising_image = denoising.input

        denoising_image = np.transpose(denoising_image, (1, 2, 0))
        H, W, C = denoising_image.shape
        for step in range(steps):
            # compute the resize size
            if step == 0:
                continue
            max_h = int(H * step / steps / 4)
            max_w = int(W * step / steps / 4)
            # get the resize and padding sizes
            resize_h = np.random.randint(0, max_h + 1)
            resize_w = np.random.randint(0, max_w + 1)
            resize_param = [H + resize_h, W + resize_w]
            pad_left = np.random.randint(0, max_h - resize_h + 1)
            pad_right = max_h - resize_h - pad_left
            pad_top = np.random.randint(0, max_w - resize_w + 1)
            pad_bottom = max_w - resize_w - pad_top
            pad_param = [pad_left, pad_right, pad_top, pad_bottom]
            # img_resizing = Resize(resize_param)
            # img_padding = paddle.nn.Pad2D(pad_param)
            img = F.resize(denoising_image, resize_param)
            img = F.pad(img, pad_param)
            img = np.transpose(img, (2, 0, 1))
            print(img.shape)
            img_label = np.argmax(self.model.predict(np.expand_dims(img, axis=0)))
            if denoising.try_accept_the_example(img, img_label):
                return denoising

        return denoising


def ndarray2opencv(img):
    """
    Convert ndarray to opencv image
    :param img: the input image, type: ndarray
    :return: an opencv image
    """

    img = np.transpose(img, (1, 2, 0))
    img = (img * 255).astype(np.uint8)
    img = Image.fromarray(img)
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def opencv2ndarray(img):
    """
    Convert opencv image to ndarray
    :param img: the input image, type: opencv
    :return: ndarray
    """
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img = np.asarray(img, dtype=np.float32)
    img = img / 255
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img