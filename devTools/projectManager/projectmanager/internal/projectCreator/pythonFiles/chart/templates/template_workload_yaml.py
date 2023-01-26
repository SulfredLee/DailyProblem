content_st = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ project_name_hyphen }}
spec:
  selector:
    matchLabels:
      app: {{ project_name_hyphen }}
  replicas: 1
  template: # template for the pods
    metadata:
      labels:
        app: {{ project_name_hyphen }}
    spec:
      containers:
      - name: {{ project_name_hyphen }}
        # Note to deployer - add -dev at the end of here for development version
        # https://juju.is/tutorials/using-gitlab-as-a-container-registry#7-pull-your-container
        # https://stackoverflow.com/questions/49669077/helm-chart-deployment-and-private-docker-repository
        # https://medium.com/devops-with-valentine/gitlab-ci-how-to-pull-a-private-docker-image-from-aws-ecr-in-your-pipeline-515285569231
        image: {% raw %}{{ .Values.ImageNameTag }}{% endraw %}
        env:
{% raw %}{{ toYaml .Values.service.env | indent 10 }}{% endraw %}
      imagePullSecrets:
      - name: {{ project_name_hyphen }}-regcred
---
apiVersion: v1
kind: Service
metadata:
  name: srv-{{ project_name_hyphen }}

spec:
  selector:
    app: {{ project_name_hyphen }}

  ports:
{% raw %}{{ toYaml .Values.service.ports | indent 4 }}{% endraw %}
  type: {% raw %}{{ .Values.service.type }}{% endraw %}
"""
