from contextlib import asynccontextmanager
from uuid import UUID

import os
import shutil
import tempfile

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from src.db import Post, get_async_session, create_db_and_tables, User
from src.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from src.users import current_active_user, fastapi_users, auth_backend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Upload a file to ImageKit, then create a Post in the database.
    """
    temp_file_path = None
    file_handle = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        file_handle = open(temp_file_path, "rb")
        upload_result = imagekit.upload_file(
            file=file_handle,
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"],
            ),
        )

        if upload_result.response_metadata.http_status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Failed to upload file to ImageKit",
            )

        if file.content_type and file.content_type.startswith("video/"):
            file_type = "video"
        else:
            file_type = "image"

        post = Post(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type=file_type,
            file_name=upload_result.name,
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)

        return post

    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_handle:
            file_handle.close()
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    Return a feed of posts with basic user info and ownership flag.
    """

    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()

    result = await session.execute(select(User))
    users = result.scalars().all()
    user_dict = {u.id: u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
                if getattr(post, "created_at", None)
                else None,
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown"),
            }
        )

    return {"posts": posts_data}


@app.delete("/post/{post_id}")
async def delete_post(
    post_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """
    Delete a post by UUID if the current user is the owner.
    """

    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this post",
        )

    try:
        await session.delete(post)
        await session.commit()
        return {"detail": "Post deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
