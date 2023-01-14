## Helm

```bash
# Add new repo and install mysql chart (helm package)
## $ helm repo add <user define label> https://charts.bitnami.com/bitnami
$ helm repo add bitnami https://charts.bitnami.com/bitnami
## $ helm install <user define pod label> <user define label>/mysql
$ helm install mysql-svc bitnami/mysql

# check repo list
$ helm repo list
NAME    URL
stable  https://charts.helm.sh/stable
bitnami https://charts.bitnami.com/bitnami

# show what can you config in the specific chart (helm package)
$ helm show values bitnami/mysql
# change variable in a chart (helm package) dynamically
$ helm upgrade mysql-svc bitnami/mysql --set database.adminPassword=admin

```

## kubectl

```bash
# Update yaml values dynamically
$ kubectl edit svc <your service>
```
