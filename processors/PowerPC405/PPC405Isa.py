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
#   (a) Luca Fossati, fossati@elet.polimi.it
#   (b) Redwanur Rahman, md.rahman@mail.polimi.it
#   (c) Ashanka Das, ashanka.das@mail.polimi.it
####################################################################################


# Lets first of all import the necessary files for the
# creation of the processor
import trap
import cxx_writer
from PPC405Coding import *
from PPC405Methods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()
#ADD
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
""")
add_Instr = trap.Instruction('ADD', True)
add_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(add_Instr)

#ADDC
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
if ((int)rb + (int)ra>exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addc_Instr)
#ADDE
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra + XER[CA];
if ((int)rb + (int)ra + XER[CA] > exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
adde_Instr = trap.Instruction('ADDE', True)
adde_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
adde_Instr.setCode(opCode,'execute')
adde_Instr.addBehavior(IncrementPC, 'execute')
adde_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(adde_Instr)
#ADDI
opCode = cxx_writer.writer_code.Code("""
rt = (((int) ra | 0) + exts(d);
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,1,0] }, ('addi r', '%rt', ' r ', '%ra', '  ', '%d'))
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
#addi_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addi_Instr)
#ADDIC 
opCode = cxx_writer.writer_code.Code("""
rt = (int) ra  + exts(d);
if (((int) ra  + exts(d))> (exp (2,32) -1))) XER[ca]=1;
else XER[ca]=o;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,0,0] }, ('addic r', '%rt', ' r ', '%ra', '  ', '%d'))
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
#addic_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addic_Instr)
#ADDIC. 
opCode = cxx_writer.writer_code.Code("""
rt = (int) ra  + exts(d);
if (((int) ra  + exts(d))> (exp (2,32) -1))) XER[ca]=1;
else XER[ca]=o;
""")
addicdot_Instr = trap.Instruction('ADDICDOT', True)
addicdot_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,0,1] }, ('addicdot r', '%rt', ' r ', '%ra', '  ', '%d'))
addicdot_Instr.setCode(opCode,'execute')
addicdot_Instr.addBehavior(IncrementPC, 'execute')
#addic_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addicdot_Instr)
#ADDIS
opCode = cxx_writer.writer_code.Code("""
rt = ((int) ra |0) + (d | 0);

