# cocotbpynq - a cocotb based emulation tool for PYNQ-targetting code
# Copyright (C) 2025 Gavin Lusby and Nachiket Kapre
# Developed at WatCAG, University of Waterloo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .dma import DMA
from cocotb import top as cocotop
from .dut import CocotbPynqDut
import os
from xml.etree import ElementTree

hwh_tree: ElementTree.Element = None
cptop: CocotbPynqDut = None

class DefaultIP:
    """ Currently just used to allow recursive hierarchical reference"""
    pass

class HierarchyObject:
    """
    Hierarchy object used by overlay class to hierarchically reference IPs

    Parameters
    ----------
    hierarchy : str/dict
        IP names or hierarchy of IP names
    """
    def __init__(self, hierarchy):
        self.hierarchy_dict = {}
        for hierarchy_object in hierarchy.keys():
            if(type(hierarchy[hierarchy_object]) == str):
                self.hierarchy_dict[hierarchy_object] = self.create_IP(hierarchy[hierarchy_object])
            else:
                self.hierarchy_dict[hierarchy_object] = HierarchyObject(hierarchy[hierarchy_object])

    def create_IP(self, instance_name):
        """
        Add an IP object to the hierarchy

        Parameters
        ----------
        hierarchy : str/dict
            IP instance type
        """
        instance_el = hwh_tree.find(f"./MODULES/MODULE[@INSTANCE='{instance_name}']")
        
        # Currently only DMA is supported here. Add more cases for more IP blocks as needed
        if(instance_el.get("VLNV").split(":")[:3] == ["xilinx.com", "ip", "axi_dma"]):
            return DMA(cptop.bus_interfaces, instance_el)
        else:
            return DefaultIP()

    def __getattr__(self, key):
        return self.hierarchy_dict[key]


class Overlay(HierarchyObject):
    """
    Drop in replacement for PYNQ overlay class

    Parameters
    ----------
    bitfile_name : str
        Name of bitstream file. Used to determine hwh file with same name. Needed for parity with PYNQ
    """
    def __init__(self, bitfile_name=None):
        bitstream_dir = os.getenv("HWH_LOCATION_DIR")
        if(not bitstream_dir):
            raise EnvironmentError("No HWH_LOCATION_DIR environment variable found")
        bitstream_path = os.path.abspath(os.path.join(bitstream_dir, bitfile_name))
        hwh_name = os.path.splitext(bitstream_path)[0] + ".hwh"
        if(not os.path.isfile(hwh_name)):
            raise ValueError(f"HWH file does not exist at {hwh_name}")

        # Create global variable hwh_tree
        global hwh_tree
        hwh_tree = ElementTree.parse(hwh_name).getroot()

        dut_module_name = str(cocotop)
        dut_module_el = hwh_tree.find(f"./MODULES/MODULE[@MODTYPE='{dut_module_name}']")

        # Create global variable cptop
        global cptop
        cptop = CocotbPynqDut(cocotop, dut_module_el, True)

        # discover all hierarchichally referenceble instances, as per how pynq library discovers them (for Zynq)
        processing_system_el = hwh_tree.find(f"./MODULES/MODULE[@MODTYPE='processing_system7']")
        if (processing_system_el is None):
            raise RuntimeError("No processing_system7 found. Please check that the HWH file you have generated is for a Zynq device. Only Zynq devices are supported at this time")
        instances_to_add = []
        for memrange in processing_system_el.findall("./MEMORYMAP/MEMRANGE"):
            instances_to_add.append(memrange.get("INSTANCE"))

        # Create pre-processor dict hierarchy
        hierarchy_to_add = {}
        for instance_name in instances_to_add:
            instance_el = hwh_tree.find(f"./MODULES/MODULE[@INSTANCE='{instance_name}']")
            instance_fullname = instance_el.get("FULLNAME")
            instance_hierarchy = instance_fullname.lstrip("/").split("/")
            imm_hierarchy = hierarchy_to_add
            for next_hierarchy_item in instance_hierarchy:
                if(next_hierarchy_item not in imm_hierarchy):
                    imm_hierarchy[next_hierarchy_item] = {}
                    if(next_hierarchy_item == instance_hierarchy[-1]):
                        imm_hierarchy[next_hierarchy_item] = instance_name
                imm_hierarchy = imm_hierarchy[next_hierarchy_item]

        # Create actual referenceable hierarchy structure recursively
        super().__init__(hierarchy_to_add)
