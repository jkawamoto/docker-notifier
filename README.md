# Docker Notifier
Notify docker's create and die events.

## Install
```sh
$ docker pull jkawamoto/docker-notifier
```

## Usage
Docker Notifier has two ways to notify those events.

One of them is via [Pushover](https://pushover.net/).
In this case, Docker Notifier notify only die events
i.e. it notify when containers restart, stop, and abend.
The usage of this notifications is as follows.

```sh
$ docker run -v /var/run/docker.sock:/var/run/docker.sock \
    jkawamoto/docker-notifier pushover <USER> <TOKEN>
```

where `<USER>` and `<TOKEN>` are user key and application key of PushOver, respectively.

The other way is via stdout / file like object.
You can connect other program with this notifications by pipe, etc.
The usage if as follows.

```bash
$ docker run -v /var/run/docker.sock:/var/run/docker.sock \
jkawamoto/docker-notifier stream
```

### Filtering
Use `--filter` option to choose containers to notify.
The option takes a UNIX-like filtering pattern.

## License
This software is released under the MIT License, see LICENSE.
