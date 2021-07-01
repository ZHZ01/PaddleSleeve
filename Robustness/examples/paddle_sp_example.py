# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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
""" Salt and pepper noise test case for Paddle """
from __future__ import absolute_import

import paddle
import paddle.vision.models as vm
import numpy as np
from perceptron.models.classification.paddle import PaddleModel
from perceptron.utils.image import imagenet_example
from perceptron.benchmarks.salt_pepper import SaltAndPepperNoiseMetric
from perceptron.utils.criteria.classification import Misclassification
from perceptron.utils.tools import plot_image
from perceptron.utils.tools import bcolors
import os

here = os.path.dirname(os.path.abspath(__file__))

# interpret the label as human language
with open(os.path.join(here, '../perceptron/utils/labels.txt')) as info:
    imagenet_dict = eval(info.read())

resnet18 = vm.resnet18(pretrained=True)
resnet18.eval()

is_available = len(paddle.static.cuda_places()) > 0
print('use gpu: ', is_available)

# initialize the PaddleModel
mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
std = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
fmodel = PaddleModel(
    resnet18, bounds=(0, 1), num_classes=1000, preprocessing=(mean, std))

# get source image and label
image, _ = imagenet_example(data_format='channels_first')
image = image / 255.  # because our model expects values in [0, 1]

# set the label as the predicted one
true_label = np.argmax(fmodel.predictions(image))
# set the type of noise which will used to generate the adversarial examples
metric = SaltAndPepperNoiseMetric(fmodel, criterion=Misclassification())

print(bcolors.BOLD + 'Process start' + bcolors.ENDC)
# set 'unpack' as false so we can access the detailed info of adversary
adversary = metric(image, true_label, unpack=False)
print(bcolors.BOLD + 'Process finished' + bcolors.ENDC)

if adversary.image is None:
    print(
        bcolors.WARNING +
        'Warning: Cannot find an adversary!' +
        bcolors.ENDC)
    exit(-1)

###################  print summary info  #####################################

keywords = ['Paddle', 'ResNet18', 'Misclassification', 'SaltAndPepper']

true_label = np.argmax(fmodel.predictions(image))
fake_label = np.argmax(fmodel.predictions(adversary.image))

# interpret the label as human language
with open('perceptron/utils/labels.txt') as info:
    imagenet_dict = eval(info.read())

print(bcolors.HEADER + bcolors.UNDERLINE + 'Summary:' + bcolors.ENDC)
print('Configuration:' + bcolors.CYAN + ' --framework %s '
                                        '--model %s --criterion %s '
                                        '--metric %s' % tuple(keywords) + bcolors.ENDC)
print('The predicted label of original image is '
      + bcolors.GREEN + imagenet_dict[true_label] + bcolors.ENDC)
print('The predicted label of adversary image is '
      + bcolors.RED + imagenet_dict[fake_label] + bcolors.ENDC)
print('Minimum perturbation required: %s' % bcolors.BLUE
      + str(adversary.distance) + bcolors.ENDC)
print('Verifiable bound: %s' % bcolors.BLUE
      + str(adversary.verifiable_bounds) + bcolors.ENDC)
print('\n')

plot_image(adversary,
           title=', '.join(keywords),
           figname='examples/images/%s.png' % '_'.join(keywords))
