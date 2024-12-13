from datetime import datetime, timezone
from webbrowser import get
from flask import flash, redirect, render_template, request, url_for
from urllib.parse import urlparse
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import (
    AboutUsSectionForm,
    CarouselForm,
    EditProfileForm,
    EventsForm,
    FeaturedArticleForm,
    HomepageWhoWeAreForm,
    IndustryUpdatesForm,
    LatestNewsForm,
    LatestVideosForm,
    LeadershipForm,
    LoginForm,
    MissionItemsForm,
    OurImpactForm,
    PartnerForm,
    RegistrationForm,
    ValuesItemsForm,
)
from app.models import (
    AboutUsSection,
    Events,
    FeaturedArticle,
    HomePageWhoWeAre,
    IndustryUpdates,
    LatestVideos,
    Leadership,
    MissionItems,
    OurImpact,
    Partner,
    User,
    Carousel,
    ValuesItems,
    LatestNews,
)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/")
@login_required
def index():
    return redirect(url_for("manage_admins"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    form.username.data = request.form.get("username")
    form.password.data = request.form.get("password")
    form.remember_me.data = bool(request.form.get("remember_me"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if (
            not next_page
            or urlparse(next_page).netloc != ""
            or urlparse(next_page).path.startswith("www.")
        ):
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("admin/login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered an admin!")
        return redirect(url_for("manage_admins"))
    return render_template("admin/register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        "templates/edit_profile.html", title="Edit Profile", form=form
    )


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} not found".format(username))
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot follow yourself")
        return redirect(url_for("user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash("You are now following {}".format(username))
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} not found".format(username))
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot unfollow yourself")
        return redirect(url_for("user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash("You are now unfollowing {}".format(username))
    return redirect(url_for("user", username=username))


# CSDD ADMIN DASHBOARD
@app.route("/admins")
@login_required
def manage_admins():
    admins = User.query.all()
    return render_template(
        "admin/manage_admins.html", admins=admins, title="Manage Admins"
    )


@app.route("/admins/remove_admin/<id>")
@login_required
def remove_admin(id):
    admin = User.query.filter_by(id=id)
    admin.first_or_404()
    admin.delete()
    db.session.commit()
    flash("Admin successfully deleted!")
    return redirect(url_for("manage_admins"))


@app.route("/edit/homepage/who-we-are", methods=["GET", "POST"])
@login_required
def homepage_who_we_are():
    form = HomepageWhoWeAreForm()
    query = HomePageWhoWeAre.query
    homepage_data = query.first()
    if form.validate_on_submit():
        if homepage_data is None:
            homepage_data = HomePageWhoWeAre(
                section_title=form.section_title.data,  # type: ignore
                section_body=form.section_body.data,  # type: ignore
                section_image_path=form.section_image_path.data,  # type: ignore
            )
            db.session.add(homepage_data)
            db.session.commit()
            flash("Data has been saved successfully!")
        else:
            query.update(
                {
                    "section_title": form.section_title.data,
                    "section_body": form.section_body.data,
                    "section_image_path": form.section_image_path.data,
                }
            )
            db.session.commit()
            flash("Changes have been saved successfully!")
        return redirect(url_for("homepage_who_we_are"))
    elif request.method == "GET":
        if homepage_data is not None:
            form.section_title.data = homepage_data.section_title
            form.section_body.data = homepage_data.section_body
            form.section_image_path.data = homepage_data.section_image_path
    return render_template(
        "admin/homepage/who_we_are.html", title="HomePage - Who We Are", form=form
    )


@app.route("/edit/homepage/featured-article", methods=["GET", "POST"])
@login_required
def homepage_featured_article():
    form = FeaturedArticleForm()
    query = FeaturedArticle.query
    featured_article_data = query.first()
    if form.validate_on_submit():
        if featured_article_data is None:
            featured_article_data = FeaturedArticle(
                section_title=form.section_title.data,  # type: ignore
                section_body=form.section_body.data,  # type: ignore
                section_image_path=form.section_image_path.data,  # type: ignore
            )
            db.session.add(featured_article_data)
            db.session.commit()
            flash("Data has been saved successfully!")
        else:
            query.update(
                {
                    "section_title": form.section_title.data,
                    "section_body": form.section_body.data,
                    "section_image_path": form.section_image_path.data,
                }
            )
            db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("homepage_featured_article"))
    elif request.method == "GET":
        if featured_article_data is not None:
            form.section_title.data = featured_article_data.section_title
            form.section_body.data = featured_article_data.section_body
            form.section_image_path.data = featured_article_data.section_image_path
    return render_template(
        "admin/homepage/featured_article.html",
        title="HomePage - Featured Article",
        form=form,
    )


@app.route("/homepage/carousel")
@login_required
def homepage_carousel():
    section_data = Carousel.query.all()
    return render_template(
        "admin/homepage/carousel.html",
        title="Carousel Data",
        section_data=section_data,
    )


@app.route("/homepage/carousel/new", methods=["GET", "POST"])
@login_required
def homepage_carousel_new():
    form = CarouselForm()
    if form.validate_on_submit():
        carousel_data = Carousel(
            section_title=form.section_title.data,  # type: ignore
            section_image_path=form.section_image_path.data,  # type: ignore
        )
        db.session.add(carousel_data)
        db.session.commit()
        flash("Data has been saved successfully!")
        return redirect(url_for("homepage_carousel"))
    return render_template(
        "admin/homepage/carousel_edit.html", title="Homepage - Carousel", form=form
    )


@app.route("/homepage/carousel/<id>", methods=["GET", "POST"])
@login_required
def homepage_carousel_edit(id):
    query = Carousel.query.filter_by(id=id)
    carousel_data = query.first_or_404()
    form = CarouselForm()
    if form.validate_on_submit():
        query.update(
            {
                "section_title": form.section_title.data,
                "section_image_path": form.section_image_path.data,
            }
        )
        db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("homepage_carousel_edit", id=id))
    form.section_title.data = carousel_data.section_title
    form.section_image_path.data = carousel_data.section_image_path
    return render_template(
        "admin/homepage/carousel_edit.html", title="Homepage - Carousel", form=form
    )


@app.route("/homepage/carousel/delete/<id>")
@login_required
def homepage_carousel_delete(id):
    query = Carousel.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("homepage_carousel"))


@app.route("/homepage/our_impact")
@login_required
def homepage_our_impact():
    section_data = OurImpact.query.all()
    return render_template(
        "admin/homepage/our_impact.html",
        title="Our Impact Data",
        section_data=section_data,
    )


@app.route("/homepage/our_impact/new", methods=["GET", "POST"])
@login_required
def homepage_our_impact_new():
    form = OurImpactForm()
    if form.validate_on_submit():
        our_impact_data = OurImpact(
            section_count=form.section_count.data,  # type: ignore
            section_title=form.section_title.data,  # type: ignore
            section_body=form.section_body.data,  # type: ignore
            section_suffix=form.section_suffix.data,  # type: ignore
        )
        db.session.add(our_impact_data)
        db.session.commit()
        flash("Data has been saved successfully!")
        return redirect(url_for("homepage_our_impact"))
    return render_template(
        "admin/homepage/our_impact_edit.html", title="Homepage - Our Impact", form=form
    )


@app.route("/homepage/our_impact/<id>", methods=["GET", "POST"])
@login_required
def homepage_our_impact_edit(id):
    query = OurImpact.query.filter_by(id=id)
    our_impact_data = query.first_or_404()
    form = OurImpactForm()
    if form.validate_on_submit():
        query.update(
            {
                "section_count": form.section_count.data,
                "section_title": form.section_title.data,
                "section_body": form.section_body.data,
                "section_suffix": form.section_suffix.data,
            }
        )
        db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("homepage_our_impact_edit", id=id))
    form.section_count.data = our_impact_data.section_count
    form.section_title.data = our_impact_data.section_title
    form.section_body.data = our_impact_data.section_body
    form.section_suffix.data = our_impact_data.section_suffix
    return render_template(
        "admin/homepage/our_impact_edit.html", title="Homepage - Our Impact", form=form
    )


@app.route("/homepage/our_impact/delete/<id>")
@login_required
def homepage_our_impact_delete(id):
    query = OurImpact.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("homepage_our_impact"))


@app.route("/about_us_section", methods=["GET", "POST"])
@login_required
def about_us_section():
    form = AboutUsSectionForm()
    query = AboutUsSection.query
    about_us_section_data = query.first()
    if form.validate_on_submit():
        if about_us_section_data is None:
            about_us_section_data = AboutUsSection(
                section_about_us_title=form.section_about_us_title.data,  # type: ignore
                section_about_us_body=form.section_about_us_body.data,  # type: ignore
                section_about_us_image_path=form.section_about_us_image_path.data,  # type: ignore
                section_mission_title=form.section_mission_title.data,  # type: ignore
                section_mission_image_path=form.section_mission_image_path.data,  # type: ignore
                section_our_vision_title=form.section_our_vision_title.data,  # type: ignore
                section_our_vision_body=form.section_our_vision_body.data,  # type: ignore
                section_vision_image=form.section_vision_image.data,  # type: ignore
                section_our_values_title=form.section_our_values_title.data,  # type: ignore
            )
            db.session.add(about_us_section_data)
            db.session.commit()
            flash("Data has been saved successfully!")
        else:
            query.update(
                {
                    "section_about_us_title": form.section_about_us_title.data,
                    "section_about_us_body": form.section_about_us_body.data,
                    "section_about_us_image_path": form.section_about_us_image_path.data,
                    "section_mission_title": form.section_mission_title.data,
                    "section_mission_image_path": form.section_mission_image_path.data,
                    "section_our_vision_title": form.section_our_vision_title.data,
                    "section_our_vision_body": form.section_our_vision_body.data,
                    # "section_vision_image": form.section_vision_image.data,
                    "section_our_values_title": form.section_our_values_title.data,
                }
            )
            db.session.commit()
            flash("Changes have been saved successfully!")
        return redirect(url_for("about_us_section"))
    elif request.method == "GET":
        if about_us_section_data is not None:
            form.section_about_us_title.data = (
                about_us_section_data.section_about_us_title
            )
            form.section_about_us_body.data = (
                about_us_section_data.section_about_us_body
            )
            form.section_about_us_image_path.data = (
                about_us_section_data.section_about_us_image_path
            )
            form.section_mission_title.data = (
                about_us_section_data.section_mission_title
            )
            form.section_mission_image_path.data = (
                about_us_section_data.section_mission_image_path
            )
            form.section_our_vision_title.data = (
                about_us_section_data.section_our_vision_title
            )
            form.section_our_vision_body.data = (
                about_us_section_data.section_our_vision_body
            )
            # form.section_vision_image = about_us_section_data.section_vision_image
            form.section_our_values_title.data = (
                about_us_section_data.section_our_values_title
            )

    mission_items = MissionItems.query.all()
    values_items = ValuesItems.query.all()

    return render_template(
        "admin/about_us/about_us_section.html",
        title="About Us Section",
        form=form,
        mission_items=mission_items,
        values_items=values_items,
    )


# OUR MISSION
@app.route("/our_mission/new", methods=["GET", "POST"])
@login_required
def our_mission_new():
    form = MissionItemsForm()
    if form.validate_on_submit():
        our_mission_data = MissionItems(
            section_mission_icon=form.section_mission_icon.data,  # type: ignore
            section_mission_body=form.section_mission_body.data,  # type: ignore
        )
        db.session.add(our_mission_data)
        db.session.commit()
        flash("Data has been saved successfully!")
        return redirect(url_for("about_us_section"))
    return render_template(
        "admin/about_us/our_mission_edit.html", title="Our Mission", form=form
    )


@app.route("/our_mission/<id>", methods=["GET", "POST"])
@login_required
def our_mission_edit(id):
    query = MissionItems.query.filter_by(id=id)
    our_mission_data = query.first_or_404()
    form = MissionItemsForm()
    if form.validate_on_submit():
        query.update(
            {
                "section_mission_icon": form.section_mission_icon.data,
                "section_mission_body": form.section_mission_body.data,
            }
        )
        db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("our_mission_edit", id=id))
    form.section_mission_icon.data = our_mission_data.section_mission_icon
    form.section_mission_body.data = our_mission_data.section_mission_body
    return render_template(
        "admin/about_us/our_mission_edit.html", title="Our Mission", form=form
    )


