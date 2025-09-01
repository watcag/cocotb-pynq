from pathlib import Path
from cocotb.runner import get_runner
import sys
projdir = Path(__file__).resolve().parent # Set projdir to "sample" folder 

RUNNER="verilator" # Simulator
TOP="poly" # Toplevel verilog module name
SOURCES=[projdir / "poly_axi.v", projdir / "poly_AXILiteS_s_axi.v"] # List of 
TEST_MODULE_PATH= projdir / "adapted"
HWH_LOCATION_DIR = projdir
SYS_ARGV=" ".join(sys.argv)

runner = get_runner(RUNNER)
runner.build(
    sources=SOURCES,
    hdl_toplevel=TOP,
    always=True,
    build_args=[],
    parameters={},
    timescale = ('1ns', '1ps'),
    waves=True
)

runner.test(
    hdl_toplevel=TOP,
    hdl_toplevel_lang="verilog",
    test_dir=TEST_MODULE_PATH.parent,
    test_module=[TEST_MODULE_PATH.name],
    test_args=[],
    extra_env={ 
        "HWH_LOCATION_DIR": HWH_LOCATION_DIR,
        "COCOTB_SYS_ARGV": SYS_ARGV # Optionally pass commandline arguments to adapted.py, accessible as os.getenv("COCOTB_SYS_ARGV")
    },
    waves=True
)
