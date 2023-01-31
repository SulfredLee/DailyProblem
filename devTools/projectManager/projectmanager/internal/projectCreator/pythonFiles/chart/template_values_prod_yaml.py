content_st = """
ImageNameTag: registry.gitlab.com/<gitlab group path>/{{ project_name }}:runner_1.0.0

service:
  # {}
  # type: ClusterIP
  type: LoadBalancer
  ports:
    - name: website
      port: 5000
      protocol: TCP
      targetPort: 5000
    - name: grpc-api
      port: 50051
      protocol: TCP
      targetPort: 50051
  env:
    - name: FLASK_APP
      value: "app"
    - name: FLASK_DEBUG
      value: "False"
    - name: FLASK_RUN_HOST
      value: "0.0.0.0"
    - name: FLASK_RUN_PORT
      value: "5000"
    - name: GRPC_RUN_HOST
      value: "localhost"
    - name: GRPC_RUN_PORT
      vlaue: "50051"
  customProbe:
    readinessProbe:
      initialDelaySeconds: 15
      httpGet:
        path: /healthcheck
        port: 5000
    livenessProbe:
      initialDelaySeconds: 15
      httpGet:
        path: /healthcheck
        port: 5000
"""