@app.route("/our_mission/delete/<id>")
@login_required
def our_mission_delete(id):
    query = MissionItems.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("about_us_section"))


# OUR VALUES
@app.route("/our_values/new", methods=["GET", "POST"])
@login_required
def our_values_new():
    form = ValuesItemsForm()
    if form.validate_on_submit():
        our_values_data = ValuesItems(
            section_our_values_icon=form.section_our_values_icon.data,  # type: ignore
            section_our_values_body=form.section_our_values_body.data,  # type: ignore
        )
        db.session.add(our_values_data)
        db.session.commit()
        flash("Data has been saved successfully!")
        return redirect(url_for("about_us_section"))
    return render_template(
        "admin/about_us/our_values_edit.html", title="Our Values", form=form
    )


@app.route("/our_values/<id>", methods=["GET", "POST"])
@login_required
def our_values_edit(id):
    query = ValuesItems.query.filter_by(id=id)
    our_values_data = query.first_or_404()
    form = ValuesItemsForm()
    if form.validate_on_submit():
        query.update(
            {
                "section_our_values_icon": form.section_our_values_icon.data,
                "section_our_values_body": form.section_our_values_body.data,
            }
        )
        db.session.commit()
        flash("Changes have been saved successfully!")
        return redirect(url_for("our_values_edit", id=id))
    form.section_our_values_icon.data = our_values_data.section_our_values_icon
    form.section_our_values_body.data = our_values_data.section_our_values_body
    return render_template(
        "admin/about_us/our_values_edit.html", title="Our Values", form=form
    )


