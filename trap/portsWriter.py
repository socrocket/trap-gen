################################################################################
#
#  _/_/_/_/_/  _/_/_/           _/        _/_/_/
#     _/      _/    _/        _/_/       _/    _/
#    _/      _/    _/       _/  _/      _/    _/
#   _/      _/_/_/        _/_/_/_/     _/_/_/
#  _/      _/    _/     _/      _/    _/
# _/      _/      _/  _/        _/   _/
#
# @file     portsWriter.py
# @brief    This file is part of the TRAP processor generator module.
# @details
# @author   Luca Fossati
# @author   Lillian Tadros (Technische Universitaet Dortmund)
# @date     2008-2013 Luca Fossati
#           2015-2016 Technische Universitaet Dortmund
# @copyright
#
# This file is part of TRAP.
#
# TRAP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# or see <http://www.gnu.org/licenses/>.
#
# (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
################################################################################

import cxx_writer

def getCPPExternalPorts(self, model, namespace):
    if len(self.tlmPorts) == 0:
        return None
    # creates the processor external TLM ports used for the
    # communication with the external world
    archDWordType = self.bitSizes[0]
    archWordType = self.bitSizes[1]
    archHWordType = self.bitSizes[2]
    archByteType = self.bitSizes[3]

    from procWriter import resourceType

    if self.isBigEndian:
        swapDEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapDEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapDEndianessCode += str(archWordType) + ' datum1 = (' + str(archWordType) + ')(datum);\nthis->swap_endianess(datum1);\n'
    swapDEndianessCode += str(archWordType) + ' datum2 = (' + str(archWordType) + ')(datum >> ' + str(self.wordSize*self.byteSize) + ');\nthis->swap_endianess(datum2);\n'
    swapDEndianessCode += 'datum = datum1 | (((' + str(archDWordType) + ')datum2) << ' + str(self.wordSize*self.byteSize) + ');\n#endif\n'

    swapEndianessCode = '// Endianess conversion: The processor is always modeled with the host endianess. In case they are different, the endianess is swapped.'
    if self.isBigEndian:
        swapEndianessDefine = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapEndianessDefine = '#ifdef BIG_ENDIAN_BO\n'

    swapEndianessCode += swapEndianessDefine + 'this->swap_endianess(datum);\n#endif\n'

    tlmPortElements = []

    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')

    MemoryToolsIfType = cxx_writer.TemplateType('MemoryToolsIf', [str(archWordType)], 'common/tools_if.hpp')
    tlmPortElements.append(cxx_writer.Attribute('debugger', MemoryToolsIfType.makePointer(), 'pri'))
    setDebuggerBody = cxx_writer.Code('this->debugger = debugger;')
    tlmPortElements.append(cxx_writer.Method('set_debugger', setDebuggerBody, cxx_writer.voidType, 'pu', [cxx_writer.Parameter('debugger', MemoryToolsIfType.makePointer())]))
    checkWatchPointCode = """if (this->debugger != NULL) {
        this->debugger->notify_address(address, sizeof(datum));
    }
    """

    memIfType = cxx_writer.Type('MemoryInterface', '#include \"memory.hpp\"')
    tlm_dmiType = cxx_writer.Type('tlm::tlm_dmi', 'tlm.h')
    TLMMemoryType = cxx_writer.Type('TLMMemory')
    tlminitsocketType = cxx_writer.TemplateType('tlm_utils::simple_initiator_socket', [TLMMemoryType, self.wordSize*self.byteSize], 'tlm_utils/simple_initiator_socket.h')
    payloadType = cxx_writer.Type('tlm::tlm_generic_payload', 'tlm.h')
    phaseType = cxx_writer.Type('tlm::tlm_phase', 'tlm.h')
    sync_enumType = cxx_writer.Type('tlm::tlm_sync_enum', 'tlm.h')
    tlmPortInit = []
    constructorParams = []

    emptyBody = cxx_writer.Code('')

    if model.endswith('AT'):
        # Some helper methods used only in the Approximate Timed coding style
        helperCode = """// TLM-2 backward non-blocking transport method.
            // The timing annotation must be honored.
            m_peq.notify(trans, phase, delay);
            return tlm::TLM_ACCEPTED;
            """
        helperBody = cxx_writer.Code(helperCode)
        transParam = cxx_writer.Parameter('trans', payloadType.makeRef())
        phaseParam = cxx_writer.Parameter('phase', phaseType.makeRef())
        delayParam = cxx_writer.Parameter('delay', cxx_writer.sc_timeType.makeRef())
        helperDecl = cxx_writer.Method('nb_transport_bw', helperBody, sync_enumType, 'pu', [transParam, phaseParam, delayParam], inline = True, noException = True)
        tlmPortElements.append(helperDecl)

        helperCode = """// Payload event queue callback to handle transactions from target.
            // Transaction could have arrived through return path or backward path.
            if (phase == tlm::END_REQ || (&trans == request_in_progress && phase == tlm::BEGIN_RESP)) {
                // The end of the BEGIN_REQ phase.
                request_in_progress = NULL;
                end_request_event.notify();
            } else if (phase == tlm::BEGIN_REQ || phase == tlm::END_RESP) {
                SC_REPORT_FATAL("TLM-2", "Illegal transaction phase received by initiator");
            }

            if (phase == tlm::BEGIN_RESP) {
                if (trans.is_response_error()) {
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
                }

                // Send final phase transition to target.
                tlm::tlm_phase fw_phase = tlm::END_RESP;
                sc_time delay = SC_ZERO_TIME;
                init_socket->nb_transport_fw(trans, fw_phase, delay);
                if (trans.is_response_error()) {
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + \
                        trans.get_response_string()).c_str());
                }
                this->end_response_event.notify(delay);
            }
            """
        helperBody = cxx_writer.Code(helperCode)
        phaseParam = cxx_writer.Parameter('phase', phaseType.makeRef().makeConst())
        helperDecl = cxx_writer.Method('peq_cb', helperBody, cxx_writer.voidType, 'pu', [transParam, phaseParam])
        tlmPortElements.append(helperDecl)

        tlmPortElements.append(cxx_writer.Attribute('request_in_progress', payloadType.makePointer(), 'pri'))
        tlmPortElements.append(cxx_writer.Attribute('end_request_event', cxx_writer.sc_eventType, 'pri'))
        tlmPortElements.append(cxx_writer.Attribute('end_response_event', cxx_writer.sc_eventType, 'pri'))

    if model.endswith('LT'):
        readCode = """ datum = 0;
            if (this->dmi_ptr_valid) {
                if (address + this->dmi_data.get_start_address() > this->dmi_data.get_end_address()) {
                    SC_REPORT_ERROR("TLM-2", "Error in reading memory data through DMI: address out of bounds");
                }
                memcpy(&datum, this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, sizeof(datum));
            """
        if not model.startswith('acc'):
            readCode += """this->quant_keeper.inc(this->dmi_data.get_read_latency());
            if (this->quant_keeper.need_sync()) {
                this->quant_keeper.sync();
            }
            """
        else:
            readCode += 'wait(this->dmi_data.get_read_latency());'
        readCode += """
            } else {
            """
        if not model.startswith('acc'):
            readCode += 'sc_time delay = this->quant_keeper.get_local_time();'
        else:
            readCode += 'sc_time delay = SC_ZERO_TIME;'
        readCode += """
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_read();
                trans.set_data_ptr(reinterpret_cast<unsigned char*>(&datum));
                trans.set_data_length(sizeof(datum));
                trans.set_streaming_width(sizeof(datum));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
                this->init_socket->b_transport(trans, delay);

                if (trans.is_response_error()) {
                    std::string error_str("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", error_str.c_str());
                }
                if (trans.is_dmi_allowed()) {
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->init_socket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                // Keep track of time.
            """
        if not model.startswith('acc'):
            readCode += """this->quant_keeper.set(delay);
                if (this->quant_keeper.need_sync()) {
                    this->quant_keeper.sync();
                }
            }
            """
        else:
            readCode += 'wait(delay);\n}\n'
    else:
        readCode = """ datum = 0;
        tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        trans.set_data_ptr(reinterpret_cast<unsigned char*>(&datum));
        trans.set_data_length(sizeof(datum));
        trans.set_streaming_width(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if (this->request_in_progress != NULL) {
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Forward non-blocking transport method.
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = init_socket->nb_transport_fw(trans, phase, delay);

        if (trans.is_response_error()) {
            std::string error_str("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", error_str.c_str());
        }

        // Check value returned from nb_transport_fw().
        if (status == tlm::TLM_UPDATED) {
            // The timing annotation must be honored.
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        } else if (status == tlm::TLM_COMPLETED) {
            // The completion of the transaction necessarily ends the BEGIN_REQ phase.
            this->request_in_progress = NULL;
            // The target has terminated the transaction, check the correctness.
            if (trans.is_response_error()) {
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """

    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\nreturn this->' + alias.alias + ';\n}\n'
    addressParam = cxx_writer.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.Code(readMemAliasCode + str(archDWordType) + readCode + swapDEndianessCode + '\nreturn datum;')
    readBody.addInclude('common/report.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.Code(readMemAliasCode + str(archWordType) + readCode + swapEndianessCode + '\nreturn datum;')
    readDecl = cxx_writer.Method('read_word', readBody, archWordType, 'pu', [addressParam], inline = True, noException = True)
    tlmPortElements.append(readDecl)
    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn (' + str(archHWordType) + ')' + alias.alias + '_temp;\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archHWordType) + ' *)&(' + alias.alias + '_temp)) + 1);\n}\n'
    readBody = cxx_writer.Code(readMemAliasCode + str(archHWordType) + readCode + swapEndianessCode + '\nreturn datum;')
    readDecl = cxx_writer.Method('read_half', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn (' + str(archByteType) + ')' + alias.alias + '_temp;\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 1);\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 2);\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 3);\n}\n'
    readBody = cxx_writer.Code(readMemAliasCode + str(archByteType) + readCode + '\nreturn datum;')
    readDecl = cxx_writer.Method('read_byte', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    writeCode = ''
    if model.endswith('LT'):
        writeCode += """if (this->dmi_ptr_valid) {
                if (address + this->dmi_data.get_start_address() > this->dmi_data.get_end_address()) {
                    SC_REPORT_ERROR("TLM-2", "Error in writing memory data through DMI: address out of bounds");
                }
                memcpy(this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, &datum, sizeof(datum));
            """
        if not model.startswith('acc'):
            writeCode += """this->quant_keeper.inc(this->dmi_data.get_write_latency());
            if (this->quant_keeper.need_sync()) {
                this->quant_keeper.sync();
            }"""
        else:
            writeCode += 'wait(this->dmi_data.get_write_latency());'
        writeCode += """
            } else {
            """
        if not model.startswith('acc'):
            writeCode += 'sc_time delay = this->quant_keeper.get_local_time();'
        else:
            writeCode += 'sc_time delay = SC_ZERO_TIME;'
        writeCode += """
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_write();
                trans.set_data_ptr((unsigned char*)&datum);
                trans.set_data_length(sizeof(datum));
                trans.set_streaming_width(sizeof(datum));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
                this->init_socket->b_transport(trans, delay);

                if (trans.is_response_error()) {
                    std::string error_str("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", error_str.c_str());
                }
                if (trans.is_dmi_allowed()) {
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->init_socket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                // Keep track of time.
            """
        if not model.startswith('acc'):
            writeCode += """this->quant_keeper.set(delay);
                if (this->quant_keeper.need_sync()) {
                    this->quant_keeper.sync();
                }
            }
            """
        else:
            writeCode += 'wait(delay);\n}\n'
    else:
        writeCode += """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        trans.set_data_ptr((unsigned char*)&datum);
        trans.set_data_length(sizeof(datum));
        trans.set_streaming_width(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if (this->request_in_progress != NULL) {
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Forward non-blocking transport method.
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = init_socket->nb_transport_fw(trans, phase, delay);

        if (trans.is_response_error()) {
            std::string error_str("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", error_str.c_str());
        }

        // Check value returned from nb_transport_fw().
        if (status == tlm::TLM_UPDATED) {
            // The timing annotation must be honored.
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        } else if (status == tlm::TLM_COMPLETED) {
            // The completion of the transaction necessarily ends the BEGIN_REQ phase.
            this->request_in_progress = NULL;
            // The target has terminated the transaction, check the correctness.
            if (trans.is_response_error()) {
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """
    writeMemAliasCode = ''
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'
    writeBody = cxx_writer.Code(swapDEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    datumParam = cxx_writer.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.Method('write_dword', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.Code(swapEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    datumParam = cxx_writer.Parameter('datum', archWordType)
    writeDecl = cxx_writer.Method('write_word', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.Parameter('datum', archHWordType)
    writeMemAliasCode = swapEndianessDefine
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#else\n'
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#endif\n'
    writeBody = cxx_writer.Code(swapEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    writeDecl = cxx_writer.Method('write_half', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.Parameter('datum', archByteType)
    writeMemAliasCode = swapEndianessDefine
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archByteType) + '*)&' + alias.alias + '_temp) = (' + str(archByteType) + ')datum;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 1) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 2) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 3) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#else\n'
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archByteType) + '*)&' + alias.alias + '_temp) = (' + str(archByteType) + ')datum;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 1) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 2) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + '*)&' + alias.alias + '_temp) + 3) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#endif\n'
    writeBody = cxx_writer.Code(writeMemAliasCode + checkWatchPointCode + writeCode)
    writeDecl = cxx_writer.Method('write_byte', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    readCode1 = """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        """
    readCode2 = """trans.set_data_ptr(reinterpret_cast<unsigned char*>(&datum));
        this->init_socket->transport_dbg(trans);
        """
    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\nreturn this->' + alias.alias + ';\n}\n'
    addressParam = cxx_writer.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\ntrans.set_streaming_width(' + str(self.wordSize*2) + ');\n' + str(archDWordType) + ' datum = 0;\n' + readCode2 + swapDEndianessCode + 'return datum;')
    readBody.addInclude('common/report.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.Method('read_dword_dbg', readBody, archDWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\ntrans.set_streaming_width(' + str(self.wordSize) + ');\n' + str(archWordType) + ' datum = 0;\n' + readCode2 + swapEndianessCode + 'return datum;')
    readDecl = cxx_writer.Method('read_word_dbg', readBody, archWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn (' + str(archHWordType) + ')' + alias.alias + '_temp;\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archHWordType) + ' *)&(' + alias.alias + '_temp)) + 1);\n}\n'
    readBody = cxx_writer.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\ntrans.set_streaming_width(' + str(self.wordSize/2) + ');\n' + str(archHWordType) + ' datum = 0;\n' + readCode2 + swapEndianessCode + 'return datum;')
    readDecl = cxx_writer.Method('read_half_dbg', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readMemAliasCode = ''
    for alias in self.memAlias:
        readMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn (' + str(archByteType) + ')' + alias.alias + '_temp;\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 1);\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 2);\n}\n'
        readMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n' + swapEndianessDefine + 'this->swap_endianess(' + alias.alias + '_temp);\n#endif\nreturn *(((' + str(archByteType) + ' *)&(' + alias.alias + '_temp)) + 3);\n}\n'
    readBody = cxx_writer.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(1);\ntrans.set_streaming_width(1);\n' + str(archByteType) + ' datum = 0;\n' + readCode2 + 'return datum;')
    readDecl = cxx_writer.Method('read_byte_dbg', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    writeCode1 = """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        """
    writeCode2 = """trans.set_data_ptr((unsigned char*)&datum);
        this->init_socket->transport_dbg(trans);
        """
    writeMemAliasCode = ''
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'
    writeBody = cxx_writer.Code(swapDEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\ntrans.set_streaming_width(' + str(self.wordSize*2) + ');\n' + writeCode2)
    datumParam = cxx_writer.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.Method('write_dword_dbg', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.Code(swapEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\ntrans.set_streaming_width(' + str(self.wordSize) + ');\n' + writeCode2)
    datumParam = cxx_writer.Parameter('datum', archWordType)
    writeDecl = cxx_writer.Method('write_word_dbg', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeMemAliasCode = swapEndianessDefine
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archHWordType) + ' *)' + alias.alias + '_temp) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#else\n'
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archHWordType) + ' *)' + alias.alias + '_temp) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + self.wordSize/2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archHWordType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archHWordType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#endif\n'
    datumParam = cxx_writer.Parameter('datum', archHWordType)
    writeBody = cxx_writer.Code(swapEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\ntrans.set_streaming_width(' + str(self.wordSize/2) + ');\n' + writeCode2)
    writeDecl = cxx_writer.Method('write_half_dbg', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeMemAliasCode = swapEndianessDefine
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archByteType) + ' *)&' + alias.alias + '_temp) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 2) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 3) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#else\n'
    for alias in self.memAlias:
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address)) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*((' + str(archByteType) + ' *)&' + alias.alias + '_temp) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 1) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 1) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 2) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 2) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
        writeMemAliasCode += 'if (address == ' + hex(long(alias.address) + 3) + ') {\n' + str(archWordType) + ' ' + alias.alias + '_temp = this->' + alias.alias + ';\n*(((' + str(archByteType) + ' *)&' + alias.alias + '_temp) + 3) = (' + str(archByteType) + ')datum;\nthis->' + alias.alias + '= ' + alias.alias + '_temp;\nreturn;\n}\n'
    writeMemAliasCode += '#endif\n'
    datumParam = cxx_writer.Parameter('datum', archByteType)
    writeBody = cxx_writer.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(1);\ntrans.set_streaming_width(1);\n' + writeCode2)
    writeDecl = cxx_writer.Method('write_byte_dbg', writeBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    lockDecl = cxx_writer.Method('lock', emptyBody, cxx_writer.voidType, 'pu')
    tlmPortElements.append(lockDecl)
    unlockDecl = cxx_writer.Method('unlock', emptyBody, cxx_writer.voidType, 'pu')
    tlmPortElements.append(unlockDecl)

    constructorParams.append(cxx_writer.Parameter('port_name', cxx_writer.sc_module_nameType))
    tlmPortInit.append('sc_module(port_name)')
    initSockAttr = cxx_writer.Attribute('init_socket', tlminitsocketType, 'pu')
    tlmPortElements.append(initSockAttr)
    constructorCode = 'this->debugger = NULL;\n'
    if model.endswith('LT'):
        if not model.startswith('acc'):
            quantumKeeperType = cxx_writer.Type('tlm_utils::tlm_quantumkeeper', 'tlm_utils/tlm_quantumkeeper.h')
            quantumKeeperAttribute = cxx_writer.Attribute('quant_keeper', quantumKeeperType.makeRef(), 'pri')
            tlmPortElements.append(quantumKeeperAttribute)
            tlmPortInit.append('quant_keeper(quant_keeper)')
            constructorParams.append(cxx_writer.Parameter('quant_keeper', quantumKeeperType.makeRef()))
        dmi_ptr_validAttribute = cxx_writer.Attribute('dmi_ptr_valid', cxx_writer.boolType, 'pri')
        tlmPortElements.append(dmi_ptr_validAttribute)
        dmi_dataAttribute = cxx_writer.Attribute('dmi_data', tlm_dmiType, 'pri')
        tlmPortElements.append(dmi_dataAttribute)
        constructorCode += 'this->dmi_ptr_valid = false;\n'
    else:
        peqType = cxx_writer.TemplateType('tlm_utils::peq_with_cb_and_phase', [TLMMemoryType], 'tlm_utils/peq_with_cb_and_phase.h')
        tlmPortElements.append(cxx_writer.Attribute('m_peq', peqType, 'pri'))
        tlmPortInit.append('m_peq(this, &TLMMemory::peq_cb)')
        tlmPortInit.append('request_in_progress(NULL)')
        constructorCode += """// Register callbacks for incoming interface method calls.
            this->init_socket.register_nb_transport_bw(this, &TLMMemory::nb_transport_bw);
            """

    tlmPortElements += aliasAttrs

    extPortDecl = cxx_writer.ClassDeclaration('TLMMemory', tlmPortElements, [memIfType, cxx_writer.sc_moduleType], namespaces = [namespace])
    extPortDecl.addDocString(brief = 'Port Class', detail = 'Defines the TLM ports used by the core for communicating with other modules.')
    constructorBody = cxx_writer.Code(constructorCode + 'end_module();')
    publicExtPortConstr = cxx_writer.Constructor(constructorBody, 'pu', constructorParams + aliasParams, tlmPortInit + aliasInit)
    extPortDecl.addConstructor(publicExtPortConstr)

    return extPortDecl

def getGetIRQPorts(self, namespace):
    """Returns the classes implementing the interrupt ports; there can
    be two different kind of ports: systemc based or TLM based"""
    TLMWidth = []
    SyscWidth = []
    for i in self.irqs:
        if i.operation:
            if i.tlm:
                if not i.portWidth in TLMWidth:
                    TLMWidth.append(i.portWidth)
            else:
                if not i.portWidth in SyscWidth:
                    SyscWidth.append(i.portWidth)

    # Lets now create the potyrt classes:
    classes = []
    for width in TLMWidth:
        # TLM ports: I declare a normal TLM slave
        tlmsocketType = cxx_writer.TemplateType('tlm_utils::multi_passthrough_target_socket', ['TLMIntrPort_' + str(width), str(width), 'tlm::tlm_base_protocol_types', 1, 'sc_core::SC_ZERO_OR_MORE_BOUND'], 'tlm_utils/multi_passthrough_target_socket.h')
        payloadType = cxx_writer.Type('tlm::tlm_generic_payload', 'tlm.h')
        tlmPortElements = []

        blockTransportCode = """unsigned char* ptr = trans.get_data_ptr();
            sc_dt::uint64 adr = trans.get_address();
            if (*ptr == 0) {
                // Lower the interrupt.
                this->irq_signal = -1;
            } else {
                // Raise the interrupt.
                this->irq_signal = adr;
            }
            trans.set_response_status(tlm::TLM_OK_RESPONSE);
        """
        blockTransportBody = cxx_writer.Code(blockTransportCode)
        tagParam = cxx_writer.Parameter('tag', cxx_writer.intType)
        payloadParam = cxx_writer.Parameter('trans', payloadType.makeRef())
        delayParam = cxx_writer.Parameter('delay', cxx_writer.sc_timeType.makeRef())
        blockTransportDecl = cxx_writer.Method('b_transport', blockTransportBody, cxx_writer.voidType, 'pu', [tagParam, payloadParam, delayParam])
        tlmPortElements.append(blockTransportDecl)

        debugTransportBody = cxx_writer.Code(blockTransportCode + 'return trans.get_data_length();')
        debugTransportDecl = cxx_writer.Method('transport_dbg', debugTransportBody, cxx_writer.uintType, 'pu', [tagParam, payloadParam])
        tlmPortElements.append(debugTransportDecl)

        nblockTransportCode = """THROW_EXCEPTION("Method not yet implemented.");
        return tlm::TLM_COMPLETED;
        """
        nblockTransportBody = cxx_writer.Code(nblockTransportCode)
        nblockTransportBody.addInclude('common/report.hpp')
        sync_enumType = cxx_writer.Type('tlm::tlm_sync_enum', 'tlm.h')
        phaseParam = cxx_writer.Parameter('phase', cxx_writer.Type('tlm::tlm_phase').makeRef())
        nblockTransportDecl = cxx_writer.Method('nb_transport_fw', nblockTransportBody, sync_enumType, 'pu', [tagParam, payloadParam, phaseParam, delayParam])
        tlmPortElements.append(nblockTransportDecl)

        socketAttr = cxx_writer.Attribute('target_socket', tlmsocketType, 'pu')
        tlmPortElements.append(socketAttr)
        from isa import resolveBitType
        widthType = resolveBitType('BIT<' + str(width) + '>')
        irqSignalAttr = cxx_writer.Attribute('irq_signal', widthType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.Parameter('port_name', cxx_writer.sc_module_nameType))
        constructorParams.append(cxx_writer.Parameter('irq_signal', widthType.makeRef()))
        tlmPortInit.append('sc_module(port_name)')
        tlmPortInit.append('irq_signal(irq_signal)')
        tlmPortInit.append('target_socket(port_name)')
        constructorCode += 'this->target_socket.register_b_transport(this, &TLMIntrPort_' + str(width) + '::b_transport);\n'
        constructorCode += 'this->target_socket.register_transport_dbg(this, &TLMIntrPort_' + str(width) + '::transport_dbg);\n'
        constructorCode += 'this->target_socket.register_nb_transport_fw(this, &TLMIntrPort_' + str(width) + '::nb_transport_fw);\n'
        irqPortDecl = cxx_writer.ClassDeclaration('TLMIntrPort_' + str(width), tlmPortElements, [cxx_writer.sc_moduleType], namespaces = [namespace])
        constructorBody = cxx_writer.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    for width in SyscWidth:
        # SystemC ports: I simply have a method listening for a signal; note that in order to lower the interrupt,
        # the signal has to be equal to 0
        widthSignalType = cxx_writer.TemplateType('sc_signal', [widthType], 'systemc.h')
        systemcPortElements = []
        sensitiveMethodCode = 'this->irq_signal = this->irq_received_signal.read();'
        sensitiveMethodBody = cxx_writer.Code(sensitiveMethodCode)
        sensitiveMethodDecl = cxx_writer.Method('irq_received', sensitiveMethodBody, cxx_writer.voidType, 'pu')
        systemcPortElements.append(sensitiveMethodDecl)
        signalAttr = cxx_writer.Attribute('irq_received_signal', widthSignalType, 'pu')
        systemcPortElements.append(signalAttr)
        irqSignalAttr = cxx_writer.Attribute('irq_signal', widthType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.Parameter('port_name', cxx_writer.sc_module_nameType))
        constructorParams.append(cxx_writer.Parameter('irq_signal', widthType.makeRef()))
        tlmPortInit.append('sc_module(port_name)')
        tlmPortInit.append('irq_signal(irq_signal)')
        constructorCode += 'SC_METHOD();\nsensitive << this->irq_received_signal;\n'
        irqPortDecl = cxx_writer.ClassDeclaration('SCIntrPort_' + str(width), systemcPortElements, [cxx_writer.sc_moduleType], namespaces = [namespace])
        irqPortDecl.addDocString(brief = 'Interrupt Port Class', detail = 'Defines both SystemC and TLM ports for convenience.')
        constructorBody = cxx_writer.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    return classes

def getGetPINPorts(self, namespace):
    """Returns the code implementing pins for communication with external world.
    there are both incoming and outgoing external ports. For the outgoing
    I simply have to declare the port class (like memory ports), for the
    incoming I also have to specify the operation which has to be performed
    when the port is triggered (they are like interrupt ports)"""
    if len(self.pins) == 0:
        return None

    alreadyDecl = []
    inboundSysCPorts = []
    outboundSysCPorts = []
    inboundTLMPorts = []
    outboundTLMPorts = []
    for port in self.pins:
        if port.inbound:
            # I add all the inbound ports since there is an action specified for each
            # of them. In order to correctly execute the specified action the
            # port needs to have references to all the architectural elements
            if port.systemc:
                inboundSysCPorts.append(port)
            else:
                inboundTLMPorts.append(port)
        else:
            # I have to declare a new port only if there is not yet another
            # port with same width and it is systemc or tlm.
            if not (str(port.portWidth) + '_' + str(port.systemc)) in alreadyDecl:
                if port.systemc:
                    outboundSysCPorts.append(port)
                else:
                    outboundTLMPorts.append(port)
                alreadyDecl.append(str(port.portWidth) + '_' + str(self.systemc))

    pinClasses = []
    # Now I have to actually declare the ports; I declare only
    # blocking interfaces
    # outgoing
    for port in outboundTLMPorts:
        pinPortElements = []

        tlm_dmiType = cxx_writer.Type('tlm::tlm_dmi', 'tlm.h')
        PinPortType = cxx_writer.Type('TLMOutPin_' + str(port.portWidth))
        tlminitsocketType = cxx_writer.TemplateType('tlm_utils::multi_passthrough_initiator_socket', [PinPortType, port.portWidth, 'tlm::tlm_base_protocol_types', 1, 'sc_core::SC_ZERO_OR_MORE_BOUND'], 'tlm_utils/multi_passthrough_initiator_socket.h')
        payloadType = cxx_writer.Type('tlm::tlm_generic_payload', 'tlm.h')
        pinPortInit = []
        constructorParams = []

        sendPINBody = cxx_writer.Code("""tlm::tlm_generic_payload trans;
        sc_time delay;
        trans.set_address(address);
        trans.set_write();
        trans.set_data_ptr((unsigned char*)&datum);
        trans.set_data_length(sizeof(datum));
        trans.set_streaming_width(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
        this->init_socket->b_transport(trans, delay);

        if (trans.is_response_error()) {
            std::string error_str("Error from b_transport, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", error_str.c_str());
        }
        """)
        sendPINBody.addInclude('common/report.hpp')
        sendPINBody.addInclude('tlm.h')
        from isa import resolveBitType
        PINWidthType = resolveBitType('BIT<' + str(port.portWidth) + '>')
        addressParam = cxx_writer.Parameter('address', PINWidthType.makeRef().makeConst())
        datumParam = cxx_writer.Parameter('datum', PINWidthType)
        sendPINDecl = cxx_writer.Method('send_pin_req', sendPINBody, cxx_writer.voidType, 'pu', [addressParam, datumParam], noException = True)
        pinPortElements.append(sendPINDecl)

        constructorParams.append(cxx_writer.Parameter('pin_name', cxx_writer.sc_module_nameType))
        pinPortInit.append('sc_module(pin_name)')
        initSockAttr = cxx_writer.Attribute('init_socket', tlminitsocketType, 'pu')
        pinPortInit.append('init_socket(\"init_socket\")')
        pinPortElements.append(initSockAttr)

        pinPortDecl = cxx_writer.ClassDeclaration('TLMOutPin_' + str(port.portWidth), pinPortElements, [cxx_writer.sc_moduleType], namespaces = [namespace])
        pinPortDecl.addDocString(brief = 'Pin Class', detail = 'Defines the pins used by the core for communicating with other modules. Outgoing ports call a given interface of another module, while incoming ports need to define the interface to be used by other modules.')
        constructorBody = cxx_writer.Code('end_module();')
        publicPINPortConstr = cxx_writer.Constructor(constructorBody, 'pu', constructorParams, pinPortInit)
        pinPortDecl.addConstructor(publicPINPortConstr)
        pinClasses.append(pinPortDecl)

    for port in outboundSysCPorts:
        raise Exception('Outbound SystemC ports not yet supported.')

    # incoming
    for port in inboundTLMPorts:
        raise Exception('Inbound TLM ports not yet supported.')

    for port in inboundSysCPorts:
        raise Exception('Inbound SystemC ports not yet supported.')

    return pinClasses

def getIRQTests(self, trace, combinedTrace, namespace):
    """Returns the code implementing the tests for the interrupts"""
    from processor import extractRegInterval
    testFuns = []
    global testNames
    from procWriter import testNames

    from procWriter import resourceType

    archElemsDeclStr = ''
    destrDecls = ''
    for reg in self.regs:
        archElemsDeclStr += str(resourceType[reg.name]) + ' ' + reg.name + ';\n'
    for regB in self.regBanks:
        if (regB.constValue and len(regB.constValue) < regB.numRegs)  or (regB.delay and len(regB.delay) < regB.numRegs):
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + '(' + str(regB.numRegs) + ');\n'
            for i in range(0, regB.numRegs):
                if regB.constValue.has_key(i) or regB.delay.has_key(i):
                    archElemsDeclStr += regB.name + '.set_new_register(' + str(i) + ', new ' + str(resourceType[regB.name + '[' + str(i) + ']']) + '());\n'
                else:
                    archElemsDeclStr += regB.name + '.set_new_register(' + str(i) + ', new ' + str(resourceType[regB.name + '_baseType']) + '());\n'
        else:
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + ' = new ' + str(resourceType[regB.name].makeNormal()) + '[' + str(regB.numRegs) + '];\n'
            destrDecls += 'delete [] ' + regB.name + ';\n'
    for alias in self.aliasRegs:
        archElemsDeclStr += str(resourceType[alias.name]) + ' ' + alias.name + ';\n'
    for aliasB in self.aliasRegBanks:
        archElemsDeclStr += str(resourceType[aliasB.name].makePointer()) + ' ' + aliasB.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        destrDecls += 'delete [] ' + aliasB.name + ';\n'
    memAliasInit = ''
    for alias in self.memAlias:
        memAliasInit += ', ' + alias.alias

    if (trace or (self.memory and self.memory[2])) and not self.systemc:
        archElemsDeclStr += 'unsigned total_cycles;\n'
    if self.memory:
        memDebugInit = ''
        if self.memory[2]:
            memDebugInit += ', total_cycles'
        if self.memory[3]:
            memDebugInit += ', ' + self.memory[3]
        archElemsDeclStr += 'LocalMemory ' + self.memory[0] + '(' + str(self.memory[1]) + memDebugInit + memAliasInit + ');\n'
    # Note how I declare local memories even for TLM ports. I use 1MB as default dimension
    for tlmPorts in self.tlmPorts.keys():
        archElemsDeclStr += 'LocalMemory ' + tlmPorts + '(' + str(1024*1024) + memAliasInit + ');\n'
    # Now I declare the PIN stubs for the outgoing PIN ports
    # and alts themselves
    for pinPort in self.pins:
        if not pinPort.inbound:
            if pinPort.systemc:
                pinPortTypeName = 'SC'
            else:
                pinPortTypeName = 'TLM'
            if pinPort.inbound:
                pinPortTypeName += 'InPin_'
            else:
                pinPortTypeName += 'OutPin_'
            pinPortTypeName += str(pinPort.portWidth)
            archElemsDeclStr += pinPortTypeName + ' ' + pinPort.name + '_pin(\"' + pinPort.name + '_pin\");\n'
            archElemsDeclStr += 'PINTarget<' + str(pinPort.portWidth) + '> ' + pinPort.name + '_target_pin(\"' + pinPort.name + '_target_pin\");\n'
            archElemsDeclStr += pinPort.name + '_pin.init_socket.bind(' + pinPort.name + '_target_pin.target_socket);\n'

    # Now we perform the alias initialization; note that they need to be initialized according to the initialization graph
    # (there might be dependences among the aliases)
    aliasInit = ''
    import networkx as NX
    from procWriter import aliasGraph
    orderedNodes = NX.topological_sort(aliasGraph)
    for alias in orderedNodes:
        if alias == 'stop':
            continue
        if isinstance(alias.initAlias, type('')):
            index = extractRegInterval(alias.initAlias)
            if index:
                curIndex = index[0]
                try:
                    for i in range(0, alias.numRegs):
                        aliasInit += alias.name + '[' + str(i) + '].update_alias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + ']);\n'
                        curIndex += 1
                except AttributeError:
                    aliasInit += alias.name + '.update_alias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + '], ' + str(alias.offset) + ');\n'
            else:
                aliasInit += alias.name + '.update_alias(' + alias.initAlias + ', ' + str(alias.offset) + ');\n'
        else:
            curIndex = 0
            for curAlias in alias.initAlias:
                index = extractRegInterval(curAlias)
                if index:
                    for curRange in range(index[0], index[1] + 1):
                        aliasInit += alias.name + '[' + str(curIndex) + '].update_alias(' + curAlias[:curAlias.find('[')] + '[' + str(curRange) + ']);\n'
                        curIndex += 1
                else:
                    aliasInit += alias.name + '[' + str(curIndex) + '].update_alias(' + curAlias + ');\n'
                    curIndex += 1

    for irq in self.irqs:
        from isa import resolveBitType
        irqType = resolveBitType('BIT<' + str(irq.portWidth) + '>')
        archElemsDeclStr += '\n// Fake interrupt line ' + str(irqType) + ' ' + irq.name + ';\n'
        testNum = 0
        for test in irq.tests:
            testName = 'irq_test_' + irq.name + '_' + str(testNum)
            code = archElemsDeclStr

            # Note that each test is composed of two parts: the first one
            # containing the status of the processor before the interrupt and
            # then the status of the processor after
            for resource, value in test[0].items():
                # I set the initial value of the global resources
                brackIndex = resource.find('[')
                memories = self.tlmPorts.keys()
                if self.memory:
                    memories.append(self.memory[0])
                if brackIndex > 0 and resource[:brackIndex] in memories:
                    try:
                        code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ', ' + hex(value) + ');\n'
                    except ValueError:
                        code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ', ' + hex(value) + ');\n'
                elif resource == irq.name:
                    code += resource + ' = ' + hex(value) + ';\n'
                else:
                    code += resource + '.immediate_write(' + hex(value) + ');\n'

            # Now I declare the actual interrupt code
            code += 'if ('
            if (irq.condition):
                code += '('
            code += irq.name + ' != -1'
            if (irq.condition):
                code += ') && (' + irq.condition + ')'
            code += ') {\n'
            # Now here we insert the actual interrupt behavior by simply creating and calling the
            # interrupt instruction
            from procWriter import baseInstrInitElement
            code += + irq.name + 'IntrInstruction test_instruction(' + baseInstrInitElement + ', ' + irq.name + ');\n'
            code += """try {
                test_instruction.behavior();
            }
            catch(annul_exception& etc) {
            }"""
            code += '\n}\n'

            # finally I check the correctness of the executed operation
            for resource, value in test[1].items():
                # I check the value of the listed resources to make sure that the
                # computation executed correctly
                code += 'BOOST_CHECK_EQUAL('
                brackIndex = resource.find('[')
                memories = self.tlmPorts.keys()
                if self.memory:
                    memories.append(self.memory[0])
                if brackIndex > 0 and resource[:brackIndex] in memories:
                    try:
                        code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                    except ValueError:
                        code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
                elif brackIndex > 0 and resource[:brackIndex] in outPinPorts:
                    try:
                        code += resource[:brackIndex] + '_target.read_pin(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                    except ValueError:
                        code += resource[:brackIndex] + '_target.read_pin(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
                else:
                    code += resource + '.read_new_value()'
                code += ', (' + str(self.bitSizes[1]) + ')' + hex(value) + ');\n\n'
            code += destrDecls
            curTest = cxx_writer.Code(code)
            curTest.addInclude('#include \"instructions.hpp\"')
            wariningDisableCode = '#ifdef _WIN32\n#pragma warning(disable : 4101)\n#endif\n'
            includeUnprotectedCode = '#define private public\n#define protected public\n#include \"registers.hpp\"\n#include \"memory.hpp\"\n#undef private\n#undef protected\n'
            curTest.addInclude(['boost/test/test_tools.hpp', 'common/report.hpp', wariningDisableCode, includeUnprotectedCode, '#include \"alias.hpp\"'])
            curTestFunction = cxx_writer.Function(testName, curTest, cxx_writer.voidType)
            curTestFunction.addDocString(brief = 'IRQ Test Function', detail = 'Called by test/main.cpp::main() via the boost::test framework. Instantiates the required modules and tests correct IRQ handling.')
            testFuns.append(curTestFunction)
            testNames.append(testName)
            testNum += 1

    return testFuns
