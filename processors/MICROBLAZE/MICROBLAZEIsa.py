# -*- coding: iso-8859-1 -*-
####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################



# Lets first of all import the necessary files for the
# creation of the processor
import trap
import cxx_writer
from MICROBLAZECoding import *
from MICROBLAZEMethods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions

isa.addMethod(SignExtend_method)


#-------------------------------------------------------------------------------------
# Let's now procede to set the behavior of the instructions
#-------------------------------------------------------------------------------------
#
# Note the special operations:
#
# -- annull(): transforms the current instruction in a NOP; if we are
# in the middle of the execution of some code, it also terminates the
# execution of that part of code (it is like an exception)
# -- flush(): flushes the pipeline stages preceding the one in which
# the flush method has been called
# -- stall(n): stalls the current stage and the preceding ones for n clock
# cycles. If we issue this operation in the middle of the execution of an
# instruction, anyway the execution of that code finished before the stall
# operation has any effect; if that code contains another call to stall(m),
# the pipeline stages are stalled for a total of n+m
# -- THROW_EXCEPTION: a macro for throwing C++ exceptions
#

#____________________________________________________________________________________________________
#----------------------------------------------------------------------------------------------------
# Now using all the defined operations, instruction codings, etc
# I can actually declare the processor instructions
#----------------------------------------------------------------------------------------------------
#____________________________________________________________________________________________________

#this is just a trial

#ADD instruction family
# ADD, first version
#~ opCode = cxx_writer.writer_code.Code("""
#~ unsigned long long result = (int)rb + (int)ra;
#~ MSR[C] = ((unsigned long long)result) >> 32;  #get the CarryOut
#~ rd = (unsigned int)result;
#~ """)
#~ add_Instr = trap.Instruction('ADD', True)
#~ add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
#~ add_Instr.setCode(opCode,'execute')
#~ add_Instr.addBehavior(IncrementPC, 'execute')
#~ isa.addInstruction(add_Instr)

# ADD, second version
opCode = cxx_writer.writer_code.Code("""
result = (int)rb + (int)ra;
MSR[key_C] = result >> 32;  /* get the CarryOut */
rd = (unsigned int)result;
""")
add_Instr = trap.Instruction('ADD', True) #?? what does 'true' mean?
add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addVariable(('result', 'BIT<64>'))
add_Instr.addTest({'rd': 5, 'ra': 3, 'rb': 2}, {'GPR[3]': 4, 'GPR[2]': 6, 'GPR[5]': 0xfffff, 'PC':0x0}, {'GPR[5]': 10, 'PC':0x4})
isa.addInstruction(add_Instr)

# ADDC
opCode = cxx_writer.writer_code.Code("""
result = (int)rb + (int)ra + (unsigned int)MSR[key_C];
MSR[key_C] = result >> 32; /* get the CarryOut */
rd = (unsigned int)result;
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addc_Instr)

# ADDK
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra;
""")
addk_Instr = trap.Instruction('ADDK', True)
addk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addk_Instr.setCode(opCode,'execute')
addk_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addk_Instr)

# ADDKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra +(unsigned int)MSR[key_C];
""")
addkc_Instr = trap.Instruction('ADDKC', True)
addkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addkc_Instr.setCode(opCode,'execute')
addkc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addkc_Instr)

#ADDI instruction family
#ADDI
opCode = cxx_writer.writer_code.Code("""
result = (int)ra + ((int)SignExtend(imm, 16));
MSR[key_C] = result >> 32;
rd = (unsigned int)result;
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,0]}, 'TODO')
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
addi_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addi_Instr)

#ADDIC
opCode = cxx_writer.writer_code.Code("""
result = (int)ra + ((int)SignExtend(imm,16)) + (unsigned int)MSR[key_C];
MSR[key_C] = result >> 32;
rd = (unsigned int)result;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,0]}, 'TODO')
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
addic_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addic_Instr)

#ADDIK
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + ((int)SignExtend(imm, 16));
""")
addik_Instr = trap.Instruction('ADDIK', True)
addik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,0]}, 'TODO')
addik_Instr.setCode(opCode,'execute')
addik_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addik_Instr)

#ADDIKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + ((int)SignExtend(imm, 16)) +(int)MSR[key_C];
""")
addikc_Instr = trap.Instruction('ADDIKC', True)
addikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,0]}, 'TODO')
addikc_Instr.setCode(opCode,'execute')
addikc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addikc_Instr)

#from here to the end, it is specified for each instruction, only
#the bytecode and the name.
#After, it will be specified also the behavior.

#AND
opCode = cxx_writer.writer_code.Code("""

""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
and_Instr.setCode(opCode,'execute')
isa.addInstruction(and_Instr)

#AND instruction family
#ANDI
opCode = cxx_writer.writer_code.Code("""

""")
andi_Instr = trap.Instruction('ANDI', True)
andi_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,1]}, 'TODO')
andi_Instr.setCode(opCode,'execute')
isa.addInstruction(andi_Instr)

#ANDN
opCode = cxx_writer.writer_code.Code("""

""")
andn_Instr = trap.Instruction('ANDN', True)
andn_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
andn_Instr.setCode(opCode,'execute')
isa.addInstruction(andn_Instr)

#ANDNI
opCode = cxx_writer.writer_code.Code("""

""")
andni_Instr = trap.Instruction('ANDNI', True)
andni_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,1]}, 'TODO')
andni_Instr.setCode(opCode,'execute')
isa.addInstruction(andni_Instr)

#BRANCH instruction family
#BEQ
#TODO: check if BEQ opcode is correct
opCode = cxx_writer.writer_code.Code("""
if (ra==0) {
	PC = PC + ((int)SignExtend(rb, 8));
} else {
	PC = PC + 4;
}
""")
beq_Instr = trap.Instruction('BEQ','True')
beq_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beq_Instr.setCode(opCode,'execute')
# we increment PC in the code. We don't have to use IncrementPCBehavior.
# beq_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(beq_Instr)

#BEQD
#TODO: check if BEQ is correct
opCode = cxx_writer.writer_code.Code("""

""")
beqd_Instr = trap.Instruction('BEQD','True')
beqd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beqd_Instr.setCode(opCode,'execute')
# we increment PC in the code. We don't have to use IncrementPCBehavior.
# beq_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(beqd_Instr)

#BEQI
opCode = cxx_writer.writer_code.Code("""

""")
beqi_Instr = trap.Instruction('BEQI','True')
beqi_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,0]}, 'TODO')
beqi_Instr.setCode(opCode,'execute')
isa.addInstruction(beqi_Instr)

#BEQID
opCode = cxx_writer.writer_code.Code("""

""")
beqid_Instr = trap.Instruction('BEQID','True')
beqid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,0]}, 'TODO')
beqid_Instr.setCode(opCode,'execute')
isa.addInstruction(beqid_Instr)

#BGE
opCode = cxx_writer.writer_code.Code("""

""")
bge_Instr = trap.Instruction('BGE','True')
bge_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bge_Instr.setCode(opCode,'execute')
isa.addInstruction(bge_Instr)

#BGED
opCode = cxx_writer.writer_code.Code("""

""")
bged_Instr = trap.Instruction('BGED','True')
bged_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bged_Instr.setCode(opCode,'execute')
isa.addInstruction(bged_Instr)

#BGEI
opCode = cxx_writer.writer_code.Code("""

""")
bgei_Instr = trap.Instruction('BGEI','True')
bgei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,1]}, 'TODO')
bgei_Instr.setCode(opCode,'execute')
isa.addInstruction(bgei_Instr)

#BGEID
opCode = cxx_writer.writer_code.Code("""

""")
bgeid_Instr = trap.Instruction('BGEID','True')
bgeid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,1]}, 'TODO')
bgeid_Instr.setCode(opCode,'execute')
isa.addInstruction(bgeid_Instr)

#BGT
opCode = cxx_writer.writer_code.Code("""

""")
bgt_Instr = trap.Instruction('BGT','True')
bgt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bgt_Instr.setCode(opCode,'execute')
isa.addInstruction(bgt_Instr)

