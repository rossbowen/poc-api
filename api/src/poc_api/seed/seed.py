import poc_api.database as database


def seed_db():
    db = database.db
    try:
        db.parse("seed.trig")
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
