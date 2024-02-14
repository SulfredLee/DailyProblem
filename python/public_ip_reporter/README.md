
## public_ip_reporter

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
$ helm template public-ip-reporter ./chart --values=./chart/values.dev.yaml

# install helm chart
$ helm upgrade --wait --timeout=1200s --install --values ./chart/values.dev.yaml public-ip-reporter ./chart

# uninstall helm chart
$ helm uninstall public-ip-reporter
```

### GRPC related
[reference](https://github.com/chelseafarley/PythonGrpc)
```bash
# generate python script from proto file
$ cd public_ip_reporter/app/grpc_api
$ poetry run python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/public_ip_reporter.proto

$ poetry add grpcio-tools