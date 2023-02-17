#=========================================================================
# SimpleQueueWrapper
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts

from squeue.SimpleQueue import SimpleQueue

class SimpleQueueWrapper:

  def __init__( s, cmdline_opts=None, autotick=True ):
    s.model = SimpleQueue()
    s.model = config_model_with_cmdline_opts( s.model, cmdline_opts, duts=[] )
    s.model.apply( DefaultPassGroup(linetrace=True) )
    s.model.sim_reset()
    s.autotick = autotick

  def tick( s ):
    s.model.sim_tick()
    s.model.enq_msg @= 0
    s.model.enq_en  @= 0
    s.model.deq_en  @= 0

  def enq_rdy( s ):
    return s.model.enq_rdy

  def enq( s, msg ):
    assert s.model.enq_rdy == 1
    s.model.enq_msg @= msg
    s.model.enq_en  @= 1
    if s.autotick:
      s.tick()

  def deq_rdy( s ):
    return s.model.deq_rdy

  def deq( s ):
    assert s.model.deq_rdy == 1
    s.model.deq_en @= 1
    s.model.sim_eval_combinational()
    msg = s.model.deq_msg.clone()
    if s.autotick:
      s.tick()
    return msg

