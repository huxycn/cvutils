from typing import Any, Callable, Dict, List, Optional, TextIO, Union

from .backends.file_client import FileClient


"""  pure paths

provide purely computational operations without I/O

"""
pure_paths = [
    'dirname',
    'basename',
    'stem',
    'suffix',
    'join',
    'with_name',
    'with_stem',
    'with_suffix',
    'with_tag_suffix'
]


def dirname(path):
    file_client = FileClient.infer_client(uri=path)
    return file_client.dirname(path)


def basename(path):
    file_client = FileClient.infer_client(uri=path)
    return file_client.basename(path)

def stem(path: str,
         file_client_args: Optional[Dict] = None,
         **kwargs) -> str:
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.stem(path)


def suffix(path: str,
         file_client_args: Optional[Dict] = None,
         **kwargs) -> str:
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.suffix(path)


def join(path, *paths, auto_mkdir=True) -> str:
    file_client = FileClient.infer_client(uri=path)
    return file_client.join(path, *paths, auto_mkdir=auto_mkdir)


def with_name(path: str, name: str) -> str:
    pass


def with_stem(path: str, stem: str) -> str:
    pass


def with_suffix(path: str, suffix: str) -> str:
    pass


def with_tag_suffix(path: str,
                    tag: str,
                    suffix: str,
                    file_client_args: Optional[Dict] = None,
                    **kwargs) -> str:
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.with_tag_suffix(path, tag, suffix)


""" concrete paths

provide simple I/O operations (read metadata or read dir)

"""
concrete_paths = [
    'exists',
    'is_dir',
    'is_file',
    'list_dir'
]


def exists(path: str,
           file_client_args: Optional[Dict] = None,
           **kwargs):
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.exists(path)


def is_dir(path: str,
           file_client_args: Optional[Dict] = None,
           **kwargs):
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.is_dir(path)


def is_file(path: str,
            file_client_args: Optional[Dict] = None,
           **kwargs):
    file_client = FileClient.infer_client(file_client_args, path)
    return file_client.is_file(path)


def list_dir(dir_path: str, 
             suffix: str = None,
             file_client_args: Optional[Dict] = None):
    file_client = FileClient.infer_client(file_client_args, dir_path)
    yield from file_client.list_dir(dir_path, suffix)


__all__ = pure_paths + concrete_paths
