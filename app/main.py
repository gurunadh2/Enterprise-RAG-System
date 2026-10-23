from fastapi import FastAPI

from app.api.routes import (
    router
)

from app.feedback.database import (
    initialize_database
)

from app.chat.database import (
    initialize_chat_database
)

from app.auth.database import (
    initialize_user_database
)

app = FastAPI(
    title="Enterprise RAG"
)

# Initialize databases

initialize_database()

initialize_chat_database()

initialize_user_database()

# Register routes

app.include_router(
    router
)

# Print loaded routes

from fastapi.routing import APIRoute

for route in app.routes:

    if isinstance(route, APIRoute):

        print(route.path)