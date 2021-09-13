from tortoise.contrib.fastapi import register_tortoise

def init_db(app) -> register_tortoise:
    
    r = register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={'models': ['app.users.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    return r
