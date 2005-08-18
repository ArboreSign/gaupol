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


"""Changing application appearance."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.constants import FRAMERATE, MODE
from gaupol.gui.colcons import *
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class Viewer(Delegate):

    """Changing application appearance."""

    def on_edit_mode_toggled(self, some_action, new_action):
        """Change edit mode."""

        project = self.get_current_project()

        # Cut off the plural "s".
        new_edit_mode_name = new_action.get_name()[:-1]
        new_edit_mode = MODE.NAMES.index(new_edit_mode_name)

        # Return if only refreshing widget state.
        if new_edit_mode == project.edit_mode:
            return

        gui.set_cursor_busy(self.window)

        model = project.tree_view.get_model()
        has_focus = project.tree_view.get_property('has-focus')

        project.edit_mode = new_edit_mode
        self.config.set('editor', 'edit_mode', new_edit_mode_name)

        # Get focus.
        row, col = project.get_focus()[:2]

        # Get selection.
        selected_rows = project.get_selected_rows()

        # Remove tree view.
        scrolled_window = project.tree_view.get_parent()
        scrolled_window.remove(project.tree_view)
        
        project.build_tree_view()

        # Add tree view.
        scrolled_window.add(project.tree_view)
        scrolled_window.show_all()
        
        project.reload_all_data()
        tree_view = project.tree_view
        tree_view.columns_autosize()
        model = tree_view.get_model()

        # Restore focus.
        try:
            tree_view_column = tree_view.get_column(col)
            tree_view.set_cursor(row, tree_view_column)
        except TypeError:
            pass
        project.set_active_column()

        # Scroll to focus.
        try:
            tree_view_column = tree_view.get_column(col)
            tree_view.scroll_to_cell(row, tree_view_column, True, 0.5, 0)
        except TypeError:
            pass

        # Restore selection.
        selection = tree_view.get_selection()
        for row in selected_rows:
            selection.select_path(row)

        tree_view.set_property('has-focus', has_focus)

        gui.set_cursor_normal(self.window)

    def on_framerate_changed(self, *args):
        """
        Change framerate.
        
        This method is called from the framerate ComboBox.
        """
        project = self.get_current_project()

        # Get new framerate.
        framerate = self.framerate_combo_box.get_active()
        framerate_name = FRAMERATE.NAMES[framerate]

        # Return if only refreshing widget state.
        if framerate == project.data.framerate:
            return

        gui.set_cursor_busy(self.window)

        # Set new framerate and save setting.
        project.data.change_framerate(framerate)
        self.config.set('editor', 'framerate', framerate_name)

        # Set the correct framerate menu item active.
        path = '/ui/menubar/view/framerate/%s' % framerate_name
        self.uim.get_widget(path).set_active(True)
        
        if project.edit_mode != project.data.main_file.MODE:
            project.reload_data_in_columns([SHOW, HIDE, DURN])

        gui.set_cursor_normal(self.window)

    def on_framerate_toggled(self, some_action, new_action):
        """
        Change framerate.
        
        This method is called from the menu.
        """
        project = self.get_current_project()

        # Get new framerate.
        framerate_name = new_action.get_name()
        framerate = FRAMERATE.NAMES.index(framerate_name)

        # Return if only refreshing widget state.
        if framerate == project.data.framerate:
            return

        gui.set_cursor_busy(self.window)

        # Set new framerate and save setting.
        project.data.change_framerate(framerate)
        self.config.set('editor', 'framerate', framerate_name)

        # Set the correct framerate ComboBox entry active.
        self.framerate_combo_box.set_active(framerate)
        
        if project.edit_mode != project.data.main_file.MODE:
            project.reload_data_in_columns([SHOW, HIDE, DURN])

        gui.set_cursor_normal(self.window)

    def on_statusbar_toggled(self, *args):
        """Toggle the visibility of the statusbar."""

        statusbar_hbox = gui.get_parent_widget(self.text_statusbar, gtk.HBox)
        visible = statusbar_hbox.get_property('visible')

        statusbar_hbox.set_property('visible', not visible)
        self.config.setboolean('view', 'statusbar', not visible)

    def on_toolbar_toggled(self, *args):
        """Toggle the visibility of the toolbar."""
        
        toolbar = self.uim.get_widget('/ui/toolbar')
        visible = toolbar.get_property('visible')
        
        toolbar.set_property('visible', not visible)
        self.config.setboolean('view', 'toolbar', not visible)

    def on_tree_view_column_toggled(self, toggle_action):
        """Toggle the visibility of a TreeView column."""

        project = self.get_current_project()

        col_name = toggle_action.get_name()
        col = COLUMN.NAMES.index(col_name)

        tree_view_column = project.tree_view.get_column(col)
        visible = tree_view_column.get_visible()

        path = '/ui/menubar/view/columns/%s' % col_name
        action = self.uim.get_action(path)
        active = action.get_active()

        # Return if only refreshing widget state.
        if active is visible:
            return

        gui.set_cursor_busy(self.window)

        tree_view_column.set_visible(not visible)
        visible_columns = []
        
        for i in range(len(COLUMN.NAMES)):
            if project.tree_view.get_column(i).get_visible():
                visible_columns.append(COLUMN.NAMES[i])
        
        self.config.setlist('view', 'columns', visible_columns)

        self.set_sensitivities()

        gui.set_cursor_normal(self.window)

    def on_tree_view_headers_clicked(self, button, event):
        """
        Show a popup menu when list headers are right-clicked.
        
        Popup menu allows showing/hiding list columns.
        """
        if event.button == 3:
            menu = self.uim.get_widget('/ui/column_popup')
            menu.popup(None, None, None, event.button, event.time)