#BGTD
opCode = cxx_writer.writer_code.Code("""

""")
bgtd_Instr = trap.Instruction('BGTD','True')
bgtd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bgtd_Instr.setCode(opCode,'execute')
isa.addInstruction(bgtd_Instr)

#BGTI
opCode = cxx_writer.writer_code.Code("""

""")
bgti_Instr = trap.Instruction('BGTI','True')
bgti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,0]}, 'TODO')
bgti_Instr.setCode(opCode,'execute')
isa.addInstruction(bgti_Instr)

#BGTID
opCode = cxx_writer.writer_code.Code("""

""")
bgtid_Instr = trap.Instruction('BGTID','True')
bgtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,0]}, 'TODO')
bgtid_Instr.setCode(opCode,'execute')
isa.addInstruction(bgtid_Instr)

#BLE
opCode = cxx_writer.writer_code.Code("""

""")
ble_Instr = trap.Instruction('BLE','True')
ble_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
ble_Instr.setCode(opCode,'execute')
isa.addInstruction(ble_Instr)

#BLED
opCode = cxx_writer.writer_code.Code("""

""")
bled_Instr = trap.Instruction('BLED','True')
bled_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bled_Instr.setCode(opCode,'execute')
isa.addInstruction(bled_Instr)

#BLEI
opCode = cxx_writer.writer_code.Code("""

""")
blei_Instr = trap.Instruction('BLEI','True')
blei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,1]}, 'TODO')
blei_Instr.setCode(opCode,'execute')
isa.addInstruction(blei_Instr)

#BLEID
opCode = cxx_writer.writer_code.Code("""

""")
bleid_Instr = trap.Instruction('BLEID','True')
bleid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,1]}, 'TODO')
bleid_Instr.setCode(opCode,'execute')
isa.addInstruction(bleid_Instr)

#BLT
opCode = cxx_writer.writer_code.Code("""

""")
blt_Instr = trap.Instruction('BLT','True')
blt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
blt_Instr.setCode(opCode,'execute')
isa.addInstruction(blt_Instr)

#BLTD
opCode = cxx_writer.writer_code.Code("""

""")
bltd_Instr = trap.Instruction('BLTD','True')
bltd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bltd_Instr.setCode(opCode,'execute')
isa.addInstruction(bltd_Instr)

#BLTI
opCode = cxx_writer.writer_code.Code("""

""")
blti_Instr = trap.Instruction('BLTI','True')
blti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,0]}, 'TODO')
blti_Instr.setCode(opCode,'execute')
isa.addInstruction(blti_Instr)

#BLTID
opCode = cxx_writer.writer_code.Code("""

""")
bltid_Instr = trap.Instruction('BLTID','True')
bltid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,0]}, 'TODO')
bltid_Instr.setCode(opCode,'execute')
isa.addInstruction(bltid_Instr)

#BNE
opCode = cxx_writer.writer_code.Code("""

""")
bne_Instr = trap.Instruction('BNE','True')
bne_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bne_Instr.setCode(opCode,'execute')
isa.addInstruction(bne_Instr)

#BNED
opCode = cxx_writer.writer_code.Code("""

""")
bned_Instr = trap.Instruction('BNED','True')
bned_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bned_Instr.setCode(opCode,'execute')
isa.addInstruction(bned_Instr)

#BNEI
opCode = cxx_writer.writer_code.Code("""

""")
bnei_Instr = trap.Instruction('BNEI','True')
bnei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,1]}, 'TODO')
bnei_Instr.setCode(opCode,'execute')
isa.addInstruction(bnei_Instr)

#BNEID
opCode = cxx_writer.writer_code.Code("""

""")
bneid_Instr = trap.Instruction('BNEID','True')
bneid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,1]}, 'TODO')
bneid_Instr.setCode(opCode,'execute')
isa.addInstruction(bneid_Instr)

#BR
opCode = cxx_writer.writer_code.Code("""

""")
br_Instr = trap.Instruction('BR','True')
br_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
br_Instr.setCode(opCode,'execute')
isa.addInstruction(br_Instr)

#BRA
opCode = cxx_writer.writer_code.Code("""

""")
bra_Instr = trap.Instruction('BRA','True')
bra_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bra_Instr.setCode(opCode,'execute')
isa.addInstruction(bra_Instr)

