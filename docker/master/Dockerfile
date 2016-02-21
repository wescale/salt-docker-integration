FROM centos:7.0.1406
MAINTAINER "slemesle" <seven.lemesle@wescale.fr>
RUN yum -y swap -- remove fakesystemd -- install systemd systemd-libs
RUN yum -y install curl
RUN curl -L https://bootstrap.saltstack.com -o /install_salt.sh
RUN sh install_salt.sh -F -Z -P -M -N -X stable
RUN mkdir -p /etc/salt/master.d
RUN mkdir -p /app/cd-factory
ADD ./master.conf /etc/salt/master.d/master.conf
ADD run.sh /usr/local/bin/run.sh
VOLUME ["/srv/salt"]
EXPOSE 4505 4506
CMD ["/usr/local/bin/run.sh"]