@app.route("/our_values/delete/<id>")
@login_required
def our_values_delete(id):
    query = ValuesItems.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("about_us_section"))


# LEADERSHIP
@app.route("/leadership")
@login_required
def leadership():
    leadership_data = Leadership.query.all()
    return render_template(
        "admin/about_us/leadership.html",
        title="Leadership",
        leadership_data=leadership_data,
    )


@app.route("/leadership/new", methods=["GET", "POST"])
@login_required
def leadership_new():
    form = LeadershipForm()
    if form.validate_on_submit():
        data = Leadership(
            leadership_name=form.leadership_name.data,  # type: ignore
            leadership_titles=form.leadership_titles.data,  # type: ignore
            leadership_logo=form.leadership_logo.data,  # type: ignore
            leadership_position=form.leadership_position.data,  # type: ignore
            is_management=form.is_management.data,  # type: ignore
            leadership_body=form.leadership_body.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("leadership"))
    return render_template(
        "admin/about_us/leadership_edit.html", title="Leadership", form=form
    )


@app.route("/leadership/<id>", methods=["GET", "POST"])
@login_required
def leadership_edit(id):
    query = Leadership.query.filter_by(id=id)
    leadership_data = query.first_or_404()
    form = LeadershipForm()
    if form.validate_on_submit():
        query.update(
            {
                "leadership_name": form.leadership_name.data,
                "leadership_titles": form.leadership_titles.data,
                "leadership_logo": form.leadership_logo.data,
                "leadership_position": form.leadership_position.data,
                "is_management": form.is_management.data,
                "leadership_body": form.leadership_body.data,
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("leadership"))
    form.leadership_name.data = leadership_data.leadership_name
    form.leadership_titles.data = leadership_data.leadership_titles
    form.leadership_logo.data = leadership_data.leadership_logo
    form.leadership_position.data = leadership_data.leadership_position
    form.is_management.data = leadership_data.is_management
    form.leadership_body.data = leadership_data.leadership_body
    return render_template(
        "admin/about_us/leadership_edit.html", title="Leadership", form=form
    )


@app.route("/leadership/delete/<id>")
@login_required
def leadership_delete(id):
    query = Leadership.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("leadership"))


