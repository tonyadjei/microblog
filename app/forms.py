from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
    IntegerField,
)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # custom flask_wtf validators (must begin with validate_<field_name>)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    # custom validator to prevent duplicate username entries

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")


class HomepageWhoWeAreForm(FlaskForm):
    section_title = StringField("Title", validators=[Length(min=5, max=20)])
    section_body = TextAreaField("Body", validators=[Length(min=0, max=400)])
    section_image_path = StringField(
        "Upload Image Path", validators=[Length(min=0, max=255)]
    )
    submit = SubmitField("Submit")


class FeaturedArticleForm(FlaskForm):
    section_title = StringField("Title", validators=[Length(min=5, max=150)])
    section_body = TextAreaField("Body", validators=[Length(min=0, max=400)])
    section_image_path = StringField(
        "Upload Image Path", validators=[Length(min=0, max=255)]
    )
    submit = SubmitField("Submit")


class CarouselForm(FlaskForm):
    section_title = StringField("Carousel Title", validators=[Length(min=5, max=200)])
    section_image_path = StringField(
        "Upload Image Path", validators=[Length(min=0, max=255)]
    )
    submit = SubmitField("Submit")


class OurImpactForm(FlaskForm):
    section_count = IntegerField("Count", validators=[DataRequired()])
    section_title = StringField("Title", validators=[Length(min=0, max=100)])
    section_suffix = StringField("Suffix", validators=[Length(min=0, max=10)])
    section_body = StringField("Body", validators=[Length(min=0, max=100)])
    submit = SubmitField("Submit")


class AboutUsSectionForm(FlaskForm):
    section_about_us_title = StringField(
        "About Us Section Title", validators=[Length(min=5, max=150)]
    )
    section_about_us_body = TextAreaField(
        "About Us Body", validators=[Length(min=0, max=1000)]
    )
    section_about_us_image_path = StringField(
        "Upload About Us Section Image Path", validators=[Length(min=0, max=255)]
    )
    section_mission_title = StringField(
        "Mission Section Title", validators=[Length(min=5, max=150)]
    )
    section_mission_image_path = StringField(
        "Upload Mission Section Image Path", validators=[Length(min=0, max=255)]
    )
    section_our_vision_title = StringField(
        "Our Vision Section Title", validators=[Length(min=5, max=150)]
    )
    section_our_vision_body = TextAreaField(
        "Our Vision Body", validators=[Length(min=0, max=400)]
    )
    # code below gives an error (not yet fixed)
    # section_vision_image = StringField(
    #     "Upload Vision Section Image Path",

    # )
    section_our_values_title = StringField(
        "Our Values Section Title", validators=[Length(min=5, max=150)]
    )
    submit = SubmitField("Submit")


class MissionItemsForm(FlaskForm):
    section_mission_icon = StringField(
        "Mission Icon", validators=[Length(min=5, max=150)]
    )
    section_mission_body = StringField(
        "Mission Body", validators=[Length(min=0, max=200)]
    )
    submit = SubmitField("Submit")


class ValuesItemsForm(FlaskForm):
    section_our_values_icon = StringField(
        "Our Values Icon", validators=[Length(min=5, max=150)]
    )
    section_our_values_body = StringField(
        "Our Values Body", validators=[Length(min=0, max=200)]
    )
    submit = SubmitField("Submit")


class LeadershipForm(FlaskForm):
    leadership_name = StringField("Name", validators=[Length(min=0, max=150)])
    leadership_titles = StringField("Titles", validators=[Length(min=0, max=150)])
    leadership_logo = StringField("Image Path", validators=[Length(min=0, max=255)])
    leadership_position = StringField("Position", validators=[Length(min=0, max=150)])
    is_management = BooleanField("Is Management")
    leadership_body = TextAreaField("Body", validators=[Length(min=0, max=600)])

    submit = SubmitField("Submit")


class PartnerForm(FlaskForm):
    partner_name = StringField("Name", validators=[DataRequired()])
    partner_description = TextAreaField(
        "Description", validators=[Length(min=0, max=200)]
    )
    partner_logo = StringField("Logo Image Path", validators=[Length(min=0, max=255)])
    submit = SubmitField("Submit")


class LatestNewsForm(FlaskForm):
    latest_news_title = StringField("Title", validators=[Length(min=0, max=200)])
    latest_news_body = TextAreaField("Body", validators=[Length(min=0, max=1000)])
    latest_news_image = StringField(
        "Article Image Path", validators=[Length(min=0, max=255)]
    )
    submit = SubmitField("Submit")


class LatestVideosForm(FlaskForm):
    latest_videos_title = StringField(
        "Video Title", validators=[Length(min=0, max=200)]
    )
    latest_videos_link = StringField("Video Link", validators=[Length(min=0, max=255)])
    submit = SubmitField("Submit")


class IndustryUpdatesForm(FlaskForm):
    industry_updates_title = StringField("Title", validators=[Length(min=0, max=200)])
    industry_updates_image = StringField(
        "Article Image Path", validators=[Length(min=0, max=255)]
    )
    industry_updates_link = StringField(
        "Article Link", validators=[Length(min=0, max=255)]
    )
    submit = SubmitField("Submit")


class EventsForm(FlaskForm):
    event_title = StringField("Title", validators=[Length(min=0, max=200)])
    event_image = StringField("Event Image Path", validators=[Length(min=0, max=255)])
    event_body = TextAreaField("Body", validators=[Length(min=0, max=1000)])
    upcoming_event = BooleanField("Upcoming Event")
    submit = SubmitField("Submit")
