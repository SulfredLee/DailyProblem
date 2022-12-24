content_st = """
{% extends "base.html" %} {% block content %}
<form method="POST">
    <label>
        E-mail
        <input type="email" name="email" />
    </label>
    <label>
        Password
        <input type="password" name="password" />
    </label>
    <input type="submit" value="Log in" />
</form>
<p><a href="{{ url_for('Authen.signup') }}">Sign up</a> instead</p>
{% endblock %}
"""
