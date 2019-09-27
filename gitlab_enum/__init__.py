import argparse
import logging
from .gitlab_enum import GitLabEnum
from urllib.parse import urlparse


def main():
    args_parser = argparse.ArgumentParser(description='GitLab users enumeration',
                                          formatter_class=argparse.RawDescriptionHelpFormatter)

    args_parser.add_argument('-u', '--url', help='GitLab URL', metavar='http[s]://URL', required=True)
    args_parser.add_argument('-o', '--out', help='CSV output file',
                             default='gitlab_users_{netloc}.csv', metavar='gitlab_users_{netloc}.csv')
    args_parser.add_argument('-p', '--proxy', help='Proxy url',
                             default=None, metavar='socks5://localhost:9050')
    args_parser.add_argument('-v', '--version', help='API version',
                             default=3, metavar='3', type=int)
    args_parser.add_argument('-t', '--threads', help='Threads count',
                             default=5, metavar='5', type=int)
    args_parser.add_argument('-n', '--nf-max', help='Max 404 codes before stop',
                             default=30, metavar='30', type=int)
    args_parser.add_argument('-k', '--no-check-certificate', help='Ignore SSL mismatch',
                             action='store_true')
    args_parser.add_argument('-l', '--logging', help='Logging level (DEBUG/INFO/WARNING/ERROR)',
                             default='INFO', metavar='INFO')
    arguments = vars(args_parser.parse_args())

    if arguments['logging'] == 'debug':
        logging.basicConfig(level=logging.DEBUG)
    elif arguments['logging'] == 'warning':
        logging.basicConfig(level=logging.WARNING)
    elif arguments['logging'] == 'error':
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    try:
        gitlab_enumeration = GitLabEnum(
            url=arguments['url'],
            proxy_url=arguments['proxy'],
            api_version=arguments['version'],
            threads_count=arguments['threads'],
            max_nf_count=arguments['nf_max'],
            no_check_certificate=arguments['no_check_certificate']
        )
    except ValueError as e:
        logger.error('Wrong URL!')
        exit(1)

    outfile_name = arguments['out'].format(netloc=urlparse(arguments['url']).netloc)
    if len(gitlab_enumeration.users):
        logger.info('Writing data to file {file}'.format(
            file=outfile_name
        ))
        with open(outfile_name, 'a') as outfile:
            outfile.write('id,name,username,state,avatar_url,web_url,'
                          'created_at,bio,location,skype,linkedin,twitter,website_url,organisation\n')
        for user in gitlab_enumeration.users:
            with open(outfile_name, 'a') as outfile:
                outfile.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},\n'.format(
                    user.id,
                    user.name,
                    user.username,
                    user.state,
                    user.avatar_url,
                    user.web_url,
                    user.created_at,
                    user.bio,
                    user.location,
                    user.skype,
                    user.linkedin,
                    user.twitter,
                    user.website_url,
                    user.organization
                ))
    else:
        logger.error('Users not found')
