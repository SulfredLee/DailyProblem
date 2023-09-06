## Commands

```bash
# Local build docker image
$ docker build --target builder -t gcc_vv_cmake:7.2.0 .

# Push to docker hub
# docker tag local-image:tagname new-repo:tagname
$ docker tag gcc_vv_cmake:7.2.0 sulfredlee/gcc_vv_cmake:7.2.0

# login
$ docker login
# push
$ docker push sulfredlee/gcc_vv_cmake:7.2.0
$ docker push sulfredlee/gcc_vv_cmake:latest
```
