from app_api import create_app
from app_api.models import db, Role

app = create_app()

with app.app_context():
    roles = ['user', 'admin', 'editor']

    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.session.add(new_role)

    db.session.commit()
    print("Roles populated successfully.")
