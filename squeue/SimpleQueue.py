#=========================================================================
# SimpleQueue
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class SimpleQueue( VerilogPlaceholder, Component ):
  def construct( s ):

    s.enq_msg = InPort(8)
    s.enq_en  = InPort()
    s.enq_rdy = OutPort()

    s.deq_msg = OutPort(8)
    s.deq_en  = InPort()
    s.deq_rdy = OutPort()