#BRD
opCode = cxx_writer.writer_code.Code("""

""")
brd_Instr = trap.Instruction('BRD','True')
brd_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brd_Instr.setCode(opCode,'execute')
isa.addInstruction(brd_Instr)

#BRAD
opCode = cxx_writer.writer_code.Code("""

""")
brad_Instr = trap.Instruction('BRAD','True')
brad_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brad_Instr.setCode(opCode,'execute')
isa.addInstruction(brad_Instr)

#BRLD
opCode = cxx_writer.writer_code.Code("""

""")
brld_Instr = trap.Instruction('BRLD','True')
brld_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brld_Instr.setCode(opCode,'execute')
isa.addInstruction(brld_Instr)

#BRALD
opCode = cxx_writer.writer_code.Code("""

""")
brald_Instr = trap.Instruction('BRALD','True')
brald_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brald_Instr.setCode(opCode,'execute')
isa.addInstruction(brald_Instr)

#BRI
opCode = cxx_writer.writer_code.Code("""

""")
bri_Instr = trap.Instruction('BRI','True')
bri_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,0,0,0,0]}, 'TODO')
bri_Instr.setCode(opCode,'execute')
isa.addInstruction(bri_Instr)

#BRAI
opCode = cxx_writer.writer_code.Code("""

""")
brai_Instr = trap.Instruction('BRAI','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,0,0,0]}, 'TODO')
brai_Instr.setCode(opCode,'execute')
isa.addInstruction(brai_Instr)

#BRID
opCode = cxx_writer.writer_code.Code("""

""")
brid_Instr = trap.Instruction('BRID','True')
brid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,0,0,0]}, 'TODO')
brid_Instr.setCode(opCode,'execute')
isa.addInstruction(brid_Instr)

#BRAID
opCode = cxx_writer.writer_code.Code("""

""")
brai_Instr = trap.Instruction('BRAID','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,0,0,0]}, 'TODO')
brai_Instr.setCode(opCode,'execute')
isa.addInstruction(brai_Instr)

#BRLID
opCode = cxx_writer.writer_code.Code("""

""")
brlid_Instr = trap.Instruction('BRLID','True')
brlid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,1,0,0]}, 'TODO')
brlid_Instr.setCode(opCode,'execute')
isa.addInstruction(brlid_Instr)

#BRALID
opCode = cxx_writer.writer_code.Code("""

""")
bralid_Instr = trap.Instruction('BRALID','True')
bralid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,1,0,0]}, 'TODO')
bralid_Instr.setCode(opCode,'execute')
isa.addInstruction(bralid_Instr)

#BRK
#BRK is equal to BRAL
opCode = cxx_writer.writer_code.Code("""

""")
brk_Instr = trap.Instruction('BRK','True')
brk_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brk_Instr.setCode(opCode,'execute')
isa.addInstruction(brk_Instr)

#BRKI
#BRKI is equal to BRALI
opCode = cxx_writer.writer_code.Code("""

""")
brki_Instr = trap.Instruction('BRKI','True')
brki_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,1,0,0]}, 'TODO')
brki_Instr.setCode(opCode,'execute')
isa.addInstruction(brki_Instr)

#BARREL SHIFT family
#BSRL (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""

""")
bsrl_Instr = trap.Instruction('BSRL', True)
bsrl_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsrl_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrl_Instr)

#BSRA (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")
bsra_Instr = trap.Instruction('BSRA', True)
bsra_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,1,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsra_Instr.setCode(opCode,'execute')
isa.addInstruction(bsra_Instr)

#BSLL (S=1, T=0)
opCode = cxx_writer.writer_code.Code("""

""")
bsll_Instr = trap.Instruction('BSLL', True)
bsll_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsll_Instr.setCode(opCode,'execute')
isa.addInstruction(bsll_Instr)

#BSRLI (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""

""")
bsrli_Instr = trap.Instruction('BSRLI', True)
bsrli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0]}, 'TODO')
bsrli_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrli_Instr)

