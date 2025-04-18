# Copyright 2024-2025 Arm Limited and/or its affiliates.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe

from typing import List

import torch

import tosa_tools.v0_80.serializer.tosa_serializer as ts  # type: ignore
from executorch.backends.arm.operators.node_visitor import (
    NodeVisitor,
    register_node_visitor,
)
from executorch.backends.arm.tosa_mapping import TosaArg


@register_node_visitor
class TransposeVisitor(NodeVisitor):
    """
    This node visitor targets the _transpose op defined in the
    passthrough_to_tosa library. Used when switching between tosa_dim_orders.
    Inserts a TOSA TRANSPOSE.
    """

    target = "_transpose.default"

    def define_node(
        self,
        node: torch.fx.Node,
        tosa_graph: ts.TosaSerializer,
        inputs: List[TosaArg],
        output: TosaArg,
    ) -> None:
        output_rank = len(output.shape)
        perms = [dim % output_rank for dim in inputs[1].special]
        attr = ts.TosaSerializerAttribute()
        attr.TransposeAttribute(perms)
        tosa_graph.addOperator(
            ts.TosaOp.Op().TRANSPOSE, [inputs[0].name], [output.name], attr
        )
