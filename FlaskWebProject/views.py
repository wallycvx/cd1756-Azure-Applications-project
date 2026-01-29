"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db
from FlaskWebProject.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import msal
import uuid
import os
# NEW: Azure Blob Storage client
from azure.storage.blob import BlobServiceClient

def get_container_client():
    """Create and return a container client using the connection string."""
    blob_service = BlobServiceClient.from_connection_string(
        app.config["BLOB_CONNECTION_STRING"]
    )
    return blob_service.get_container_client(app.config["BLOB_CONTAINER"])

imageSourceUrl = (
    "https://"
    + app.config["BLOB_ACCOUNT"]
    + ".blob.core.windows.net/"
    + app.config["BLOB_CONTAINER"]
    + "/"
)

@app.route("/")
@app.route("/home")
@login_required
def home():
    # user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template("index.html", title="Home Page", posts=posts)

@app.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        # Pass container client to model
        container_client = get_container_client()
        post.save_changes(form, request.files["image_path"], current_user.id, container_client, new=True)
        return redirect(url_for("home"))
    return render_template(
        "post.html",
        title="Create Post",
        imageSource=imageSourceUrl,
        form=form,
    )

@app.route("/post/<int:id>", methods=["GET", "POST"])
@login_required
def post(id):
    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        container_client = get_container_client()
        post.save_changes(form, request.files["image_path"], current_user.id, container_client)
        return redirect(url_for("home"))
    return render_template(
        "post.html",
        title="Edit Post",
        imageSource=imageSourceUrl,
        form=form,
    )

# LOGIN Local and MS Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    
    # Add this line to see the redirect URI Azure expects
    print("PRODUCTION REDIRECT URI:", url_for("authorized", _external=True))
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template("login.html", title="Sign In", form=form, auth_url=auth_url)

# Microsoft Authentication redirect route
@app.route(Config.REDIRECT_PATH)
def authorized():
    if request.args.get("state") != session.get("state"):
        return redirect(url_for("login")) # change home to 

    if "error" in request.args:
        return render_template("auth_error.html", result=request.args)

    code = request.args.get("code")
    if not code:
        return redirect(url_for("login"))

    cache = _load_cache()
    msal_app = _build_msal_app(cache=cache)

    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=Config.SCOPE,
        redirect_uri=url_for("authorized", _external=True),
    )

    if "error" in result:
        return render_template("auth_error.html", result=result)

    session["user"] = result.get("id_token_claims")
    _save_cache(cache)

    # Extract Microsoft account user email
    ms_email = session["user"].get("preferred_username")

        # Check if user exists
    user = User.query.filter_by(username=ms_email).first()

    # If not, create a new user
    if not user:
        user = User(username=ms_email)
        user.set_password(uuid.uuid4().hex)  # random password
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("home"))

# LOGOUT route
@app.route("/logout")
def logout():
    logout_user()
    if session.get("user"):
        session.clear()
        return redirect(
            Config.AUTHORITY
            + "/oauth2/v2.0/logout"
            + "?post_logout_redirect_uri="
            + url_for("login", _external=True)
        )
    return redirect(url_for("login"))

# debug route to show redirect URI
@app.route("/debug-redirect")
def debug_redirect():
    return url_for("authorized", _external=True)

# Load MSAL token cache
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

# Save MSAL token cache
def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

# Build MSAL ConfidentialClientApplication
def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        client_id=Config.CLIENT_ID,
        client_credential=Config.CLIENT_SECRET,
        authority=authority,
        token_cache=cache,
    )

# Build full Microsoft login URL
def _build_auth_url(authority=None, scopes=None, state=None):
    msal_app = _build_msal_app(authority=authority)
    return msal_app.get_authorization_request_url(
        scopes=scopes,
        state=state,
        redirect_uri=url_for("authorized", _external=True),
    )