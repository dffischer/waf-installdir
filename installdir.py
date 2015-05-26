#!/usr/bin/python

"""
Install directories with permissions.

This adds an install_dir function to the build, install and uninstall contexts,
similar to install_files, install_as and symlink_as. It allows to set directory
permissions and install empty directories. Note that placing a decoy file is
good practice nonetheless, as many package management systems like to strip out
empty directories.

It is only necessary and effective to load this tool in the build function.
"""

from waflib.Utils import O755, check_dir, to_list, subst_vars
from waflib.Build import InstallContext, UninstallContext, BuildContext, inst
from waflib.Logs import info
from os import chmod, stat
from os.path import join


def patch(cls):
    """Patch a decorated method into an existing class given as an argument."""
    def add(method):
        setattr(cls, method.__name__, method)
        return method
    return add


installContext = patch(InstallContext)

@installContext
def install_dir(self, dest, paths, env=None, chmod=O755, cwd=None, add=True, postpone=True, task=None):
    """
    Create a task to install direcories on the system::

            def build(bld):
                    bld.install_files('${DATADIR}', '${PACKAGE}')

    :param dest: absolute path of the destination directory
    :type dest: string
    :param paths: paths of directories to create
    :type paths: list of strings or space separated string
    :param env: configuration set for performing substitutions in dest
    :type env: Configuration set
    :param chmod: mode for directories to set
    :type chmod: int
    :param cwd: parent node for searching srcfile, when srcfile is not a :py:class:`waflib.Node.Node`
    :type cwd: :py:class:`waflib.Node.Node`
    :param add: add the task created to a build group - set ``False`` only if the installation task is created after the build has started
    :type add: bool
    :param postpone: execute the task immediately to perform the installation
    :type postpone: bool
    """
    assert(dest)
    tsk = inst(env=env or self.env)
    tsk.bld = self
    tsk.path = cwd or self.path
    tsk.chmod = chmod
    tsk.task = task
    tsk.dest = dest
    tsk.source = []
    tsk.paths = to_list(paths)
    tsk.exec_task = tsk.exec_install_dir
    if add: self.add_to_group(tsk)
    self.run_task_now(tsk, postpone)
    return tsk

@patch(inst)
def exec_install_dir(self):
    destpath = self.get_install_path()
    if not destpath:
        raise Errors.WafError('unknown installation path %r' % self.generator)
    for path in self.paths:
        self.generator.bld.do_install_dir(
                join(destpath, subst_vars(path, self.env)),
                chmod=self.chmod, tsk=self)

@installContext
def do_install_dir(self, tgt, **kw):
    """
    Create a directory tgt and all its parents. The actual creating or mode
    modification is not performed if the directory already exists with the
    given permissions

    This method is overridden in :py:meth:`waflib.Build.UninstallContext.do_install_dir` to remove the file.

    :param tgt: directory name, as absolute path
    :type tgt: string
    :param chmod: installation mode
    :type chmod: int
    """
    mode = kw.get('chmod', O755)

    # Do not install when already present with correct mode.
    try:
        if stat(tgt).st_mode & 0o777 == mode & 0o777:
            if not self.progress_bar:
                info('- install %s (directory)' % (tgt, ))
            return False
    except OSError:
        pass

    check_dir(tgt)
    chmod(tgt, mode)
    if not self.progress_bar:
        info('+ install %s (directory) %s' % (tgt, mode))

@patch(UninstallContext)
def do_install_dir(self, tgt, **kw):
    if not self.progress_bar:
        info('- remove %s' % tgt)
    self.rm_empty_dirs(join(tgt, '.empty'))

@patch(BuildContext)
def install_dir(self, *k, **kw):
    pass
