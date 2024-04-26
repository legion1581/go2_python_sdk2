"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: unitree_go.msg.dds_
  IDL file: BmsState_.idl

"""

from enum import auto
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
# import unitree_go


@dataclass
@annotate.final
@annotate.autoid("sequential")
class BmsState_(idl.IdlStruct, typename="unitree_go.msg.dds_.BmsState_"):
    version_high: types.uint8
    version_low: types.uint8
    status: types.uint8
    soc: types.uint8
    current: types.int32
    cycle: types.uint16
    bq_ntc: types.array[types.uint8, 2]
    mcu_ntc: types.array[types.uint8, 2]
    cell_vol: types.array[types.uint16, 15]

