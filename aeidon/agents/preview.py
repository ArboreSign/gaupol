# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Previewing subtitles with a video player."""

import aeidon
import os
import string
import subprocess


class PreviewAgent(aeidon.Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=W0201

    __metaclass__ = aeidon.Contractual

    def __init__(self, master):
        """Initialize a :class:`aeidon.PreviewAgent` object."""
        aeidon.Delegate.__init__(self, master)
        aeidon.util.connect(self, self, "notify::main_file")

    def _get_subtitle_path_require(self, doc, encoding=None):
        assert self.get_file(doc) is not None
        if encoding is not None:
            assert aeidon.encodings.is_valid_code(encoding)

    def _get_subtitle_path(self, doc, encoding=None):
        """Return path to a file to preview, either real or temporary.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        """
        if encoding is not None:
            if encoding != self.get_file(doc).encoding:
                return self.new_temp_file(doc, encoding)
        if doc == aeidon.documents.MAIN:
            if not self.main_changed:
                return self.main_file.path
        if doc == aeidon.documents.TRAN:
            if not self.tran_changed:
                return self.tran_file.path
        return self.new_temp_file(doc)

    def _on_notify_main_file(self, *args):
        """Try to find the video file path if unset."""
        if not self.video_path:
            self.find_video()

    @aeidon.deco.export
    def find_video(self, extensions=None):
        """Find and return the video file path based on main file's path.

        `extensions` should be a sequence of video filename extensions or
        ``None`` for defaults. The video file is searched for in the same
        directory as the subtitle file. The subtitle file's filename without
        extension is assumed to start with or match the video file's filename
        without extension.
        """
        if self.main_file is None: return None
        extensions = list(extensions or (
            ".3ivx", ".asf", ".avi", ".divx", ".flv", ".m2v", ".mkv", ".mov",
            ".mp4", ".mpeg", ".mpg", ".ogm", ".qt", ".rm", ".rmvb", ".swf",
            ".vob", ".wmv",
            # Keep extensions that are used by other file types than videos at
            # the end of the list, so that if there are multiple matches, these
            # ambiguous extensions would not be the ones chosen.
            ".ogg", ".dat"))

        subroot = os.path.splitext(self.main_file.path)[0]
        dirname = os.path.dirname(self.main_file.path)
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            extension = extension.lower()
            if (extension in extensions) and subroot.startswith(fileroot):
                self.video_path = filepath
                return self.video_path
        return None

    def preview_require(self, position, doc, command, offset, encoding=None):
        assert self.get_file(doc) is not None
        assert self.video_path is not None

    def preview_ensure(self, value, *args, **kwargs):
        assert os.path.isfile(value[2])

    @aeidon.deco.export
    def preview(self, position, doc, command, offset, encoding=None):
        """Start video player with `command` from `position`.

        `command` should have variables ``$SECONDS``, ``$SUBFILE`` and
        ``$VIDEOFILE``. `offset` should be the amount of seconds before
        `position` to start, which can be used to take into account that video
        player's can usually seek only to keyframes, which exist maybe ten
        seconds or so apart. `encoding` can be specified if different from
        `doc` file encoding.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        Raise :exc:`aeidon.ProcessError` if unable to start process.

        Return a three tuple of :class:`subprocess.POpen` instance, command
        with variables expanded and process standard output and error path.
        """
        sub_path = self._get_subtitle_path(doc, encoding)
        output_path = aeidon.temp.create(".output")
        output_fd = aeidon.temp.get_handle(output_path)
        seconds = self.calc.to_seconds(position)
        seconds = "%.3f" % max(0.0, seconds - float(offset))
        command = string.Template(command).safe_substitute(
            SECONDS=seconds,
            SUBFILE=aeidon.util.shell_quote(sub_path),
            VIDEOFILE=aeidon.util.shell_quote(self.video_path))

        process = aeidon.util.start_process(command,
                                            stderr=subprocess.STDOUT,
                                            stdout=output_fd)

        return process, command, output_path
