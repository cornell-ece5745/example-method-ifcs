//========================================================================
// Simple Queue
//========================================================================
// Simple single-element normal queue.

`ifndef SQUEUE_SIMPLE_QUEUE_V
`define SQUEUE_SIMPLE_QUEUE_V

`include "vc/trace.v"

module squeue_SimpleQueue
(
  input  logic       clk,
  input  logic       reset,

  input  logic [7:0] enq_msg,
  input  logic       enq_en,
  output logic       enq_rdy,

  output logic [7:0] deq_msg,
  input  logic       deq_en,
  output logic       deq_rdy
);

  //----------------------------------------------------------------------
  // Sequential State
  //----------------------------------------------------------------------

  // Data register

  logic [7:0] data;
  logic [7:0] data_next;

  always @( posedge clk ) begin
    if ( reset )
      data <= 0;
    else
      data <= data_next;
  end

  // Valid register

  logic val;
  logic val_next;

  always @( posedge clk ) begin
    if ( reset )
      val <= 0;
    else
      val <= val_next;
  end

  //----------------------------------------------------------------------
  // Combinational Logic
  //----------------------------------------------------------------------

  always @(*) begin

    data_next = data;
    val_next  = val;
    deq_msg   = 8'b0;

    // If we do an enqueue operation then write the data register and set
    // the valid bit

    if ( enq_en ) begin
      data_next = enq_msg;
      val_next  = 1'b1;
    end

    // If we do a dequeue operation then return the data, clear the data
    // register, and clear the valid bit

    if ( deq_en ) begin
      deq_msg   = data;
      data_next = 8'b0;
      val_next  = 1'b0;
    end

    // Note that we should never be able to do an enqueue and dequeue
    // operation in the same cycle!

  end

  assign enq_rdy = ~val;
  assign deq_rdy = val;

  //----------------------------------------------------------------------
  // Line tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    if ( enq_en ) begin
      $sformat( str, "enq(%x)", enq_msg );
      vc_trace.append_str( trace_str, str );
    end
    else
      vc_trace.append_chars( trace_str, " ", 7 );

    vc_trace.append_str( trace_str, " " );

    if ( deq_en ) begin
      $sformat( str, "%x=deq()", deq_msg );
      vc_trace.append_str( trace_str, str );
    end
    else
      vc_trace.append_chars( trace_str, " ", 8 );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* SQUEUE_SIMPLE_QUEUE_V */