""")
addis_Instr = trap.Instruction('ADDIS', True)
addis_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,1,1] }, ('addicdot r', '%rt', ' r ', '%ra', '  ', '%d'))
addis_Instr.setCode(opCode,'execute')
addis_Instr.addBehavior(IncrementPC, 'execute')
#addis_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addis_Instr)
#ADDME
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA]+(-1);
if ((int)ra + XER[CA]+0xFFFFFFFF > exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addme_Instr = trap.Instruction('ADDME', True)
addme_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,1,0]}, ('Add r', '%rt', ' r', '%ra'))
addme_Instr.setCode(opCode,'execute')
addme_Instr.addBehavior(IncrementPC, 'execute')
addme_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addme_Instr)
#ADDZE
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA];
if ((int)ra + XER[CA]> exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addze_Instr = trap.Instruction('ADDZE', True)
addze_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,0,0]}, ('Add r', '%rt', ' r', '%ra'))
addze_Instr.setCode(opCode,'execute')
addze_Instr.addBehavior(IncrementPC, 'execute')
addze_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addze_Instr)
#AND
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & (int)rb;
""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,0,1,0,1,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
and_Instr.setCode(opCode,'execute')
and_Instr.addBehavior(IncrementPC, 'execute')
#and_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x66440044, 'PC':0x4})
#and_Instr.addTest({'ra': 1, 'rs': 1, 'rb': 1}, {'GPR[1]': 0xab88cd77, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[1]': 0xab88cd77, 'PC':0x4})
isa.addInstruction(and_Instr)
#ANDC
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & ~((int)rb);
""")
andc_Instr = trap.Instruction('ANDC', True)
andc_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,1,0,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
andc_Instr.setCode(opCode,'execute')
andc_Instr.addBehavior(IncrementPC, 'execute')
#andc_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andc_Instr)
#ANDI 
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & (0x0000000000000000 |(int)si);
""")
andi_Instr = trap.Instruction('ANDI', True)
andi_Instr.setMachineCode(oper_Dform_2, {'primary_opcode': [0,1,1,1,0,0]}, ('and r', '%ra', ' r', '%rs', '  ', '%si'))
andi_Instr.setCode(opCode,'execute')
andi_Instr.addBehavior(IncrementPC, 'execute')
#andi_Instr.addTest({'ra': 3, 'rs': 1, ' ': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andi_Instr)
#ANDIS
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & ((int)si | 0x0000000000000000 );
""")
andis_Instr = trap.Instruction('ANDIS', True)
andis_Instr.setMachineCode(oper_Dform_2, {'primary_opcode': [0,1,1,1,0,1]}, ('and r', '%ra', ' r', '%rs', '  ', '%si'))
andis_Instr.setCode(opCode,'execute')
andis_Instr.addBehavior(IncrementPC, 'execute')
#andis_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andis_Instr)
#B register Mormat not found(oper_Iform may be but AA,LK not found)
opCode = cxx_writer.writer_code.Code("""
//if ( (int) aa ==1)
//LI ← target6:29
//NIA ← EXTS(LI || 20)
//else
//LI ← (target – CIA)6:29
//NIA ← CIA + EXTS(LI || 20)
//if LK = 1 
//(LR) ← CIA + 4
//PC ← NIA
""")
b_Instr = trap.Instruction('B', True)
b_Instr.setMachineCode(oper_Iform, {'primary_opcode': [0,1,0,0,1,0]}, ('TODO'))
b_Instr.setCode(opCode,'execute')
b_Instr.addBehavior(IncrementPC, 'execute')
#b_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(b_Instr)
#BC
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bc_Instr = trap.Instruction('BC', True)
bc_Instr.setMachineCode(oper_Bform, {'primary_opcode': [0,1,0,0,0,0]}, ('TODO'))
bc_Instr.setCode(opCode,'execute')
bc_Instr.addBehavior(IncrementPC, 'execute')
#bc_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bc_Instr)
#BCCTR
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bccrt_Instr = trap.Instruction('BCCRT', True)
bccrt_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,0,0,1,1], 'xo': [1,0,0,0,0,1,0,0,0,0]}, ('TODO'))
bccrt_Instr.setCode(opCode,'execute')
bccrt_Instr.addBehavior(IncrementPC, 'execute')
#bccrt_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bccrt_Instr)
#BCLR
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bclr_Instr = trap.Instruction('BCLR', True)
bclr_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,0,1,0,0,0,0]}, ('TODO'))
bclr_Instr.setCode(opCode,'execute')
bclr_Instr.addBehavior(IncrementPC, 'execute')
#bclr_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bclr_Instr)
#CMP
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmp_Instr = trap.Instruction('CMP', True)
cmp_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,0,0,0,0,0]}, ('cmp r', '%bf', ' r', '%ra', ' r', '%rb'))
cmp_Instr.setCode(opCode,'execute')
cmp_Instr.addBehavior(IncrementPC, 'execute')
#cmp_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmp_Instr)
#CMPI
opCode = cxx_writer.writer_code.Code("""
int c0=0,c1=0,c2=0,c3=0;
if (int)ra < exts(im_si) c0=1;
if (int)ra > exts(im_si) c1=1;
if (int)ra = exts(im_si) c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpi_Instr = trap.Instruction('CMPI', True)
cmpi_Instr.setMachineCode(oper_Dform_5, {'primary_opcode': [0,0,1,0,1,1]}, ('cmpi r', '%bf', ' r', '%ra')) # need to check
cmpi_Instr.setCode(opCode,'execute')
cmpi_Instr.addBehavior(IncrementPC, 'execute')
#cmpi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpi_Instr)
#CMPL
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpl_Instr = trap.Instruction('CMPL', True)
cmpl_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,0,0,0,0,0]}, ('cmpl r', '%bf', ' r', '%ra'))
cmpl_Instr.setCode(opCode,'execute')
cmpl_Instr.addBehavior(IncrementPC, 'execute')
#cmpl_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpl_Instr)
#CMPLI
opCode = cxx_writer.writer_code.Code("""
int c0=0,c1=0,c2=0,c3=0;
if (int)ra < exts(im_si) c0=1;
if (int)ra > exts(im_si) c1=1;
if (int)ra = exts(im_si) c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpli_Instr = trap.Instruction('CMPLI', True)
cmpli_Instr.setMachineCode(oper_Dform_5, {'primary_opcode': [0,0,1,0,1,0]}, ('cmpi r', '%bf', ' r', '%ra')) # need to check
cmpli_Instr.setCode(opCode,'execute')
cmpli_Instr.addBehavior(IncrementPC, 'execute')
#cmpli_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpli_Instr)
#CNTLZW
opCode = cxx_writer.writer_code.Code("""
int n=0;
do{
if (int) ra = 1 ;
else	{
 	n = n+1;
	ra=n;
	}
}while(n<32);
""")
cntlzw_Instr = trap.Instruction('CNTLZW', True)
cntlzw_Instr.setMachineCode(oper_Xform_13, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,0,1,1,0,1,0]}, ('cntlzw r', '%ra', ' r', '%rs'))
cntlzw_Instr.setCode(opCode,'execute')
cntlzw_Instr.addBehavior(IncrementPC, 'execute')
#cntlzw_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cntlzw_Instr)
#CRAND
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba & (int)bb;
""")
crand_Instr = trap.Instruction('CRAND', True)
crand_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,0,0,0,0,0,0,0,1]}, ('crand r', '%bt', ' r', '%ba', ' r', '%bb'))
crand_Instr.setCode(opCode,'execute')
crand_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crand_Instr)
#CRANDC
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba &  ~((int)bb);
""")
crandc_Instr = trap.Instruction('CRANDC', True)
crandc_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,0,0,0,0,0,0,1]}, ('crand r', '%bt', ' r', '%ba', ' r', '%bb'))
crandc_Instr.setCode(opCode,'execute')
crandc_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crandc_Instr)
#CREQV
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba|(int) bb) &  ~((int) ba & (int)bb));
//(a || b) && !(a && b) xor
""")
creqv_Instr = trap.Instruction('CREQV', True)
creqv_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,0,0,1,0,0,0,0,1]}, ('creqv r', '%bt', ' r', '%ba', ' r', '%bb'))
creqv_Instr.setCode(opCode,'execute')
creqv_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(creqv_Instr)
#CRNAND
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba & (int) bb);
""")
crnand_Instr = trap.Instruction('CRNAND', True)
crnand_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,1,1,0,0,0,0,1]}, ('crnand r', '%bt', ' r', '%ba', ' r', '%bb'))
crnand_Instr.setCode(opCode,'execute')
crnand_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crnand_Instr)
#CRNOR
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba|(int) bb);
""")
crnor_Instr = trap.Instruction('CRNOR', True)
crnor_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,0,0,1,0,0,0,0,1]}, ('crnor r', '%bt', ' r', '%ba', ' r', '%bb'))
crnor_Instr.setCode(opCode,'execute')
crnor_Instr.addBehavior(IncrementPC, 'execute')
#crnor_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crnor_Instr)
#CROR
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba|(int) bb;
""")
cror_Instr = trap.Instruction('CROR', True)
cror_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,1,1,0,0,0,0,0,1]}, ('cror r', '%bt', ' r', '%ba', ' r', '%bb'))
cror_Instr.setCode(opCode,'execute')
cror_Instr.addBehavior(IncrementPC, 'execute')
#cror_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cror_Instr)
#CRORC
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba| ~((int) bb);
""")
crorc_Instr = trap.Instruction('CRORC', True)
crorc_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,1,0,1,0,0,0,0,1]}, ('crorc r', '%bt', ' r', '%ba', ' r', '%bb'))
crorc_Instr.setCode(opCode,'execute')
crorc_Instr.addBehavior(IncrementPC, 'execute')
#crorc_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crorc_Instr)
#CRXOR
opCode = cxx_writer.writer_code.Code("""
bt = ((int) ba|(int) bb) &  ~((int) ba & (int)bb));
""")
crxor_Instr = trap.Instruction('CRXOR', True)
crxor_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,1,0,0,0,0,0,1]}, ('crxor r', '%bt', ' r', '%ba', ' r', '%bb'))
crxor_Instr.setCode(opCode,'execute')
crxor_Instr.addBehavior(IncrementPC, 'execute')
#crxor_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crxor_Instr)
#DCBA
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcba(ea);
""")
dcba_Instr = trap.Instruction('DCBA', True)
dcba_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,1,1,1,1,0,1,1,0]}, ('dcba r', '%ra', ' r', '%rb'))
dcba_Instr.setCode(opCode,'execute')
dcba_Instr.addBehavior(IncrementPC, 'execute')
#dcba_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcba_Instr)
#DCBF
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcbf(ea);
""")
dcbf_Instr = trap.Instruction('DCBF', True)
dcbf_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,1,0,1,0,1,1,0]}, ('dcbf r', '%ra', ' r', '%rb'))
dcbf_Instr.setCode(opCode,'execute')
dcbf_Instr.addBehavior(IncrementPC, 'execute')
#dcbf_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbf_Instr)
#DCBI
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcbi(ea);
""")
dcbi_Instr = trap.Instruction('DCBI', True)
dcbi_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,0,1,0,1,1,0]}, ('dcbi r', '%ra', ' r', '%rb'))
dcbi_Instr.setCode(opCode,'execute')
dcbi_Instr.addBehavior(IncrementPC, 'execute')
#dcbi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbi_Instr)
#DCBST
opCode = cxx_writer.writer_code.Code("""ea = (((int) ra|0) + (int) ba);
//dcbst(ea);
""")
dcbst_Instr = trap.Instruction('DCBST', True)
dcbst_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,1,1,0,1,1,0]}, ('dcbst r', '%ra', ' r', '%rb'))
dcbst_Instr.setCode(opCode,'execute')
dcbst_Instr.addBehavior(IncrementPC, 'execute')
#dcbst_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbst_Instr)
#DCBT
opCode = cxx_writer.writer_code.Code("""ea = (((int) ra|0) + (int) ba);
//dcbt(ea);
""")
dcbt_Instr = trap.Instruction('DCBT', True)
dcbt_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,0,0,1,0,1,1,0]}, ('dcbt r', '%ra', ' r', '%rb'))
dcbt_Instr.setCode(opCode,'execute')
dcbt_Instr.addBehavior(IncrementPC, 'execute')
#dcbt_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbt_Instr)
#DCBTST
opCode = cxx_writer.writer_code.Code("""ea = (((int) ra|0) + (int) ba);
//dcbtst(ea);
""")
dcbtst_Instr = trap.Instruction('DCBTST', True)
dcbtst_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,1,1,1,1,0,1,1,0]}, ('dcbtst r', '%ra', ' r', '%rb'))
dcbtst_Instr.setCode(opCode,'execute')
dcbtst_Instr.addBehavior(IncrementPC, 'execute')
#dcbtst_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbtst_Instr)
#DCBZ
opCode = cxx_writer.writer_code.Code("""ea = (((int) ra|0) + (int) ba);
//dcbz(ea);
""")
dcbz_Instr = trap.Instruction('DCBZ', True)
dcbz_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,1,1,1,0,1,1,0]}, ('dcbz r', '%ra', ' r', '%rb'))
dcbz_Instr.setCode(opCode,'execute')
dcbz_Instr.addBehavior(IncrementPC, 'execute')
#dcbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbz_Instr)
#DCCCI
opCode = cxx_writer.writer_code.Code("""ea = (((int) ra|0) + (int) ba);
//dcbtst(ea);
""")
dccci_Instr = trap.Instruction('DCCCI', True)
dccci_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,0,0,0,1,1,0]}, ('dccci r', '%ra', ' r', '%rb'))
dccci_Instr.setCode(opCode,'execute')
dccci_Instr.addBehavior(IncrementPC, 'execute')
#dccci_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dccci_Instr)
#DCREAD
#DIVW
#DIVWU
#EIEIO
#EQV
#EXTSB
#EXTSH
#ICBI
#ICBT
#ICCCI
#ICREAD
#ISYNC
#LBZ
#LBZU
#LBZUX
#LBZX
#LHA
#LHAU
#LHAUX
#LHAX
#LHBRX
#LHZ
#LHZU
#LHZUX
#LHZX
#LMW
#LSWI
#LSWX
#LWARX
#LWBRX
#LWZ
#LWZU
#LWZUX
#LWZX
#MACCHW
#MACCHWS
#MACCHWSU
#MACCHWU
#MACHHW
#MACHHWS
#MACHHWSU
#MACHHWU
#MACLHW
#MACLHWS
#MACLHWSU
#MACLHWU
#MCRF
#MCRXR
#MFCR
#MFDCR
#MFMSR
#MFSPR
#MFTB
#MTCRF
#MTDCR
#MTMSR
#MTSPR
#MULCHW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; //rb is signed
""")
mulchw_Instr = trap.Instruction('MULCHW', True)
mulchw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,1,0,1,0,0,0]}, ('mulchw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulchw_Instr.setCode(opCode,'execute')
mulchw_Instr.addBehavior(IncrementPC, 'execute')
#mulchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulchw_Instr)
#MULCHWU
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(unsigned)rb; //rb is unsigned
""")
mulchwu_Instr = trap.Instruction('MULCHWU', True)
mulchwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,0,0,1,0,0,0]}, ('mulchwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulchwu_Instr.setCode(opCode,'execute')
mulchwu_Instr.addBehavior(IncrementPC, 'execute')
#mulchwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulchwu_Instr)

#MULHHW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; //rb is signed
""")
mulhhw_Instr = trap.Instruction('MULHHW', True)
mulhhw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,1,0,1,0,0,0]}, ('mulhhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhhw_Instr.setCode(opCode,'execute')
mulhhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhhw_Instr)

#MULHHWU
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(unsigned)rb; //rb is unsigned
""")
mulhhwu_Instr = trap.Instruction('MULHHWU', True)
mulhhwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,0,0,1,0,0,0]}, ('mulhhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhhwu_Instr.setCode(opCode,'execute')
mulhhwu_Instr.addBehavior(IncrementPC, 'execute')
#mulhhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhhwu_Instr)

#MULHW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; //rb is signed
//prod0:63 ← (RA) × (RB) signed
//(RT) ← prod0:31
""")
mulhw_Instr = trap.Instruction('MULHW', True)
mulhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,1,0,1,1]}, ('mulhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhw_Instr.setCode(opCode,'execute')
mulhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhw_Instr)

#MULHWU
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(unsigned)rb; //rb is unsigned
//prod0:63 ← (RA) × (RB) unsigned
//(RT) ← prod0:31
""")
mulhwu_Instr = trap.Instruction('MULHWU', True)
mulhwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,0,1,1]}, ('mulhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhwu_Instr.setCode(opCode,'execute')
mulhwu_Instr.addBehavior(IncrementPC, 'execute')
#mulhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhwu_Instr)

#MULLHW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; //rb is signed
//(RT)0:31 ← (RA)16:31 x (RB)16:31 signed
""")
mullhw_Instr = trap.Instruction('MULLHW', True)
mullhw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,1,0,1,0,0,0]}, ('mullhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mullhw_Instr.setCode(opCode,'execute')
mullhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullhw_Instr)

#MULLHWU
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; //rb is signed
//(RT)0:31 ← (RA)16:31 x (RB)16:31 unsigned
""")
mullhwu_Instr = trap.Instruction('MULLHWU', True)
mullhwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,0,0,1,0,0,0]}, ('mullhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mullhwu_Instr.setCode(opCode,'execute')
mullhwu_Instr.addBehavior(IncrementPC, 'execute')
#mullhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullhwu_Instr)
#MULLI
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * exts(im); 
//prod0:47 ← (RA) × EXTS(IM) signed
//(RT) ← prod16:47
""")
mulli_Instr = trap.Instruction('MULLI', True)
mulli_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [0,0,0,1,1,1] }, ('mulli r', '%rt', ' r', '%ra'))
mulli_Instr.setCode(opCode,'execute')
mulli_Instr.addBehavior(IncrementPC, 'execute')
#mulli_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulli_Instr)

#MULLW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; 
//prod0:63 ← (RA) × (RB) signed
//(RT) ← prod32:63
""")
mullw_Instr = trap.Instruction('MULLW', True)
mullw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,1,1]}, ('mullw r', '%rt', ' r', '%ra', ' r', '%rb'))
mullw_Instr.setCode(opCode,'execute')
mullw_Instr.addBehavior(IncrementPC, 'execute')
#mullw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullw_Instr)

