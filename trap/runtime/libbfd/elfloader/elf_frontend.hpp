/***************************************************************************//**
*
*  _/_/_/_/_/  _/_/_/           _/        _/_/_/
*     _/      _/    _/        _/_/       _/    _/
*    _/      _/    _/       _/  _/      _/    _/
*   _/      _/_/_/        _/_/_/_/     _/_/_/
*  _/      _/    _/     _/      _/    _/
* _/      _/      _/  _/        _/   _/
*
* @file     elf_frontend.hpp
* @brief    This file is part of the TRAP runtime library.
* @details  Part of the code of this class is taken from the binutils sources.
* @author   Luca Fossati
* @author   Lillian Tadros (Technische Universitaet Dortmund)
* @date     2008-2013 Luca Fossati
*           2015-2016 Technische Universitaet Dortmund
* @copyright
*
* This file is part of TRAP.
*
* TRAP is free software; you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as
* published by the Free Software Foundation; either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with this program; if not, write to the
* Free Software Foundation, Inc.,
* 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
* or see <http://www.gnu.org/licenses/>.
*
* (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
*
*******************************************************************************/

#ifndef TRAP_BFD_FRONTEND_H
#define TRAP_BFD_FRONTEND_H

extern "C" {
#include <bfd.h>
}

#ifdef __GNUC__
#ifdef __GNUC_MINOR__
#if (__GNUC__ >= 4 && __GNUC_MINOR__ >= 3)
#include <tr1/unordered_map>
#define template_map std::tr1::unordered_map
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#ifdef _WIN32
#include <hash_map>
#define  template_map stdext::hash_map
#else
#include <map>
#define  template_map std::map
#endif
#endif

#include <map>
#include <string>
#include <list>
#include <vector>

namespace trap {

/**
 * @brief Section
 */
struct Section {
  struct bfd_section* descriptor;
  bfd_byte* data;
  bfd_vma start_addr;
  bfd_size_type data_size;
  std::string name;
  int type;
}; // struct Section

/// ****************************************************************************

/**
 * @brief ELFFrontend
 */
class ELFFrontend {
  /// @name Constructors and Destructors
  /// @{

  private:
  // Private constructor. We want people to be only able to use get_instance
  // to get an instance of the frontend.
  ELFFrontend(std::string binary_name);

  public:
  ~ELFFrontend();

  /// @} Constructors and Destructors
  /// --------------------------------------------------------------------------
  /// @name Interface Methods
  /// @{

  public:
  static ELFFrontend& get_instance(std::string filename);

  static void reset();

  /// Returns the name of the executable file.
  std::string get_exec_name() const;

  /// Given an address, it sets filename to the name of the source file which
  /// contains the code and line to the line in that file. Returns false if the
  /// address is not valid.
  bool get_src_file(unsigned address, std::string& filename, unsigned& line) const;

  /// Returns the start address of the loadable code.
  unsigned get_binary_start() const;

  /// Returns the end address of the loadable code.
  unsigned get_binary_end() const;

  /// Given an address, it returns the first symbol found there, "" if no symbol
  /// is found at the specified address. Note that if address is in the middle
  /// of a function, the symbol returned refers to the function itself.
  std::string symbol_at(unsigned address) const throw();

  /// Given an address, it returns the symbols found there,(more than one symbol
  /// can be mapped to an address). Note that if address is in the middle of a
  /// function, the symbol returned refers to the function itself.
  std::list<std::string> symbols_at(unsigned address) const throw();

  /// Given the name of a symbol it returns its value (which usually is its
  /// address). valid is set to false if no symbol with the specified name is
  /// found.
  unsigned get_sym_addr(const std::string& symbol, bool& valid) const throw();

  /// Specifies whether the address is the first one of a rountine.
  bool is_routine_entry(unsigned address) const;

  /// Specifies whether the address is the last one of a routine.
  bool is_routine_exit(unsigned address) const;

  /// @} Interface Methods
  /// --------------------------------------------------------------------------
  /// @name Internal Methods
  /// @{

  private:
  /// Accesses the BFD internal structures in order to get the symbols.
  void read_syms();

  /// Accesses the BFD internal structures in order to get correspondence among
  /// machine code and the source code.
  void read_src();

  /// In case it is not possible to open the BFD because it is not possible to
  /// determine its target, this function extracts the list of possible targets.
  std::string get_matching_formats (char** p) const;
  static std::map<std::string, ELFFrontend*> cur_instance;

  /// @} Internal Methods
  /// --------------------------------------------------------------------------
  /// @name Data
  /// @{

  private:
  /// Name of the executable file.
  std::string exec_name;

  /// File descriptor of the binary file.
  bfd* exec_image;

  /// Size of each assembly instruction in bytes.
  unsigned word_size;

  // End address and start address (not necessarily the entry point) of the
  // loadable part of the binary file.
  std::pair<unsigned, unsigned> code_size;

  /// List of the sections which contain executable code.
  std::vector<Section> sec_list;

  // List of all the symbols in the binary file.
  asymbol** sy;

  /// What is read from the file.
  template_map<unsigned, std::list<std::string> > addr_to_sym;
  template_map<unsigned, std::string> addr_to_func;
  std::map<std::string, unsigned> sym_to_addr;
  template_map<unsigned, std::pair<std::string, unsigned> > addr_to_src;

  /// @} Data
}; // class ELFFrontend

} // namespace trap

/// ****************************************************************************
#endif // TRAP_BFD_FRONTEND_H
