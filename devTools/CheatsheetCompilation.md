## Helm

```bash
# Add new repo and install mysql chart (helm package)
# $ helm repo add <user define label> https://charts.bitnami.com/bitnami
$ helm repo add bitnami https://charts.bitnami.com/bitnami
# $ helm install <user define pod label> <user define label>/mysql
$ helm install mysql-svc bitnami/mysql

# check repo list
$ helm repo list
NAME    URL
stable  https://charts.helm.sh/stable
bitnami https://charts.bitnami.com/bitnami

# show what can you config in the specific chart (helm package)
$ helm show values bitnami/mysql > values.yaml
# change variable in a chart (helm package) from command line dynamically
$ helm upgrade mysql-svc bitnami/mysql --set database.adminPassword=admin
# change variable in a chart (helm package) from a file dynamically
$ helm upgrade mysql-svc bitnami/mysql --values=values.yaml

# check all the installed charts (helm package)
$ helm list

# uninstall charts (helm package)
$ helm uninstall <your chart name>

# Record your installations for repeatable infrastructure setup
# download the charts (helm package) without immediately install
$ helm pull bitnami/mysql --untar=ture
# install charts from local files
$ helm install mysql-svc ./mysql
# override by your customized values
$ helm upgrade mysql-svc --values=myvalues.yaml ./mysql

# Generate yaml from charts --- this command will consolidate all your custom values but not installing the environment
$ helm template mysql-svc ./mysql --values=./mysql/myvalues.yaml > mysql-stack.yaml
```

## kubectl

```bash
# Update yaml values dynamically
$ kubectl edit svc <your service>
```
