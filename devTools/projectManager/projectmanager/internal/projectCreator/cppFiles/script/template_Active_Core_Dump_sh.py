content_st = """
#!/bin/bash
ulimit -c unlimited
sudo bash -c 'echo core.%e.%p.%t > /proc/sys/kernel/core_pattern'

# check output pattern
# sysctl kernel.core_pattern

# change core file name
# echo "core.%e.%p.%t" > /proc/sys/kernel/core_pattern
# sudo bash -c 'echo core.%e.%p.%t > /proc/sys/kernel/core_pattern'
"""
