content_st = """
## {{ project_name }}

### How to publish to pypi
```bash
# set up pypi token
$ poetry config pypi-token.pypi my-token

# build the project
$ poetry build

# publish the project
$ poetry publish

# DONE
```

### How to use QC CLI
[reference](https://www.quantconnect.com/docs/v2/lean-cli)
```bash
# Install lean
$ poetry add lean
$ poetry install

# Login
$ poetry run lean login --user-id xxx --api-token xxx

# Initial workspace
$ poetry run lean init

# Pull projects
$ poetry run lean cloud pull

# Push projects
$ poetry run lean cloud push
```

### kubernetes helm related
```bash
# check helm template
$ helm template {{ project_name_hyphen }} ./chart --values=./chart/template_values_dev_yaml.py

# install helm chart
$ helm upgrade --wait --timeout=1200s --install --values ./chart/template_values_dev_yaml.py {{ project_name_hyphen }} ./chart

# uninstall helm chart
$ helm uninstall {{ project_name_hyphen }}
```
"""
