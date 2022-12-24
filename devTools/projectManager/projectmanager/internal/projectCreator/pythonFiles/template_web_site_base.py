content_st = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title or "Microblog" }}</title>
        <link rel="stylesheet" href="/static/css/styles.css" />
    </head>
    <body>
        {% block content %}
        <p>Hello, world!</p>
        {% endblock %}
    </body>
</html>
"""