#NAND
opCode = cxx_writer.writer_code.Code("""
ra = !((int)rs && (int)rb); 
//(RA) ← ¬((RS) ∧ (RB))
""")
nand_Instr = trap.Instruction('NAND', True)
nand_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,1,1,0,0]}, ('nand r', '%rt', ' r', '%ra', ' r', '%rb'))
nand_Instr.setCode(opCode,'execute')
nand_Instr.addBehavior(IncrementPC, 'execute')
#nand_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nand_Instr)

#NEG
opCode = cxx_writer.writer_code.Code("""
rt = !((int)ra) + 1; 
//(RT) ← ¬(RA) + 1
""")
neg_Instr = trap.Instruction('NEG', True)
neg_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,1,0,0,0]}, ('neg r', '%rt', ' r', '%ra'))
neg_Instr.setCode(opCode,'execute')
neg_Instr.addBehavior(IncrementPC, 'execute')
#neg_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(neg_Instr)

#NMACCHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmacchw_Instr = trap.Instruction('NMACCHW', True)
nmacchw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,1,0,1,1,1,0]}, ('nmacchw r', '%rt', ' r', '%ra', ' r', '%rb'))
nmacchw_Instr.setCode(opCode,'execute')
nmacchw_Instr.addBehavior(IncrementPC, 'execute')
#nmacchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmacchw_Instr)

#NMACCHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)0:15 signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmacchws_Instr = trap.Instruction('NMACCHWS', True)
nmacchws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,1,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmacchws_Instr.setCode(opCode,'execute')
nmacchws_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmacchws_Instr)

#NMACHHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)0:15 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmachhw_Instr = trap.Instruction('NMACHHW', True)
nmachhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmachhw_Instr.setCode(opCode,'execute')
nmachhw_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmachhw_Instr)

#NMACHHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)0:15 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmachhws_Instr = trap.Instruction('NMACHHWS', True)
nmachhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,1,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmachhws_Instr.setCode(opCode,'execute')
nmachhws_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmachhws_Instr)

#NMACLHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)16:31) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmaclhw_Instr = trap.Instruction('NMACLHW', True)
nmaclhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,1,0,1,1,1,0]}, ('nmaclhw r', '%rt', ' r', '%ra', ' r', '%rb'))
nmaclhw_Instr.setCode(opCode,'execute')
nmaclhw_Instr.addBehavior(IncrementPC, 'execute')
#nmaclhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmaclhw_Instr)

#NMACLHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)16:31) signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmaclhws_Instr = trap.Instruction('NMACLHWS', True)
nmaclhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,1,1,0,1,1,1,0]}, ('nmaclhws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmaclhws_Instr.setCode(opCode,'execute')
nmaclhws_Instr.addBehavior(IncrementPC, 'execute')
#nmaclhws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmaclhws_Instr)

#NOR
opCode = cxx_writer.writer_code.Code("""
ra = !((int)rs || (int)rb)
//(RA) ← ¬((RS) ∨ (RB))
""")
nor_Instr = trap.Instruction('NOR', True)
nor_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,1,1,1,1,1,0,0]}, ('nor r', '%rt', ' r', '%ra', ' r', '%rb'))
nor_Instr.setCode(opCode,'execute')
nor_Instr.addBehavior(IncrementPC, 'execute')
#nor_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nor_Instr)