# PARTNERS
@app.route("/partners")
@login_required
def partners():
    partners_data = Partner.query.all()
    return render_template(
        "admin/about_us/partners.html", title="Partners", partners_data=partners_data
    )


@app.route("/partners/new", methods=["GET", "POST"])
@login_required
def partner_new():
    form = PartnerForm()
    if form.validate_on_submit():
        data = Partner(
            partner_name=form.partner_name.data,  # type: ignore
            partner_description=form.partner_description.data,  # type: ignore
            partner_logo=form.partner_logo.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("partners"))
    return render_template(
        "admin/about_us/partners_edit.html", title="Partner", form=form
    )


@app.route("/partners/<id>", methods=["GET", "POST"])
@login_required
def partner_edit(id):
    query = Partner.query.filter_by(id=id)
    partner_data = query.first_or_404()
    form = PartnerForm()
    if form.validate_on_submit():
        query.update(
            {
                "partner_name": form.partner_name.data,
                "partner_description": form.partner_description.data,
                "partner_logo": form.partner_logo.data,
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("partners"))
    form.partner_name.data = partner_data.partner_name
    form.partner_description.data = partner_data.partner_description
    form.partner_logo.data = partner_data.partner_logo
    return render_template(
        "admin/about_us/partners_edit.html", title="Partner", form=form
    )


@app.route("/partners/delete/<id>")
@login_required
def partner_delete(id):
    query = Partner.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("partners"))


