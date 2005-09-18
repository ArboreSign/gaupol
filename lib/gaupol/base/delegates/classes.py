# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""All delegate classes."""


from gaupol.base.delegates.analyzer   import Analyzer
from gaupol.base.delegates.editor     import Editor
from gaupol.base.delegates.filereader import FileReader
from gaupol.base.delegates.filewriter import FileWriter
from gaupol.base.delegates.formatter  import Formatter
from gaupol.base.delegates.frconv     import FramerateConverter


def get_delegate_names():
    """Get a list of the names of the delegate classes."""
    
    return [
        'Analyzer',
        'Editor',
        'FileReader',
        'FileWriter',
        'Formatter',
        'FramerateConverter',
    ]