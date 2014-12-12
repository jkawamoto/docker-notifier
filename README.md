# Docker Notifier
Notify docker's events, especially exit events, via [Pushover](https://pushover.net/).

## Install
```bash
docker pull jkawamoto/docker-notifier
```

## Usage

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock \
       jkawamoto/docker-notifier <USER> <TOKE>
```

where `<USER>` and `<TOKEN>` are user key and application key of PushOver.

### Filtering
Use `--filter` option to choose containers to notify. The option takes a regular expression.

## License
This software is released under the MIT License, see LICENSE.
