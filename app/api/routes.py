import os

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from app.auth.jwt_handler import (
    get_current_user
)

from fastapi import Depends

from app.models.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.auth.database import (
    create_user,
    get_user_by_username
)

from app.auth.security import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)

from app.admin.service import (
    get_admin_stats,
    get_admin_users,
    remove_user
)

from app.chat.service import (
    fetch_chat_history,
    fetch_user_chat_history,
    fetch_all_chat_history,
    fetch_most_active_users
)

from app.rag.document_manager import (
    get_document_summary,
    delete_document
)

from app.feedback.service import (
    get_all_feedback
)

from app.models.feedback import (
    FeedbackRequest
)

from app.feedback.database import (
    save_feedback
)

from app.models.query import (
    QueryRequest,
    QueryResponse
)

from app.models.upload import (
    UploadResponse
)

from app.rag.rag_pipeline import (
    RAGPipeline
)

from app.rag.hybrid_retriever import (
    HybridRetriever
)

from app.utils.pdf_processor import (
    extract_text_from_pdf
)

from app.rag.indexer import (
    index_document
)

router = APIRouter()

rag = RAGPipeline()

retriever = HybridRetriever()


@router.get("/")
def home():

    return {
        "message": "Enterprise RAG API Running"
    }


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.post(
    "/query",
    response_model=QueryResponse
)
def query_rag(
    request: QueryRequest,
    current_user: str = Depends(
        get_current_user
    )
):

    response = rag.ask(
        request.question,
        current_user,
        source_filter=request.source_filter
    )

    return QueryResponse(
        answer=response["answer"],
        sources=response["sources"],
        evaluation=response["evaluation"]
    )


@router.post("/debug-search")
def debug_search(
    request: QueryRequest
):

    results = retriever.search(
        request.question
    )

    return {
        "results": results[:5]
    }


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: str = Depends(
        get_current_user
    )
):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(
            content
        )

    text = extract_text_from_pdf(
        file_path
    )

    chunk_count = index_document(
        text,
        file.filename,
        current_user
    )

    return UploadResponse(
        filename=file.filename,
        chunks_created=chunk_count,
        message="Indexed successfully"
    )


@router.post("/feedback")
def submit_feedback(
    request: FeedbackRequest
):

    save_feedback(
        request.question,
        request.answer,
        request.rating
    )

    return {
        "message": "Feedback saved successfully"
    }


@router.get("/feedbacks")
def view_feedbacks():

    rows = get_all_feedback()

    feedbacks = []

    for row in rows:

        feedbacks.append(
            {
                "id": row[0],
                "question": row[1],
                "answer": row[2],
                "rating": row[3],
                "created_at": row[4]
            }
        )

    return {
        "feedbacks": feedbacks
    }


@router.get("/stats")
def get_stats():

    rows = get_all_feedback()

    thumbs_up = 0
    thumbs_down = 0

    for row in rows:

        if row[3] == "thumbs_up":
            thumbs_up += 1

        elif row[3] == "thumbs_down":
            thumbs_down += 1

    total_feedback = len(rows)

    helpful_percentage = 0

    if total_feedback > 0:

        helpful_percentage = round(
            (thumbs_up / total_feedback) * 100,
            2
        )

    return {
        "total_feedback": total_feedback,
        "thumbs_up": thumbs_up,
        "thumbs_down": thumbs_down,
        "helpful_percentage": helpful_percentage,
        "model": "llama3",
        "retrieval": "Hybrid",
        "vector_db": "Qdrant"
    }

@router.get("/test-stats")
def test_stats():

    return {
        "message": "stats route loaded"
    }

print("ROUTES FILE LOADED")

@router.get("/documents")
def list_documents(
    current_user: str = Depends(
        get_current_user
    )
):

    documents = get_document_summary(
        current_user
    )

    return {
        "documents": documents
    }


@router.delete("/documents/{filename}")
def remove_document(
    filename: str,
    current_user: str = Depends(
        get_current_user
    )
):

    deleted_chunks = delete_document(
        filename,
        current_user
    )

    return {
        "message": f"{filename} deleted successfully",
        "deleted_chunks": deleted_chunks
    }


@router.get("/chat-history")
def get_chat_history(
    current_user: str = Depends(
        get_current_user
    )
):

    chats = fetch_user_chat_history(
        current_user
    )

    return {
        "chats": chats
    }

@router.get("/admin/stats")
def admin_stats():

    return get_admin_stats()
@router.get("/admin/users")
def admin_users():

    return {
        "users": get_admin_users()
    }


@router.delete(
    "/admin/users/{username}"
)
def admin_delete_user(
    username: str
):

    deleted = remove_user(
        username
    )

    if not deleted:

        return {
            "message": "User not found"
        }

    return {
        "message": f"{username} deleted successfully"
    }


@router.get("/admin/chats")
def admin_chats():

    return {
        "chats": fetch_all_chat_history()
    }

@router.get("/admin/active-users")
def admin_active_users():

    return {
        "users": fetch_most_active_users()
    }

@router.post("/register")
def register_user(
    request: RegisterRequest
):

    password_hash = hash_password(
        request.password
    )

    success = create_user(
        request.username,
        password_hash
    )

    if not success:

        return {
            "message": "Username already exists"
        }

    return {
        "message": "User registered successfully"
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    request: LoginRequest
):

    user = get_user_by_username(
        request.username
    )

    if not user:

        return {
            "access_token": "",
            "token_type": "bearer"
        }

    stored_hash = user[2]

    if not verify_password(
        request.password,
        stored_hash
    ):

        return {
            "access_token": "",
            "token_type": "bearer"
        }

    token = create_access_token(
        request.username
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )

@router.get("/me")
def get_me(
    current_user: str = Depends(
        get_current_user
    )
):

    return {
        "username": current_user
    }

from app.auth.jwt_handler import verify_token

@router.post("/verify-token")
def verify_user_token(
    token: str
):

    return verify_token(token)