#BSRAI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")
bsrai_Instr = trap.Instruction('BSRAI', True)
bsrai_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,1,0,0,0,0]}, 'TODO')
bsrai_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrai_Instr)

#BSLLI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")
bslli_Instr = trap.Instruction('BSLLI', True)
bslli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [1,0,0,0,0,0]}, 'TODO')
bslli_Instr.setCode(opCode,'execute')
isa.addInstruction(bslli_Instr)

#COMPARE family
#CMP
opCode = cxx_writer.writer_code.Code("""

""")
cmp_Instr = trap.Instruction('CMP', True)
cmp_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
cmp_Instr.setCode(opCode,'execute')
isa.addInstruction(cmp_Instr)

#CMPU
opCode = cxx_writer.writer_code.Code("""

""")
cmpu_Instr = trap.Instruction('CMPU', True)
cmpu_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, 'TODO')
cmpu_Instr.setCode(opCode,'execute')
isa.addInstruction(cmpu_Instr)

#FLOAT family
#FADD
opCode = cxx_writer.writer_code.Code("""

""")
fadd_Instr = trap.Instruction('FADD', True)
fadd_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
fadd_Instr.setCode(opCode,'execute')
isa.addInstruction(fadd_Instr)

#FRSUB
opCode = cxx_writer.writer_code.Code("""

""")
frsub_Instr = trap.Instruction('FRSUB', True)
frsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,1,0,0,0,0,0,0,0]}, 'TODO')
frsub_Instr.setCode(opCode,'execute')
isa.addInstruction(frsub_Instr)

#FMUL
opCode = cxx_writer.writer_code.Code("""

""")
fmul_Instr = trap.Instruction('FMUL', True)
fmul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,0,0,0,0,0,0,0,0]}, 'TODO')
fmul_Instr.setCode(opCode,'execute')
isa.addInstruction(fmul_Instr)

#FDIV
opCode = cxx_writer.writer_code.Code("""

""")
fdiv_Instr = trap.Instruction('FDIV', True)
fdiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,1,0,0,0,0,0,0,0]}, 'TODO')
fdiv_Instr.setCode(opCode,'execute')
isa.addInstruction(fdiv_Instr)

#FCMP
opCode = cxx_writer.writer_code.Code("""

""")
fcmp_Instr = trap.Instruction('FCMP', True)
fcmp_Instr.setMachineCode(float_cmp, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,0,0], 'opcode2': [0,0,0,0]}, 'TODO')
fcmp_Instr.setCode(opCode,'execute')
isa.addInstruction(fcmp_Instr)

#FLT
opCode = cxx_writer.writer_code.Code("""

""")
flt_Instr = trap.Instruction('FLT', True)
flt_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,0,1,0,0,0,0,0,0,0]}, 'TODO')
flt_Instr.setCode(opCode,'execute')
isa.addInstruction(flt_Instr)

#FINT
opCode = cxx_writer.writer_code.Code("""

""")
fint_Instr = trap.Instruction('FINT', True)
fint_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,1,0,0,0,0,0,0,0,0]}, 'TODO')
fint_Instr.setCode(opCode,'execute')
isa.addInstruction(fint_Instr)

#FSQRT
opCode = cxx_writer.writer_code.Code("""

""")
fsqrt_Instr = trap.Instruction('FSQRT', True)
fsqrt_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,1,1,0,0,0,0,0,0,0]}, 'TODO')
fsqrt_Instr.setCode(opCode,'execute')
isa.addInstruction(fsqrt_Instr)

#GET / GETD
#very strange instructions :)

#IDIV
opCode = cxx_writer.writer_code.Code("""

""")
idiv_Instr = trap.Instruction('IDIV', True)
idiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
idiv_Instr.setCode(opCode,'execute')
isa.addInstruction(idiv_Instr)

#IDIVU
opCode = cxx_writer.writer_code.Code("""

""")
idivu_Instr = trap.Instruction('IDIVU', True)
idivu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, 'TODO')
idivu_Instr.setCode(opCode,'execute')
isa.addInstruction(idivu_Instr)

