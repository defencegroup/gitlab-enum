# Installation
`pip3 install git+https://github.com/defencegroup/gitlab-enum.git`

# Usage
```
usage: gitlabenum [-h] -u http[s]://URL [-o gitlab_users_{netloc}.csv]
                  [-p socks5://localhost:9050] [-v 3] [-t 5] [-n 30] [-l INFO]

GitLab users enumeration

optional arguments:
  -h, --help            show this help message and exit
  -u http[s]://URL, --url http[s]://URL
                        GitLab URL
  -o gitlab_users_{netloc}.csv, --out gitlab_users_{netloc}.csv
                        CSV output file
  -p socks5://localhost:9050, --proxy socks5://localhost:9050
                        Proxy url
  -v 3, --version 3     API version
  -t 5, --threads 5     Threads count
  -n 30, --nf-max 30    Max 404 codes before stop
  -l INFO, --logging INFO
                        Logging level (DEBUG/INFO/WARNING/ERROR)
```