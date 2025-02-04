# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

from ..policy import DSPolicy
from ...model_implementations.diffusers.vae import DSVAE
from pydebug import debuginfo

class VAEPolicy(DSPolicy):

    def __init__(self):
        debuginfo(prj='ds', info='VAEPolicy init')
        super().__init__()
        try:
            import diffusers
            if hasattr(diffusers.models.vae, "AutoencoderKL"):
                debuginfo(prj='ds')
                self._orig_layer_class = diffusers.models.vae.AutoencoderKL
            else:
                debuginfo(prj='ds')
                # Diffusers >= 0.12.0 changes location of AutoencoderKL
                self._orig_layer_class = diffusers.models.autoencoder_kl.AutoencoderKL
        except ImportError:
            self._orig_layer_class = None

    def match(self, module):
        debuginfo(prj='ds')
        return isinstance(module, self._orig_layer_class)

    def match_replaced(self, module):
        debuginfo(prj='ds')
        return isinstance(module, DSVAE)

    def apply(self, module, enable_cuda_graph=True):
        debuginfo(prj='ds')
        # TODO(cmikeh2): Enable cuda graph should be an inference configuration
        return DSVAE(module, enable_cuda_graph=enable_cuda_graph)

    # NOTE (lekurile): Should we have a diffusers policy class?
    def attention(self, client_module):
        pass
