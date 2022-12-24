content_st = """
html {
  font-family: Lato, sans-serif;
}

*,
*::after,
*::before {
  box-sizing: inherit;
}

body {
  box-sizing: border-box;
  margin: 0;
}

.navbar {
  max-width: 640px;
  margin: 50px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: 24px;
}

.navbar__brand {
  display: flex;
  align-items: center;
}

.navbar__logo {
  margin-right: 30px;
}

.navbar__navigation {
  display: flex;
  flex-direction: row;
  padding: 0;
  list-style: none;
  color: #5c6b70;
}

.navbar__navigation-item {
  margin-left: 50px;
}

.navbar__link {
  text-decoration: none;
  color: inherit;
}

.main {
  max-width: 450px;
  margin: 0 auto;
  padding: 0 20px;
}

.form {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.form__input {
  width: 100%;
}

.form__label {
  display: block;
  margin-bottom: 10px;
}

.form__textarea {
  width: inherit;
  font-size: 18px;
  padding: 12px 20px;
  border: none;
  background-color: #f3f6f6;
  margin-bottom: 10px;
}

.form__submit {
  background-color: #3cd0ff;
  border: none;
  font-size: 18px;
  font-weight: bold;
  padding: 5px 30px;
  border-radius: 20px;
  color: white;
  cursor: pointer;
}

.form__submit:hover {
  background-color: #18c1e1;
}

.entry {
  margin-top: 50px;
}
"""
