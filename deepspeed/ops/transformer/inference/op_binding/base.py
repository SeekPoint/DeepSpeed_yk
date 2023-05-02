# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

import torch
from ..config import DeepSpeedInferenceConfig

from deepspeed.ops.op_builder import InferenceBuilder


class BaseOp(torch.nn.Module):
    inference_cuda_module = None

    def __init__(self, config: DeepSpeedInferenceConfig):
        #print('BaseOp init')
        super(BaseOp, self).__init__()
        self.config = config
        if BaseOp.inference_cuda_module is None:
            builder = InferenceBuilder()
            BaseOp.inference_cuda_module = builder.load()
