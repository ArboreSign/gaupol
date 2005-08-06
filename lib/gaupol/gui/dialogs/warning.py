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


"""Warning message dialogs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk


FLAGS   = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT
TYPE    = gtk.MESSAGE_WARNING
BUTTONS = gtk.BUTTONS_NONE


class OpenBigFileWarningDialog(gtk.MessageDialog):

    """Warning dialog displayed when trying to open a file over 1 MB."""
    
    def __init__(self, parent, basename, size):
        """
        Initialize an OpenBigFileWarningDialog object.
        
        basename: basename of the file being opened
        size: file's size in megabytes.
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Open abnormally large file "%s"?') % basename
        )
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_OPEN  , gtk.RESPONSE_YES)
        
        self.set_default_response(gtk.RESPONSE_NO)
        
        self.format_secondary_text( \
            _('Size of the file is %.1f MB, which is abnormally large for a text-based subtitle file. Please, check that you are not trying to open a binary file.') \
            % size \
        )


class CloseMainDocumentWarningDialog(gtk.MessageDialog):

    """
    Warning dialog displayed when trying to close a main document.
    
    Dialog will be displayed if subtitle document has unsaved changes.
    """
    
    def __init__(self, parent, basename):
        """
        Initialize a CloseMainDocumentWarningDialog object.
        
        basename: basename of the document being closed
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Save changes to subtitle document "%s" before closing?') \
            % basename
        )
        
        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL          , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE            , gtk.RESPONSE_YES   )
        
        self.set_default_response(gtk.RESPONSE_YES)
        
        self.format_secondary_text( \
            _('If you don\'t save, changes will be permanently lost.') \
        )


class CloseTranslationDocumentWarningDialog(gtk.MessageDialog):

    """
    Warning dialog displayed when trying to close a translation document. 
    
    Dialog will be displayed if translation document has unsaved changes.
    """
    
    def __init__(self, parent, basename):
        """
        Initialize a CloseTranslationDocumentWarningDialog object.
        
        basename: basename of the document being closed
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Save changes to translation document "%s" before closing?') \
            % basename
        )
        
        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL          , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE            , gtk.RESPONSE_YES   )
        
        self.set_default_response(gtk.RESPONSE_YES)
        
        self.format_secondary_text( \
            _('If you don\'t save, changes will be permanently lost.') \
        )


class ImportTranslationWarningDialog(gtk.MessageDialog):

    """
    Warning dialog displayed when trying to import a translation file.
    
    Dialog will be displayed if currently open translation document has
    unsaved changes.
    """
    
    def __init__(self, parent, basename):
        """
        Initialize an ImportTranslationWarningDialog object.
        
        basename: basename of the file being opened
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Save changes to translation document "%s" before importing a new one?') \
            % basename
        )
        
        self.add_button(_('Import _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL           , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE             , gtk.RESPONSE_YES   )
        
        self.set_default_response(gtk.RESPONSE_YES)
        
        self.format_secondary_text( \
            _('If you don\'t save, changes will be permanently lost.') \
        )