# LATEST NEWS
@app.route("/latest_news")
@login_required
def latest_news():
    latest_news = LatestNews.query.all()
    return render_template(
        "admin/latest_news.html", title="Latest News", latest_news=latest_news
    )


@app.route("/latest_news/new", methods=["GET", "POST"])
@login_required
def latest_news_new():
    form = LatestNewsForm()
    if form.validate_on_submit():
        data = LatestNews(
            latest_news_title=form.latest_news_title.data,  # type: ignore
            latest_news_image=form.latest_news_image.data,  # type: ignore
            latest_news_body=form.latest_news_body.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("latest_news"))
    return render_template(
        "admin/latest_news_edit.html", title="Latest News", form=form
    )


@app.route("/latest_news/<id>", methods=["GET", "POST"])
@login_required
def latest_news_edit(id):
    query = LatestNews.query.filter_by(id=id)
    latest_news_data = query.first_or_404()
    form = LatestNewsForm()
    if form.validate_on_submit():
        query.update(
            {
                "latest_news_title": form.latest_news_title.data,
                "latest_news_image": form.latest_news_image.data,
                "latest_news_body": form.latest_news_body.data,
                "last_modified": datetime.now(timezone.utc),
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("latest_news"))
    form.latest_news_title.data = latest_news_data.latest_news_title
    form.latest_news_image.data = latest_news_data.latest_news_image
    form.latest_news_body.data = latest_news_data.latest_news_body
    return render_template(
        "admin/latest_news_edit.html", title="Latest News", form=form
    )


@app.route("/latest_news/delete/<id>")
@login_required
def latest_news_delete(id):
    query = LatestNews.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("latest_news"))


# LATEST VIDEOS
@app.route("/latest_videos")
@login_required
def latest_videos():
    latest_videos = LatestVideos.query.all()
    return render_template(
        "admin/latest_videos.html", title="Latest Videos", latest_videos=latest_videos
    )


@app.route("/latest_videos/new", methods=["GET", "POST"])
@login_required
def latest_videos_new():
    form = LatestVideosForm()
    if form.validate_on_submit():
        data = LatestVideos(
            latest_videos_title=form.latest_videos_title.data,  # type: ignore
            latest_videos_link=form.latest_videos_link.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("latest_videos"))
    return render_template(
        "admin/latest_videos_edit.html", title="Latest Videos", form=form
    )


@app.route("/latest_videos/<id>", methods=["GET", "POST"])
@login_required
def latest_videos_edit(id):
    query = LatestVideos.query.filter_by(id=id)
    latest_videos_data = query.first_or_404()
    form = LatestVideosForm()
    if form.validate_on_submit():
        query.update(
            {
                "latest_videos_title": form.latest_videos_title.data,
                "latest_videos_link": form.latest_videos_link.data,
                "last_modified": datetime.now(timezone.utc),
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("latest_videos"))
    form.latest_videos_title.data = latest_videos_data.latest_videos_title
    form.latest_videos_link.data = latest_videos_data.latest_videos_link
    return render_template(
        "admin/latest_videos_edit.html", title="Latest Videos", form=form
    )


@app.route("/latest_videos/delete/<id>")
@login_required
def latest_videos_delete(id):
    query = LatestVideos.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("latest_videos"))


