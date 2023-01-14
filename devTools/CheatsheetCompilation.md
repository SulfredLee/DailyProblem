## Helm

```bash
# Add new repo and install mysql package (charts)
## $ helm repo add <user define label> https://charts.bitnami.com/bitnami
$ helm repo add bitnami https://charts.bitnami.com/bitnami
## $ helm install <user define pod label> bitnami/mysql
$ helm install mysql-svc bitnami/mysql

$ helm repo list
NAME    URL
stable  https://charts.helm.sh/stable
bitnami https://charts.bitnami.com/bitnami
```
