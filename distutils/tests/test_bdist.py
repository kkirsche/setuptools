"""Tests for distutils.command.bdist."""
import os
import warnings

from distutils.command.bdist import bdist
from distutils.tests import support


class TestBuild(support.TempdirManager):
    def test_formats(self):
        # let's create a command and make sure
        # we can set the format
        dist = self.create_dist()[1]
        cmd = bdist(dist)
        cmd.formats = ['msi']
        cmd.ensure_finalized()
        assert cmd.formats == ['msi']

        # what formats does bdist offer?
        formats = [
            'bztar',
            'gztar',
            'msi',
            'rpm',
            'tar',
            'xztar',
            'zip',
            'ztar',
        ]
        found = sorted(cmd.format_commands)
        assert found == formats

    def test_skip_build(self):
        # bug #10946: bdist --skip-build should trickle down to subcommands
        dist = self.create_dist()[1]
        cmd = bdist(dist)
        cmd.skip_build = 1
        cmd.ensure_finalized()
        dist.command_obj['bdist'] = cmd

        names = [
            'bdist_dumb',
        ]  # bdist_rpm does not support --skip-build
        if os.name == 'nt':
            names.append('bdist_msi')

        for name in names:
            subcmd = cmd.get_finalized_command(name)
            if getattr(subcmd, '_unsupported', False):
                # command is not supported on this build
                continue
            assert subcmd.skip_build, '%s should take --skip-build from bdist' % name
