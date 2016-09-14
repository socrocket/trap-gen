################################################################################
#
#  _/_/_/_/_/  _/_/_/           _/        _/_/_/
#     _/      _/    _/        _/_/       _/    _/
#    _/      _/    _/       _/  _/      _/    _/
#   _/      _/_/_/        _/_/_/_/     _/_/_/
#  _/      _/    _/     _/      _/    _/
# _/      _/      _/  _/        _/   _/
#
# @file     __run_tests.py
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

import unittest
from tests import testWriter
from tests import testFileDumper
from tests import testSimpleDecls
from tests import testClassDecls

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(testWriter.TestWriter)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testFileDumper.TestFileDumper))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testSimpleDecls.TestSimpleDecls))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testClassDecls.TestClassDecls))
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(suite)

################################################################################