#IMM
opCode = cxx_writer.writer_code.Code("""

""")
imm_Instr = trap.Instruction('IMM', True)
imm_Instr.setMachineCode(imm_code, {'opcode': [1,0,1,1,0,0]}, 'TODO')
imm_Instr.setCode(opCode,'execute')
isa.addInstruction(imm_Instr)

#LOAD family
#LBU
opCode = cxx_writer.writer_code.Code("""

""")
lbu_Instr = trap.Instruction('LBU', True)
lbu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lbu_Instr.setCode(opCode,'execute')
isa.addInstruction(lbu_Instr)

#LBUI
opCode = cxx_writer.writer_code.Code("""

""")
lbui_Instr = trap.Instruction('LBUI', True)
lbui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,0]}, 'TODO')
lbui_Instr.setCode(opCode,'execute')
isa.addInstruction(lbui_Instr)

#LHU
opCode = cxx_writer.writer_code.Code("""

""")
lhu_Instr = trap.Instruction('LHU', True)
lhu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lhu_Instr.setCode(opCode,'execute')
isa.addInstruction(lhu_Instr)

#LHUI
opCode = cxx_writer.writer_code.Code("""

""")
lhui_Instr = trap.Instruction('LHUI', True)
lhui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,1]}, 'TODO')
lhui_Instr.setCode(opCode,'execute')
isa.addInstruction(lhui_Instr)

#LW
opCode = cxx_writer.writer_code.Code("""

""")
lw_Instr = trap.Instruction('LW', True)
lw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lw_Instr.setCode(opCode,'execute')
isa.addInstruction(lw_Instr)

#LWI
opCode = cxx_writer.writer_code.Code("""

""")
lwi_Instr = trap.Instruction('LWI', True)
lwi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,1,0]}, 'TODO')
lwi_Instr.setCode(opCode,'execute')
isa.addInstruction(lwi_Instr)

#MFS
opCode = cxx_writer.writer_code.Code("""

""")
mfs_Instr = trap.Instruction('MFS', True)
mfs_Instr.setMachineCode(mfs_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mfs_Instr.setCode(opCode,'execute')
isa.addInstruction(mfs_Instr)

#MSRCLR
opCode = cxx_writer.writer_code.Code("""

""")
msrclr_Instr = trap.Instruction('MSRCLR', True)
msrclr_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,1,0]}, 'TODO')
msrclr_Instr.setCode(opCode,'execute')
isa.addInstruction(msrclr_Instr)

#MSRSET
opCode = cxx_writer.writer_code.Code("""

""")
msrset_Instr = trap.Instruction('MSRSET', True)
msrset_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0]}, 'TODO')
msrset_Instr.setCode(opCode,'execute')
isa.addInstruction(msrset_Instr)

#MTS
opCode = cxx_writer.writer_code.Code("""

""")
mts_Instr = trap.Instruction('MTS', True)
mts_Instr.setMachineCode(mts_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mts_Instr.setCode(opCode,'execute')
isa.addInstruction(mts_Instr)

#MUL
opCode = cxx_writer.writer_code.Code("""

""")
mul_Instr = trap.Instruction('MUL', True)
mul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
mul_Instr.setCode(opCode,'execute')
isa.addInstruction(mul_Instr)

#MULH
opCode = cxx_writer.writer_code.Code("""

""")
mulh_Instr = trap.Instruction('MULH', True)
mulh_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
mulh_Instr.setCode(opCode,'execute')
isa.addInstruction(mulh_Instr)

#MULHU
opCode = cxx_writer.writer_code.Code("""

""")
mulhu_Instr = trap.Instruction('MULHU', True)
mulhu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, 'TODO')
mulhu_Instr.setCode(opCode,'execute')
isa.addInstruction(mulhu_Instr)

#MULHSU
opCode = cxx_writer.writer_code.Code("""

""")
mulhsu_Instr = trap.Instruction('MULHSU', True)
mulhsu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, 'TODO')
mulhsu_Instr.setCode(opCode,'execute')
isa.addInstruction(mulhsu_Instr)

#MULI
opCode = cxx_writer.writer_code.Code("""

""")
muli_Instr = trap.Instruction('MULI', True)
muli_Instr.setMachineCode(oper_imm, {'opcode': [0,1,1,0,0,0]}, 'TODO')
muli_Instr.setCode(opCode,'execute')
isa.addInstruction(muli_Instr)

