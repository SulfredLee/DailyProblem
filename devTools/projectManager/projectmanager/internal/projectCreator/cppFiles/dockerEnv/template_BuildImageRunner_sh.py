content_st = """
#!/bin/bash

docker build --target runner -t {{ project_name }}_run_env:1.0.0 .
"""