# INDUSTRY UPDATES
@app.route("/industry_updates")
@login_required
def industry_updates():
    industry_updates = IndustryUpdates.query.all()
    return render_template(
        "admin/industry_updates.html",
        title="Industry Updates",
        industry_updates=industry_updates,
    )


@app.route("/industry_updates/new", methods=["GET", "POST"])
@login_required
def industry_updates_new():
    form = IndustryUpdatesForm()
    if form.validate_on_submit():
        data = IndustryUpdates(
            industry_updates_title=form.industry_updates_title.data,  # type: ignore
            industry_updates_link=form.industry_updates_link.data,  # type: ignore
            industry_updates_image=form.industry_updates_image.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("industry_updates"))
    return render_template(
        "admin/industry_updates_edit.html", title="Industry Updates", form=form
    )


@app.route("/industry_updates/<id>", methods=["GET", "POST"])
@login_required
def industry_updates_edit(id):
    query = IndustryUpdates.query.filter_by(id=id)
    industry_updates_data = query.first_or_404()
    form = IndustryUpdatesForm()
    if form.validate_on_submit():
        query.update(
            {
                "industry_updates_title": form.industry_updates_title.data,
                "industry_updates_link": form.industry_updates_link.data,
                "industry_updates_image": form.industry_updates_image.data,
                "last_modified": datetime.now(timezone.utc),
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("industry_updates"))
    form.industry_updates_title.data = industry_updates_data.industry_updates_title
    form.industry_updates_link.data = industry_updates_data.industry_updates_link
    form.industry_updates_image.data = industry_updates_data.industry_updates_image
    return render_template(
        "admin/industry_updates_edit.html", title="Industry Updates", form=form
    )


@app.route("/industry_updates/delete/<id>")
@login_required
def industry_updates_delete(id):
    query = IndustryUpdates.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("industry_updates"))


# EVENTS
@app.route("/events")
@login_required
def events():
    events_data = Events.query.all()
    return render_template("admin/events.html", title="Events", events_data=events_data)


@app.route("/events/new", methods=["GET", "POST"])
@login_required
def events_new():
    form = EventsForm()
    if form.validate_on_submit():
        data = Events(
            event_title=form.event_title.data,  # type: ignore
            event_image=form.event_image.data,  # type: ignore
            event_body=form.event_body.data,  # type: ignore
            upcoming_event=form.upcoming_event.data,  # type: ignore
        )
        db.session.add(data)
        db.session.commit()
        flash("Data has been saved succesfully!")
        return redirect(url_for("events"))
    return render_template("admin/events_edit.html", title="Events", form=form)


@app.route("/events/<id>", methods=["GET", "POST"])
@login_required
def events_edit(id):
    query = Events.query.filter_by(id=id)
    events_data = query.first_or_404()
    form = EventsForm()
    if form.validate_on_submit():
        query.update(
            {
                "event_title": form.event_title.data,
                "event_image": form.event_image.data,
                "event_body": form.event_body.data,
                "upcoming_event": form.upcoming_event.data,
                "last_modified": datetime.now(timezone.utc),
            }
        )
        db.session.commit()
        flash("Data has been updated successfully!")
        return redirect(url_for("events"))
    form.event_title.data = events_data.event_title
    form.event_image.data = events_data.event_image
    form.event_body.data = events_data.event_body
    form.upcoming_event.data = events_data.upcoming_event
    return render_template("admin/events_edit.html", title="Events", form=form)


@app.route("/events/delete/<id>")
@login_required
def events_delete(id):
    query = Events.query.filter_by(id=id)
    query.first_or_404()
    query.delete(synchronize_session="auto")
    db.session.commit()
    flash("Data deleted successfully!")
    return redirect(url_for("events"))
