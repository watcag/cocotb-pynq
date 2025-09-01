Use python3 -m cocotbpynq.sample to see sample
# cocotbpynq
cocotbpynq is an extension of cocotb that allows for your PYNQ code to be seamlessly used for simulation. This allows you to debug the AXI transactions that occur between the PL and PS. Currently, there is support for the Pynq Z1 board, although it shouldn't be much different, (if at all), to adapt this code to other PYNQ-compatible FPGAs.

## Installation
Once Python is installed, install cocotbpynq using the following:

`pip install cocotbpynq`

 Alternatively, clone the repo and use it as an install directory for the most up-to-date version:

 `https://github.com/watcag/cocotb-pynq`


## cocotbpynq.sample
### How to use cocotbpynq
There is a sample directory, `src/cocotbpynq/sample` that shows everything needed make use cocotbpynq yourself. It even includes a hardware hand-off file. Specifically, you will want to reference `cocotb_runner.py` and `adapted.py` for development of your own tests.
### Running the sample
You can run this sample project mentioned above (after installing cocotbpynq) with:

`python3 -m cocotbpynq.sample`

Note that verilator is used in the sample project, so you will need verilator installed for this to work out of the box.
### Adaptation from PYNQ code
The `original.py` and `original_vs_adapted.diff` files are there to illustrate how few changes are needed to adapt PYNQ code ALSO be simulation ready. The adaptation should allow you to either run the `cocotb_runner.py` file to run a simulation, or continue to run the adapted file on a PYNQ-compatible board.
### Verilog Description
The sample is meant to illustrate a simple example with one AXI-Lite port(MMIO), one AXI-Stream read port (DMA send), and one AXI-Stream write port (DMA recv). The circuit performs a simple `y = ax²+bx+c` operation, where a, b, and c are all constants that can be modified/read using the MMIO port at addresses `0x10`, `0x18`, and `0x20` respectively, and `x` and `y` are AXI-Stream write/read ports respectively.

### HWH Generation
HWH file can be generated independantly of bitstream using the following Vivado CLI command:

`generate_target all <block design file>`

This can be used to circumvent the need to ever to bitstream generation. Unlike bitstream generation, this command only needs to be run if the block diagram is updated.



## Paper
Our paper was presented at the 35th International Conference on Field-Programmable Logic and Applications(FPL 2025). The conference paper can be found here: < Proceedings not available yet >