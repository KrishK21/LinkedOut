from flask import Flask
from flask_cors import CORS

from db import get_db, close_db, init_db
from jobs import jobs_bp

import auth as auth_module

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

CORS(app)

# Close DB connection after every request
app.teardown_appcontext(close_db)

# Register jobs blueprint
app.register_blueprint(jobs_bp, url_prefix="/jobs")

# Re-register auth routes from auth.py onto this app
app.add_url_rule("/signup",  view_func=auth_module.signup,  methods=["POST"])
app.add_url_rule("/login",   view_func=auth_module.login,   methods=["POST"])
app.add_url_rule("/profile", view_func=auth_module.profile, methods=["GET", "POST"])
app.add_url_rule("/",        view_func=auth_module.home)
app.add_url_rule("/health",  view_func=auth_module.health)
app.add_url_rule("/db-test", view_func=auth_module.db_test)
app.add_url_rule("/home",    view_func=auth_module.homepage)
app.add_url_rule("/profile-page", view_func=auth_module.profilePage)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    # use if running into port issues.  app.run(debug=True, port=5004)