#OR
opCode = cxx_writer.writer_code.Code("""

""")
or_Instr = trap.Instruction('OR', True)
or_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
or_Instr.setCode(opCode,'execute')
isa.addInstruction(or_Instr)

#ORI
opCode = cxx_writer.writer_code.Code("""

""")
ori_Instr = trap.Instruction('ORI', True)
ori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,0]}, 'TODO')
ori_Instr.setCode(opCode,'execute')
isa.addInstruction(ori_Instr)

#PCMPBF
opCode = cxx_writer.writer_code.Code("""

""")
pcmpbf_Instr = trap.Instruction('PCMPBF', True)
pcmpbf_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpbf_Instr.setCode(opCode,'execute')
isa.addInstruction(pcmpbf_Instr)

#PCMPEQ
opCode = cxx_writer.writer_code.Code("""

""")
pcmpeq_Instr = trap.Instruction('PCMPEQ', True)
pcmpeq_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpeq_Instr.setCode(opCode,'execute')
isa.addInstruction(pcmpeq_Instr)

#PCMPNE
opCode = cxx_writer.writer_code.Code("""

""")
pcmpne_Instr = trap.Instruction('PCMPNE', True)
pcmpne_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpne_Instr.setCode(opCode,'execute')
isa.addInstruction(pcmpne_Instr)

#PUT / PUTD
#very strange instructions :)

#RSUB instruction family
#RSUB
opCode = cxx_writer.writer_code.Code("""

""")
rsub_Instr = trap.Instruction('RSUB', True)
rsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsub_Instr.setCode(opCode,'execute')
isa.addInstruction(rsub_Instr)

# RSUBC
opCode = cxx_writer.writer_code.Code("""

""")
rsubc_Instr = trap.Instruction('RSUBC', True)
rsubc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubc_Instr)

# RSUBK
opCode = cxx_writer.writer_code.Code("""

""")
rsubk_Instr = trap.Instruction('RSUBK', True)
rsubk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubk_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubk_Instr)

# RSUBKC
opCode = cxx_writer.writer_code.Code("""

""")
rsubkc_Instr = trap.Instruction('RSUBKC', True)
rsubkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubkc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubkc_Instr)

#RSUBI instruction family
#RSUBI
opCode = cxx_writer.writer_code.Code("""

""")
rsubi_Instr = trap.Instruction('RSUBI', True)
rsubi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,1]}, 'TODO')
rsubi_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubi_Instr)

#RSUBIC
opCode = cxx_writer.writer_code.Code("""

""")
rsubic_Instr = trap.Instruction('RSUBIC', True)
rsubic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,1]}, 'TODO')
rsubic_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubic_Instr)

#RSUBIK
opCode = cxx_writer.writer_code.Code("""

""")
rsubik_Instr = trap.Instruction('RSUBIK', True)
rsubik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,1]}, 'TODO')
rsubik_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubik_Instr)

#RSUBIKC
opCode = cxx_writer.writer_code.Code("""

""")
rsubikc_Instr = trap.Instruction('RSUBIKC', True)
rsubikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,1]}, 'TODO')
rsubikc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubikc_Instr)

#RETURN instruction family
#RTBD
opCode = cxx_writer.writer_code.Code("""

""")
rtbd_Instr = trap.Instruction('RTBD','True')
rtbd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,1,0]}, 'TODO')
rtbd_Instr.setCode(opCode,'execute')
isa.addInstruction(rtbd_Instr)

#RTID
opCode = cxx_writer.writer_code.Code("""

""")
rtid_Instr = trap.Instruction('RTID','True')
rtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,1]}, 'TODO')
rtid_Instr.setCode(opCode,'execute')
isa.addInstruction(rtid_Instr)

#RTED
opCode = cxx_writer.writer_code.Code("""

""")
rted_Instr = trap.Instruction('RTED','True')
rted_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,1,0,0]}, 'TODO')
rted_Instr.setCode(opCode,'execute')
isa.addInstruction(rted_Instr)

