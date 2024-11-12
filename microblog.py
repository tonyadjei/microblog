from app import app, db
from app.models import (
    User,
    Post,
    OurImpact,
    AboutUsSection,
    MissionItems,
    ValuesItems,
    Leadership,
)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Post": Post,
        "OurImpact": OurImpact,
        "AboutUsSection": AboutUsSection,
        "MissionItems": MissionItems,
        "ValueItems": ValuesItems,
        "Leadership": Leadership,
    }
