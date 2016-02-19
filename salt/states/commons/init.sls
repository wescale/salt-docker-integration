# Needs SELinux commands
selinux-utils:
  pkg.latest:
    - name: policycoreutils-python

# Provides a Makefile to compile
# type enforcement files
selinux-policy-devel:
  pkg.latest

lsof:
  pkg.latest