#RTSD
opCode = cxx_writer.writer_code.Code("""

""")
rtsd_Instr = trap.Instruction('RTSD','True')
rtsd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,0]}, 'TODO')
rtsd_Instr.setCode(opCode,'execute')
isa.addInstruction(rtsd_Instr)

#STORE instruction family
#SB
opCode = cxx_writer.writer_code.Code("""

""")
sb_Instr = trap.Instruction('SB', True)
sb_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sb_Instr.setCode(opCode,'execute')
isa.addInstruction(sb_Instr)

#SBI
opCode = cxx_writer.writer_code.Code("""

""")
sbi_Instr = trap.Instruction('SBI', True)
sbi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,0]}, 'TODO')
sbi_Instr.setCode(opCode,'execute')
isa.addInstruction(sbi_Instr)

#SH
opCode = cxx_writer.writer_code.Code("""

""")
sh_Instr = trap.Instruction('SH', True)
sh_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sh_Instr.setCode(opCode,'execute')
isa.addInstruction(sh_Instr)

#SHI
opCode = cxx_writer.writer_code.Code("""

""")
shi_Instr = trap.Instruction('SHI', True)
shi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,1]}, 'TODO')
shi_Instr.setCode(opCode,'execute')
isa.addInstruction(shi_Instr)

#SW
opCode = cxx_writer.writer_code.Code("""

""")
sw_Instr = trap.Instruction('SW', True)
sw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sw_Instr.setCode(opCode,'execute')
isa.addInstruction(sw_Instr)

#SWI
opCode = cxx_writer.writer_code.Code("""
""")
swi_Instr = trap.Instruction('SWI', True)
swi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,1,0]}, 'TODO')
swi_Instr.setCode(opCode,'execute')
isa.addInstruction(swi_Instr)

#SEXT16
opCode = cxx_writer.writer_code.Code("""

""")
sext16_Instr = trap.Instruction('SEXT16', True)
sext16_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1]}, 'TODO')
sext16_Instr.setCode(opCode,'execute')
isa.addInstruction(sext16_Instr)

#SEXT8
opCode = cxx_writer.writer_code.Code("""

""")
sext8_Instr = trap.Instruction('SEXT8', True)
sext8_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0]}, 'TODO')
sext8_Instr.setCode(opCode,'execute')
isa.addInstruction(sext8_Instr)

#SRA
opCode = cxx_writer.writer_code.Code("""

""")
sra_Instr = trap.Instruction('SRA', True)
sra_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
sra_Instr.setCode(opCode,'execute')
isa.addInstruction(sra_Instr)

#SRC
opCode = cxx_writer.writer_code.Code("""

""")
src_Instr = trap.Instruction('SRC', True)
src_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1]}, 'TODO')
src_Instr.setCode(opCode,'execute')
isa.addInstruction(src_Instr)

#SRL
opCode = cxx_writer.writer_code.Code("""

""")
srl_Instr = trap.Instruction('SRL', True)
srl_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]}, 'TODO')
srl_Instr.setCode(opCode,'execute')
isa.addInstruction(srl_Instr)

#WDC
opCode = cxx_writer.writer_code.Code("""

""")
wdc_Instr = trap.Instruction('WDC', True)
wdc_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,0,1,0,0]}, 'TODO')
wdc_Instr.setCode(opCode,'execute')
isa.addInstruction(wdc_Instr)

#WIC
opCode = cxx_writer.writer_code.Code("""

""")
wic_Instr = trap.Instruction('WIC', True)
wic_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,1,0,0,0]}, 'TODO')
wic_Instr.setCode(opCode,'execute')
isa.addInstruction(wic_Instr)

#XOR
opCode = cxx_writer.writer_code.Code("""

""")
xor_Instr = trap.Instruction('XOR', True)
xor_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
xor_Instr.setCode(opCode,'execute')
isa.addInstruction(xor_Instr)

#XORI
opCode = cxx_writer.writer_code.Code("""

""")
xori_Instr = trap.Instruction('XORI', True)
xori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,0]}, 'TODO')
xori_Instr.setCode(opCode,'execute')
isa.addInstruction(xori_Instr)