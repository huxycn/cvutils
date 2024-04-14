
# Copyright (c) OpenMMLab. All rights reserved.
import inspect
import os
import os.path as osp
import re
import tempfile
import warnings
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Iterator, Optional, Tuple, Union
from urllib.request import urlopen

import cvutils
from cvutils.utils.misc import has_method
from cvutils.utils.path import is_filepath


from .base import BaseStorageBackend


class HTTPBackend(BaseStorageBackend):
    """HTTP and HTTPS storage bachend."""

    def get(self, filepath):
        value_buf = urlopen(filepath).read()
        return value_buf

    def get_text(self, filepath, encoding='utf-8'):
        value_buf = urlopen(filepath).read()
        return value_buf.decode(encoding)

    @contextmanager
    def get_local_path(
            self, filepath: str) -> Generator[Union[str, Path], None, None]:
        """Download a file from ``filepath``.

        ``get_local_path`` is decorated by :meth:`contxtlib.contextmanager`. It
        can be called with ``with`` statement, and when exists from the
        ``with`` statement, the temporary path will be released.

        Args:
            filepath (str): Download a file from ``filepath``.

        Examples:
            >>> client = HTTPBackend()
            >>> # After existing from the ``with`` clause,
            >>> # the path will be removed
            >>> with client.get_local_path('http://path/of/your/file') as path:
            ...     # do something here
        """
        try:
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(self.get(filepath))
            f.close()
            yield f.name
        finally:
            os.remove(f.name)