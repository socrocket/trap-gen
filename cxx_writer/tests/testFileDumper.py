################################################################################
#
#  _/_/_/_/_/  _/_/_/           _/        _/_/_/
#     _/      _/    _/        _/_/       _/    _/
#    _/      _/    _/       _/  _/      _/    _/
#   _/      _/_/_/        _/_/_/_/     _/_/_/
#  _/      _/    _/     _/      _/    _/
# _/      _/      _/  _/        _/   _/
#
# @file     testFileDumper.py
# @brief    This file is part of the TRAP CXX code generator testsuite.
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

try:
    import cxx_writer
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join('..')))
    try:
        import cxx_writer
    except ImportError:
        sys.path.append(os.path.abspath(os.path.join('..', '..')))
        try:
            import cxx_writer
        except ImportError:
            print ('Please specify location of core TRAP files in testFileDumper.py.')

import unittest
import os

class TestFileDumper(unittest.TestCase):

    def testDumpVariablesHeader(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Variable('pippo', tempType)
        dumper = cxx_writer.FileDumper('prova.cpp', True, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 2 + 18)
        self.assertEqual(lines[13], '#include <map>\n')
        self.assertEqual(lines[14], '#include <string>\n')

    def testDumpVariablesImpl(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Variable('pippo', tempType)
        dumper = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + 14)
        self.assertEqual(lines[11], '#include <map>\n')
        self.assertEqual(lines[12], '#include <string>\n')
        self.assertEqual(lines[15], 'std::map<int, std::string> pippo;\n')

    def testDumpFunctionsHeader(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Function('pippo', cxx_writer.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = cxx_writer.FileDumper('prova.cpp', True, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + 18)
        self.assertEqual(lines[13], '#include <map>\n')
        self.assertEqual(lines[14], '#include <string>\n')
        self.assertEqual(lines[17], 'std::map<int, std::string> pippo();\n')

    def testDumpFunctionsImpl(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Function('pippo', cxx_writer.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 7 + 14)
        self.assertEqual(lines[11], '#include <map>\n')
        self.assertEqual(lines[12], '#include <string>\n')
        self.assertEqual(lines[15], 'std::map<int, std::string> pippo() {\n')
        self.assertEqual(lines[16], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[17], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[18], '    return myMap;\n')
        self.assertEqual(lines[19], '} // pippo()\n')

    def testTemplateFunctionsHeader(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Function('pippo', cxx_writer.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, False, ['T'])
        dumper = cxx_writer.FileDumper('prova.cpp', True, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 7 + 18)
        self.assertEqual(lines[13], '#include <map>\n')
        self.assertEqual(lines[14], '#include <string>\n')
        self.assertEqual(lines[17], 'template <typename T> std::map<int, std::string> pippo() {\n')
        self.assertEqual(lines[18], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[19], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[20], '    return myMap;\n')
        self.assertEqual(lines[21], '} // pippo()\n')

    def testTemplateFunctionsImpl(self):
        tempType = cxx_writer.TemplateType('std::map', [cxx_writer.intType, cxx_writer.stringType], 'map')
        tempVar = cxx_writer.Function('pippo', cxx_writer.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, ['T'])
        dumper = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 2 + 14)
        self.assertEqual(lines[11], '#include <map>\n')
        self.assertEqual(lines[12], '#include <string>\n')

    def testDumpClassHeader(self):
        intDecl = cxx_writer.intType
        privateVar = cxx_writer.Attribute('pippo', intDecl, 'private')
        emptyBody = cxx_writer.Code('')
        publicConstr = cxx_writer.Constructor(emptyBody, 'public')
        classDecl = cxx_writer.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = cxx_writer.FileDumper('prova.cpp', True, indentSize = 4, lineWidth = 80)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + 18)
        self.assertEqual(lines[14], 'class MyClass {\n')
        self.assertEqual(lines[15], '    public:\n')
        self.assertEqual(lines[16], '    MyClass();\n')
        self.assertEqual(lines[17], '\n')
        self.assertEqual(lines[18], '    private:\n')
        self.assertEqual(lines[19], '    int pippo;\n')
        self.assertEqual(lines[20], '\n')
        self.assertEqual(lines[21], '}; // class MyClass\n')

    def testDumpClassImpl(self):
        intDecl = cxx_writer.intType
        privateVar = cxx_writer.Attribute('pippo', intDecl, 'private')
        emptyBody = cxx_writer.Code('')
        publicConstr = cxx_writer.Constructor(emptyBody, 'public')
        classDecl = cxx_writer.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + 14)
        self.assertEqual(lines[12], 'MyClass::MyClass() {\n')
        self.assertEqual(lines[13], '\n')
        self.assertEqual(lines[14], '} // MyClass()\n')

    def testDumpTemplateClassHeader(self):
        intDecl = cxx_writer.intType
        stringDecl = cxx_writer.stringType
        privateVar = cxx_writer.Attribute('pippo', intDecl, 'private')
        emptyBody = cxx_writer.Code('')
        publicConstr = cxx_writer.Constructor(emptyBody, 'public', [], ['std::string()'])
        classDecl = cxx_writer.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = cxx_writer.FileDumper('prova.cpp', True, indentSize = 4, lineWidth = 80)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 15 + 18)
        self.assertEqual(lines[16], 'template <typename T>\n')
        self.assertEqual(lines[17], 'class MyClass : public std::string {\n')
        self.assertEqual(lines[18], '    public:\n')
        self.assertEqual(lines[19], '    MyClass() :\n')
        self.assertEqual(lines[20], '        std::string() {\n')
        self.assertEqual(lines[21], '\n')
        self.assertEqual(lines[22], '    } // MyClass()\n')
        self.assertEqual(lines[23], '\n')
        self.assertEqual(lines[24], '\n')
        self.assertEqual(lines[25], '    private:\n')
        self.assertEqual(lines[26], '    int pippo;\n')
        self.assertEqual(lines[27], '\n')
        self.assertEqual(lines[28], '}; // class MyClass\n')

    def testDumpTemplateClassImpl(self):
        intDecl = cxx_writer.intType
        stringDecl = cxx_writer.stringType
        privateVar = cxx_writer.Attribute('pippo', intDecl, 'private')
        emptyBody = cxx_writer.Code('')
        publicConstr = cxx_writer.Constructor(emptyBody, 'public', [], ['std::string()'])
        classDecl = cxx_writer.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 1 + 14)

    def testEmptyFolder(self):
        folder = cxx_writer.Folder('temp/try')
        folder.create()
        self.assert_(os.path.exists('temp/try/wscript'))
        os.remove('temp/try/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testDumpAll(self):
        folder = cxx_writer.Folder('temp')
        intDecl = cxx_writer.intType
        privateVar = cxx_writer.Attribute('pippo', intDecl, 'private')
        emptyBody = cxx_writer.Code('')
        publicConstr = cxx_writer.Constructor(emptyBody, 'public')
        classDecl = cxx_writer.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        implFile = cxx_writer.FileDumper('prova.cpp', False, indentSize = 4, lineWidth = 80)
        implFile.addMember(classDecl)
        headFile = cxx_writer.FileDumper('prova.hpp', True, indentSize = 4, lineWidth = 80)
        headFile.addMember(classDecl)
        folder.addHeader(headFile)
        folder.addCode(implFile)
        folder.create()
        testImplFile = open('temp/prova.cpp', 'rt')
        lines = testImplFile.readlines()
        testImplFile.close()
        os.remove('temp/prova.cpp')
        self.assertEqual(len(lines), 3 + 14)
        self.assertEqual(lines[12], 'MyClass::MyClass() {\n')
        self.assertEqual(lines[13], '\n')
        self.assertEqual(lines[14], '} // MyClass()\n')
        testHeadFile = open('temp/prova.hpp', 'rt')
        lines = testHeadFile.readlines()
        testHeadFile.close()
        os.remove('temp/prova.hpp')
        self.assertEqual(len(lines), 8 + 18)
        self.assertEqual(lines[14], 'class MyClass {\n')
        self.assertEqual(lines[15], '    public:\n')
        self.assertEqual(lines[16], '    MyClass();\n')
        self.assertEqual(lines[17], '\n')
        self.assertEqual(lines[18], '    private:\n')
        self.assertEqual(lines[19], '    int pippo;\n')
        self.assertEqual(lines[20], '\n')
        self.assertEqual(lines[21], '}; // class MyClass\n')
        testWscriptFile = open('temp/wscript', 'rt')
        lines = testWscriptFile.readlines()
        testWscriptFile.close()
        os.remove('temp/wscript')
        self.assertEqual(len(lines), 16)
        self.assertEqual(lines[0], '#!/usr/bin/env python\n')
        self.assertEqual(lines[1], '# -*- coding: iso-8859-1 -*-\n')
        self.assertEqual(lines[2], '\n')
        self.assertEqual(lines[3], 'import os\n')
        self.assertEqual(lines[4], '\n')
        self.assertEqual(lines[5], '\n')
        self.assertEqual(lines[6], 'def build(bld):\n')
        self.assertEqual(lines[7], '    sources = \"\"\"\n')
        self.assertEqual(lines[8], '        prova.cpp\n')
        self.assertEqual(lines[9], '    \"\"\"\n')
        self.assertEqual(lines[10], '    uselib = \'BOOST SYSTEMC TLM TRAP\'\n')
        self.assertEqual(lines[11], '    objects = \'\'\n')
        self.assertEqual(lines[12], '    includes = \'.\'\n')
        self.assertEqual(lines[13], '    target = \'temp\'\n')
        self.assertEqual(lines[15], '    bld.program(source = sources, target = target, use = uselib + \' \' + objects, includes = includes)\n')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs1(self):
        folder = cxx_writer.Folder('temp')
        nestFolder = cxx_writer.Folder('nested')
        folder.addSubFolder(nestFolder)
        folder.create()
        nestFolder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs2(self):
        folder = cxx_writer.Folder('temp')
        nestFolder = cxx_writer.Folder('nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirsCommonPath(self):
        folder = cxx_writer.Folder('temp')
        nestFolder = cxx_writer.Folder('temp/nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

################################################################################
