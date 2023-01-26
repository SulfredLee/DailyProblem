content_st = """
ImageNameTag: {{ project_name }}:runner_1.0.0_{{ cur_name }}

service:
  # {}
  # type: ClusterIP
  type: LoadBalancer
  ports:
    - name: website
      port: 5000
      protocol: TCP
      targetPort: 5000
  env:
    - name: FLASK_APP
      value: "app"
    - name: FLASK_DEBUG
      value: "True"
    - name: FLASK_RUN_HOST
      value: "0.0.0.0"
    - name: FLASK_RUN_PORT
      value: "5000"
"""
