## Commands

```bash
# Local build docker image
$ docker build --target builder -t aws-k8s-mm-local:1.0.0 .

# Push to docker hub
# docker tag local-image:tagname new-repo:tagname
$ docker tag aws-k8s-mm-local:1.0.0 sulfredlee/aws-k8s-management:tagname

# login
$ docker login
# push
$ docker push sulfredlee/aws-k8s-management:tagname
$ docker push sulfredlee/aws-k8s-management:latest
```
