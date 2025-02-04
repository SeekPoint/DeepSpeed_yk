# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

from .sparsity_config import SparsityConfig, DenseSparsityConfig, FixedSparsityConfig, VariableSparsityConfig, BigBirdSparsityConfig, BSLongformerSparsityConfig, LocalSlidingWindowSparsityConfig
from .sparse_self_attention import SparseSelfAttention
from .bert_sparse_self_attention import BertSparseSelfAttention
from .sparse_attention_utils import SparseAttentionUtils
from pydebug import debuginfo
debuginfo(prj='ds', info='sparse_attention __init__')
