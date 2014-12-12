FROM ubuntu:latest
MAINTAINER Junpei Kawamoto <kawamoto.junpei@gmail.com>

# Install packages
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python-pip
RUN pip install --upgrade requests

# Copy scripts
ADD ./bin/*.py /root/bin/

# Set the entrypoint
ENTRYPOINT ["/root/bin/notifier.py"]
CMD [""]

