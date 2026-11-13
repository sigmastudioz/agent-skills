"""Environment for local media tools; never copy the caller's environment."""
import os
from pathlib import Path


def tool_environment(*executables):
    """Keep selected tool directories, OS defaults and fixed non-secret settings.

    Tools are selected by the caller's explicit config or executable discovery. No
    HOME, credential, proxy, Python injection or loader settings reach the child.
    Temporary-directory and locale overrides are deliberately not inherited.
    """
    directories = [str(Path(executable).absolute().parent) for executable in executables if executable]
    directories += [item for item in os.defpath.split(os.pathsep) if item and item != '.']
    env = {'PATH': os.pathsep.join(dict.fromkeys(directories)),
           'LANG': 'C', 'LC_ALL': 'C', 'PYTHONNOUSERSITE': '1'}
    if os.name == 'nt':
        # Windows children need the OS directory. Query the OS, not an env value.
        import ctypes
        buffer = ctypes.create_unicode_buffer(32768)
        length = ctypes.windll.kernel32.GetWindowsDirectoryW(buffer, len(buffer))
        if not 0 < length < len(buffer):
            raise OSError('Cannot determine the Windows system directory')
        env['SYSTEMROOT'] = buffer.value
    return env
