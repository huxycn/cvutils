import os

from pathlib import Path
from typing import Union
from contextlib import contextmanager

from .base import BaseStorageBackend


class ObsBackend(BaseStorageBackend):
    """ Huawei Cloud OBS Storage Backend

    Args:
        ak (str): access_key_id
        sk (str): secret_access_key
        server (str): server

    Examples:
        >>> filepath = 'obs://path/of/file'
        >>> client = ObsBackend()
        >>> client.get(filepath)
    """
    def __init__(self, ak=None, sk=None, server=None):
        try:
            from obs import ObsClient
        except ImportError:
            raise ImportError('Please install esdk-obs-python to enable ObsBackend')

        if ak is None:
            ak = os.getenv('OBS_AK')
        if sk is None:
            sk = os.getenv('OBS_SK')
        if server is None:
            server = os.getenv('OBS_SERVER')
        self._client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)

    @staticmethod
    def split_names(obs_url):
        assert obs_url.startswith('obs://')

        splits = obs_url[6:].split('/')
        bucketname = splits[0]
        objectname = '/'.join(splits[1:])
        parent_path = '/'.join(splits[1:-1])
        current_name = splits[-1]

        return bucketname, objectname, parent_path, current_name

    @staticmethod
    def join_names(bucketname, objectname):
        return f'obs://{bucketname}/{objectname}'

    def _upload_stream(self, obs_url, content):
        bucketname, objectname, _, _ = self.split_names(obs_url)
        try:
            resp = self._client.putContent(bucketname, objectname, content=content)
            if resp.status < 300:
                pass
            else:
                raise Exception('resp.status >= 300')
        except Exception as e:
            raise e

    def _download_stream(self, obs_url):
        bucketname, objectname, _, _ = self.split_names(obs_url)
        try:
            resp = self._client.getObject(bucketname, objectname, loadStreamInMemory=True)
            if resp.status < 300:
                return resp.body.buffer
            else:
                raise Exception('resp.status >= 300')
        except Exception as e:
            raise e

    def get(self, filepath: str) -> memoryview:
        return self._download_stream(filepath)

    def get_text(self,
                 filepath: Union[str, Path],
                 encoding: str = 'utf-8') -> str:
        return str(self._download_stream(filepath), encoding=encoding)

    def put(self, obj, filepath):
        self._upload_stream(filepath, obj)

    def put_text(self, obj, filepath):
        self._upload_stream(filepath, obj)

    def remove(self, filepath):
        raise NotImplementedError
        # bucketname, objectname, _, _ = self.split_names(filepath)
        # try:
        #     resp = self.deleteObject(bucketname, objectname)

        #     if resp.status < 300:
        #         return True
        #         # print('requestId:', resp.requestId)
        #         # print('deleteMarker:', resp.body.deleteMarker)
        #         # print('versionId:', resp.body.versionId)
        #     else:
        #         # print('errorCode:', resp.errorCode)
        #         # print('errorMessage:', resp.errorMessage)
        #         return False
        # except Exception as e:
        #     # import traceback
        #     # print(traceback.format_exc())
        #     logger.debug(f'Exception({e}): {obs_url}')
        #     return False

    def exists(self, filepath):
        bucketname, objectname, _, _ = self.split_names(filepath)
        try:
            resp = self._client.getObjectMetadata(bucketname, objectname)

            if resp.status < 300:
                return True
                # print('requestId:', resp.requestId)
                # print('etag:', resp.body.etag)
                # print('lastModified:', resp.body.lastModified)
                # print('contentType:', resp.body.contentType)
                # print('contentLength:', resp.body.contentLength)
            else:
                # print('status:', resp.status)
                return False
        except Exception as e:
            # import traceback
            # print(traceback.format_exc())
            raise e

    def is_dir(self, path):
        return not self.exists(path)

    def is_file(self, path):
        return self.exists(path)

    def join(self, path, *paths, auto_mkdir=True):
        paths = list(paths)
        if self.is_dir(path):
            path = path[:-1] if path.endswith('/') else path
            paths.insert(0, path)
            return '/'.join(paths)

    @contextmanager
    def get_local_path(self, filepath):
        raise NotImplementedError

    def list_dir(self, dir_path, suffix=None):
        def _endswith_suffix(t, s=None):
            return s is None or t.endswith(s)

        # if dir_path not end with '/', e.g. obs://bigdata-tmp/test,
        # 'listObjects' function will deal with all dir_path like obs://bigdata-tmp/test*
        if not dir_path.endswith('/'):
            dir_path += '/'

        if (suffix is not None) and not isinstance(suffix, (str, tuple)):
            raise TypeError('`suffix` must be a string or tuple of strings')

        bucketname, objectname, _, _ = self.split_names(dir_path)
        mark = None
        if suffix is not None:
            suffix = (suffix, ) if isinstance(suffix, str) else suffix
        else:
            suffix = (None, )
        while True:
            bucket_data = self._client.listObjects(bucketname, prefix=objectname, marker=mark)
            for val in bucket_data["body"]["contents"]:
                for s in suffix:
                    if _endswith_suffix(val['key'], s):
                        yield self.join_names(bucketname, val['key'])
            if bucket_data.body.is_truncated is True:
                mark = bucket_data.body.next_marker
            else:
                break

    def with_tag_suffix(self, path, tag, suffix):
        bucketname, objectname, parent_path, current_name = self.split_names(path)
        objectname = Path(objectname)
        objectname = objectname.with_name(objectname.stem + tag).with_suffix(suffix)
        objectname = str(objectname)
        return self.join_names(bucketname, objectname)

    def dirname(self, path):
        bucketname, objectname, parent_path, current_name = self.split_names(path)
        return self.join_names(bucketname, parent_path)

    def basename(self, path):
        bucketname, objectname, parent_path, current_name = self.split_names(path)
        return current_name
