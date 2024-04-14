# Copyright (c) OpenMMLab. All rights reserved.
# flake8: noqa
import warnings

from . import config
from . import iopath
from . import vis

# from .arraymisc import *
# from .image import *
from .utils import *
from .version import *
# from .video import *
# from .visualization import *




# The following modules are not imported to this level, so cvutils may be used
# without PyTorch.
# - runner
# - parallel
# - op
# - device

# warnings.warn(
#     'On January 1, 2023, MMCV will release v2.0.0, in which it will remove '
#     'components related to the training process and add a data transformation '
#     'module. In addition, it will rename the package names cvutils to cvutils-lite '
#     'and cvutils-full to cvutils. '
#     'See https://github.com/open-mmlab/cvutils/blob/master/docs/en/compatibility.md '
#     'for more details.')
