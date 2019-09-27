from typing import Optional, List
from datetime import datetime
from urllib.parse import urlparse
from threading import Thread
from queue import Queue, Empty
import urllib3
import requests
import logging


class GitLabUser:
    id: int
    name: str
    username: str
    state: str
    avatar_url: str
    web_url: str
    created_at: datetime
    bio: Optional[str]
    location: Optional[str]
    skype: str
    linkedin: str
    twitter: str
    website_url: str
    organization: Optional[str]

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return '[id: {id}; username: {username}]'.format(
            id=self.id,
            username=self.username
        )


class GitLabEnum:
    def __init__(self, url, proxy_url=None, api_version=3, threads_count=5, max_nf_count=30, no_check_certificate=False):
        self._logger = logging.getLogger(__name__)
        self._url = url
        self._api_version = api_version
        self._threads_count = threads_count
        self._max_nf_count = max_nf_count
        self._no_check_certificate = no_check_certificate
        if self._no_check_certificate:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            self._check_url()
        except ValueError as e:
            self._logger.error(e)
        self._proxy_url = proxy_url
        self._nf_count = 0

        self.users: List[GitLabUser] = list()
        self._process()

    def _check_url(self):
        if not urlparse(self._url).scheme:
            raise ValueError('Scheme not found in url')
        if self._url.endswith('/'):
            self._url = self._url[:-1]

    def _check_user(self, id_queue):
        while True:
            try:
                user_id = id_queue.get(timeout=5)
            except Empty:
                self._logger.debug('Thread finished his work')
                return
            try:
                response = requests.get('{url}/api/v{api_version}/users/{user_id}'.format(
                    url=self._url,
                    api_version=self._api_version,
                    user_id=user_id
                ), proxies={
                    'http': self._proxy_url,
                    'https': self._proxy_url
                }, verify=not self._no_check_certificate)
            except urllib3.exceptions.SSLError:
                self._logger.error('SSL Error occurred, try to use --no-check-certificate option')
                return
            if response.status_code != 200:
                self._nf_count += 1
                continue

            self._nf_count = 0
            self.users.append(GitLabUser(response.json()))

    def _enum_users(self):
        threads = list()
        id_queue = Queue(maxsize=self._threads_count * 2)

        self._logger.info('Spawning {} threads...'.format(self._threads_count))
        for i in range(self._threads_count):
            threads.append(Thread(target=self._check_user, args=(id_queue,)))
            threads[-1].start()
        curr_user_id = 1
        while self._nf_count < self._max_nf_count:
            id_queue.put(curr_user_id)
            curr_user_id += 1
        self._logger.info('Finishing threads...')
        for thread in threads:
            thread.join()

    def _process(self):
        self._enum_users()
        self.users.sort(key=lambda x: x.id)
