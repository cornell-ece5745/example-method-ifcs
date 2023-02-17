#=========================================================================
# SimpleQueue_test
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from squeue.SimpleQueue import SimpleQueue
from squeue.SimpleQueueWrapper import SimpleQueueWrapper

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( cmdline_opts ):
  run_test_vector_sim( SimpleQueue(), [
    ('enq_msg enq_en enq_rdy* deq_msg* deq_en deq_rdy*'),
    [ 0x00,   0,     1,       0x00,    0,     0        ],
    [ 0xab,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0x00,    0,     1        ],
    [ 0x00,   0,     0,       0xab,    1,     1        ],
    [ 0x00,   0,     1,       0x00,    0,     0        ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test_two_msgs
#-------------------------------------------------------------------------

def test_two_msgs( cmdline_opts ):
  run_test_vector_sim( SimpleQueue(), [
    ('enq_msg enq_en enq_rdy* deq_msg* deq_en deq_rdy*'),
    [ 0x00,   0,     1,       0x00,    0,     0        ],
    [ 0xab,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0x00,    0,     1        ],
    [ 0x00,   0,     0,       0xab,    1,     1        ],
    [ 0x00,   0,     1,       0x00,    0,     0        ],
    [ 0xcd,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0x00,    0,     1        ],
    [ 0x00,   0,     0,       0xcd,    1,     1        ],
    [ 0x00,   0,     1,       0x00,    0,     0        ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test_back2back
#-------------------------------------------------------------------------

def test_back2back( cmdline_opts ):
  run_test_vector_sim( SimpleQueue(), [
    ('enq_msg enq_en enq_rdy* deq_msg* deq_en deq_rdy*'),
    [ 0xab,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0xab,    1,     1        ],
    [ 0xcd,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0xcd,    1,     1        ],
    [ 0xef,   1,     1,       0x00,    0,     0        ],
    [ 0x00,   0,     0,       0xef,    1,     1        ],
    [ 0x00,   0,     1,       0x00,    0,     0        ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test_wrapper_basic
#-------------------------------------------------------------------------

def test_wrapper_basic( cmdline_opts ):
  q = SimpleQueueWrapper( cmdline_opts, autotick=False )

  q.tick()
  q.enq(0xab)
  q.tick()
  q.tick()
  assert q.deq() == 0xab
  q.tick()
  q.tick()

#-------------------------------------------------------------------------
# test_wrapper_autotick
#-------------------------------------------------------------------------

def test_wrapper_autotick( cmdline_opts ):
  q = SimpleQueueWrapper( cmdline_opts )

  q.enq(0xab)
  assert q.deq() == 0xab

  q.enq(0xcd)
  assert q.deq() == 0xcd

  q.enq(0xef)
  assert q.deq() == 0xef

#-------------------------------------------------------------------------
# test_wrapper_many
#-------------------------------------------------------------------------

def test_wrapper_many( cmdline_opts ):
  q = SimpleQueueWrapper( cmdline_opts )

  for i in range(32):
    q.enq(i)
    assert q.deq() == i