#OR
opCode = cxx_writer.writer_code.Code("""
ra = ((int)rs || (int)rb)
//(RA) ← (RS) ∨ (RB)
""")
or_Instr = trap.Instruction('OR', True)
or_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,0,1,1,1,1,0,0]}, ('or r', '%rs', ' r', '%ra', ' r', '%rb'))
or_Instr.setCode(opCode,'execute')
or_Instr.addBehavior(IncrementPC, 'execute')
#or_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(or_Instr)

#ORC
opCode = cxx_writer.writer_code.Code("""
ra = ((int)rs || !(int)rb)
//(RA) ← (RS) ∨ ¬(RB)
""")
orc_Instr = trap.Instruction('ORC', True)
orc_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,0,0,1,1,1,0,0]}, ('orc r', '%rt', ' r', '%ra', ' r', '%rb'))
orc_Instr.setCode(opCode,'execute')
orc_Instr.addBehavior(IncrementPC, 'execute')
#orc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(orc_Instr)

#ORI
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ∨ (16:0 || IM)
""")
ori_Instr = trap.Instruction('ORI', True)
ori_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,0,0] }, ('ori r', '%rs', ' r', '%ra'))
ori_Instr.setCode(opCode,'execute')
ori_Instr.addBehavior(IncrementPC, 'execute')
#ori_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(ori_Instr)

#ORIS
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ∨ (IM || 16:0)
""")
oris_Instr = trap.Instruction('ORIS', True)
oris_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,0,1] }, ('oris r', '%rs', ' r', '%ra'))
oris_Instr.setCode(opCode,'execute')
oris_Instr.addBehavior(IncrementPC, 'execute')
#oris_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(oris_Instr)

