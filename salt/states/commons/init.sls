# Needs SELinux commands
selinux-tools:
  pkg.latest:
    - name: policycoreutils

selinux-utils:
  pkg.latest:
    - name: policycoreutils-python

# Provides a Makefile to compile
# type enforcement files
selinux-policy-devel:
  pkg.latest

lsof:
  pkg.latest

python-pip:
  pkg.installed

