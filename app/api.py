from flask import jsonify, request
from app import app
from app.models import (
    AboutUsSection,
    Events,
    FeaturedArticle,
    HomePageWhoWeAre,
    IndustryUpdates,
    LatestNews,
    Leadership,
    MissionItems,
    OurImpact,
    Partner,
    ValuesItems,
)


@app.route("/api/homepage/who-we-are")
def who_we_are():
    data = HomePageWhoWeAre.query.first()
    return jsonify(data.to_dict())  # type: ignore


@app.route("/api/homepage/our-impact")
def our_impact():
    data = OurImpact.query.all()
    for index in range(len(data)):
        data[index] = data[index].to_dict()
    return jsonify(data)


@app.route("/api/homepage/featured-article")
def featured_article():
    data = FeaturedArticle.query.first()
    kk = FeaturedArticle.query.all()
    return jsonify(data.to_dict())  # type: ignore


@app.route("/api/about-us/all-data")
def about_us():
    about_us_data = AboutUsSection.query.first()
    about_us_data = about_us_data.to_dict()  # type: ignore
    mission_items_data = MissionItems.query.all()
    value_items_data = ValuesItems.query.all()
    for index in range(len(mission_items_data)):
        mission_items_data[index] = mission_items_data[index].to_dict()
    for index in range(len(value_items_data)):
        value_items_data[index] = value_items_data[index].to_dict()
    data = {
        "about_us_data": about_us_data,
        "mission_items": mission_items_data,
        "value_items": value_items_data,
    }
    return jsonify(data)


@app.route("/api/about-us/leadership")
def leadership_api():
    leadership_data = Leadership.query.filter_by(is_management=False).all()
    for index in range(len(leadership_data)):
        leadership_data[index] = leadership_data[index].to_dict()
    return jsonify(leadership_data)


@app.route("/api/about-us/management")
def management_api():
    management_data = Leadership.query.filter_by(is_management=True).all()
    for index in range(len(management_data)):
        management_data[index] = management_data[index].to_dict()
    return jsonify(management_data)


@app.route("/api/about-us/leadership/<id>")
def leadership_name(id):
    leader = Leadership.query.filter_by(id=id).first_or_404()
    leader = leader.to_dict()
    return jsonify(leader)


@app.route("/api/about-us/partners")
def partners_api():
    partners_data = Partner.query.all()
    for index in range(len(partners_data)):
        partners_data[index] = partners_data[index].to_dict()
    return jsonify(partners_data)


@app.route("/api/news/latest-news")
def latest_news_api():
    if request.args.get("limit") == "4":
        latest_news = LatestNews.query.limit(4).all()
    else:
        latest_news = LatestNews.query.all()
    for index in range(len(latest_news)):
        latest_news[index] = latest_news[index].to_dict()
    return jsonify(latest_news)


@app.route("/api/news/industry-updates")
def industry_updates_api():
    if request.args.get("limit") == "4":
        industry_updates = IndustryUpdates.query.limit(4).all()
    else:
        industry_updates = IndustryUpdates.query.all()
    for index in range(len(industry_updates)):
        industry_updates[index] = industry_updates[index].to_dict()
    return jsonify(industry_updates)


@app.route("/api/events/")
def events_api():
    if request.args.get("upcoming-events") == "true":
        events = Events.query.filter_by(upcoming_event=True).all()
    else:
        events = Events.query.filter_by(upcoming_event=False).all()
    for index in range(len(events)):
        events[index] = events[index].to_dict()
    return jsonify(events)


@app.route("/api/events/gallery")
def events_gallery_api():
    events_gallery = (
        Events.query.with_entities(Events.id, Events.event_title, Events.event_image)
        .filter_by(upcoming_event=False)
        .all()
    )
    gallery = []
    for index in range(len(events_gallery)):
        gallery.append(
            {
                "id": events_gallery[index][0],
                "event_title": events_gallery[index][1],
                "images": [events_gallery[index][2]],
            }
        )
    return jsonify(gallery)