#RFCI
opCode = cxx_writer.writer_code.Code("""
//(PC) ← (SRR2)
//(MSR) ← (SRR3)
""")
rfci_Instr = trap.Instruction('RFCI', True)
rfci_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,1,1,0,0,1,1] }, ())
rfci_Instr.setCode(opCode,'execute')
rfci_Instr.addBehavior(IncrementPC, 'execute')
#rfci_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rfci_Instr)

#RFI
opCode = cxx_writer.writer_code.Code("""
//(PC) ← (SRR0)
//(MSR) ← (SRR1)
""")
rfi_Instr = trap.Instruction('RFI', True)
rfi_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,1,1,0,0,1,0] }, ())
rfi_Instr.setCode(opCode,'execute')
rfi_Instr.addBehavior(IncrementPC, 'execute')
#rfi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rfi_Instr)

#RLWIMI
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← (r ∧ m) ∨ ((RA) ∧ ¬m)
""")
rlwimi_Instr = trap.Instruction('RLWIMI', True)
rlwimi_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,0,0] }, ('rlwimi r', '%rs', ' r', '%ra'))
rlwimi_Instr.setCode(opCode,'execute')
rlwimi_Instr.addBehavior(IncrementPC, 'execute')
#rlwimi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwimi_Instr)

#RLWINM
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← r ∧ m
""")
rlwinm_Instr = trap.Instruction('RLWINM', True)
rlwinm_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,0,1] }, ('rlwinm r', '%rs', ' r', '%ra'))
rlwinm_Instr.setCode(opCode,'execute')
rlwinm_Instr.addBehavior(IncrementPC, 'execute')
#rlwinm_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwinm_Instr)

