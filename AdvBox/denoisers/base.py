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
The base model of the model.
"""
import logging
from abc import ABCMeta
from abc import abstractmethod
import numpy as np
import paddle


class Denoise(object):
    """
    Abstract base class for adversarial denoising. `Denoise` represent an
    denoising which search an denoising example. Subclass should
    implement the _apply(self, denoising, **kwargs) method.
    Args:
        model(Model): an instance of a paddle model
    """
    __metaclass__ = ABCMeta

    def __init__(self, model):
        self.model = model

    def __call__(self, denoising, **kwargs):
        """
        Generate the denoising sample.
        Args:
        denoising(object): The denoising object.
        **kwargs: Other named arguments.
        """
        return self._apply(denoising, **kwargs)

    @abstractmethod
    def _apply(self, denoising, **kwargs):
        """
        Search an denoising example.
        Args:
        denoising(object): The denoising object.
        **kwargs: Other named arguments.
        """
        raise NotImplementedError