#RLWNM
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← r ∧ m
""")
rlwnm_Instr = trap.Instruction('RLWNM', True)
rlwnm_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,1,1] }, ('rlwnm r', '%rs', ' r', '%ra'))
rlwnm_Instr.setCode(opCode,'execute')
rlwnm_Instr.addBehavior(IncrementPC, 'execute')
#rlwnm_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwnm_Instr)

#SC
opCode = cxx_writer.writer_code.Code("""
//(SRR1) ← (MSR)
//(SRR0) ← (PC)
//PC ← EVPR0:15 || 0x0C00
//(MSR[WE, EE, PR, DR, IR]) ← 0
""")
sc_Instr = trap.Instruction('SC', True)
sc_Instr.setMachineCode(oper_SCform, {'primary_opcode': [0,1,0,0,0,1] , '1':[1] }, ())
sc_Instr.setCode(opCode,'execute')
sc_Instr.addBehavior(IncrementPC, 'execute')
#sc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sc_Instr)

#SLW
opCode = cxx_writer.writer_code.Code("""
//n ← (RB)27:31
//r ← ROTL((RS), n)
//if (RB)26 = 0 then
//    m ← MASK(0, 31 – n)
//else
//    m ← 320
//(RA) ← r ∧ m
""")
slw_Instr = trap.Instruction('SLW', True)
slw_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,1,0,0,0] }, ('slw r', '%rs', ' r', '%ra', ' r', '%rb'))
slw_Instr.setCode(opCode,'execute')
slw_Instr.addBehavior(IncrementPC, 'execute')
#slw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(slw_Instr)

#SRAW
opCode = cxx_writer.writer_code.Code("""
//n ← (RB)27:31
//r ← ROTL((RS), 32 – n)
//if (RB)26 = 0 then
//    m ← MASK(n, 31)
//else
//    m ← 320
//s ← (RS)0
//(RA) ← (r ∧ m) ∨ (32s ∧ ¬m)
//XER[CA] ← s ∧ ((r ∧ ¬m) ≠ 0)
""")
sraw_Instr = trap.Instruction('SRAW', True)
sraw_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,0,0,0,1,1,0,0,0] }, ('sraw r', '%rs', ' r', '%ra', ' r', '%rb'))
sraw_Instr.setCode(opCode,'execute')
sraw_Instr.addBehavior(IncrementPC, 'execute')
#sraw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sraw_Instr)

