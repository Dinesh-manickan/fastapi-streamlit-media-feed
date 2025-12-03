# import streamlit as st
# import requests
# import base64
# import urllib.parse

# st.set_page_config(page_title="Simple Social", layout="wide")

# # Initialize session state
# if "token" not in st.session_state:
#     st.session_state.token = None
# if "user" not in st.session_state:
#     st.session_state.user = None


# def get_headers():
#     """Get authorization headers with token"""
#     if st.session_state.token:
#         return {"Authorization": f"Bearer {st.session_state.token}"}
#     return {}


# def login_page():
#     st.title("🚀 Welcome to Simple Social")

#     # Simple form with two buttons
#     email = st.text_input("Email:")
#     password = st.text_input("Password:", type="password")

#     if email and password:
#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("Login", type="primary", use_container_width=True):
#                 # Login using FastAPI Users JWT endpoint
#                 login_data = {"username": email, "password": password}
#                 response = requests.post(
#                     "http://localhost:8000/auth/jwt/login", data=login_data
#                 )

#                 if response.status_code == 200:
#                     token_data = response.json()
#                     st.session_state.token = token_data["access_token"]

#                     # Get user info
#                     user_response = requests.get(
#                         "http://localhost:8000/users/me", headers=get_headers()
#                     )
#                     if user_response.status_code == 200:
#                         st.session_state.user = user_response.json()
#                         st.rerun()
#                     else:
#                         st.error("Failed to get user info")
#                 else:
#                     st.error("Invalid email or password!")

#         with col2:
#             if st.button("Sign Up", type="secondary", use_container_width=True):
#                 # Register using FastAPI Users
#                 signup_data = {"email": email, "password": password}
#                 response = requests.post(
#                     "http://localhost:8000/auth/register", json=signup_data
#                 )

#                 if response.status_code == 201:
#                     st.success("Account created! Click Login now.")
#                 else:
#                     error_detail = response.json().get("detail", "Registration failed")
#                     st.error(f"Registration failed: {error_detail}")
#     else:
#         st.info("Enter your email and password above")


# def upload_page():
#     st.title("📸 Share Something")

#     uploaded_file = st.file_uploader(
#         "Choose media", type=["png", "jpg", "jpeg", "mp4", "avi", "mov", "mkv", "webm"]
#     )
#     caption = st.text_area("Caption:", placeholder="What's on your mind?")

#     if uploaded_file and st.button("Share", type="primary"):
#         with st.spinner("Uploading..."):
#             files = {
#                 "file": (
#                     uploaded_file.name,
#                     uploaded_file.getvalue(),
#                     uploaded_file.type,
#                 )
#             }
#             data = {"caption": caption}
#             response = requests.post(
#                 "http://localhost:8000/upload",
#                 files=files,
#                 data=data,
#                 headers=get_headers(),
#             )

#             if response.status_code == 200:
#                 st.success("Posted!")
#                 st.rerun()
#             else:
#                 st.error("Upload failed!")


# def encode_text_for_overlay(text):
#     """Encode text for ImageKit overlay - base64 then URL encode"""
#     if not text:
#         return ""
#     # Base64 encode the text
#     base64_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
#     # URL encode the result
#     return urllib.parse.quote(base64_text)


# def create_transformed_url(original_url, transformation_params, caption=None):
#     if caption:
#         encoded_caption = encode_text_for_overlay(caption)
#         # Add text overlay at bottom with semi-transparent background
#         text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
#         transformation_params = text_overlay

#     if not transformation_params:
#         return original_url

#     parts = original_url.split("/")

#     imagekit_id = parts[3]
#     file_path = "/".join(parts[4:])
#     base_url = "/".join(parts[:4])
#     return f"{base_url}/tr:{transformation_params}/{file_path}"


# def feed_page():
#     st.title("🏠 Feed")

#     response = requests.get("http://localhost:8000/feed", headers=get_headers())
#     if response.status_code == 200:
#         posts = response.json()["posts"]

#         if not posts:
#             st.info("No posts yet! Be the first to share something.")
#             return

#         for post in posts:
#             st.markdown("---")

#             # Header with user, date, and delete button (if owner)
#             col1, col2 = st.columns([4, 1])
#             with col1:
#                 st.markdown(f"**{post['email']}** • {post['created_at'][:10]}")
#             with col2:
#                 if post.get("is_owner", False):
#                     if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
#                         # Delete the post
#                         response = requests.delete(
#                             f"http://localhost:8000/posts/{post['id']}",
#                             headers=get_headers(),
#                         )
#                         if response.status_code == 200:
#                             st.success("Post deleted!")
#                             st.rerun()
#                         else:
#                             st.error("Failed to delete post!")

#             # Uniform media display with caption overlay
#             caption = post.get("caption", "")
#             if post["file_type"] == "image":
#                 uniform_url = create_transformed_url(post["url"], "", caption)
#                 st.image(uniform_url, width=300)
#             else:
#                 # For videos: specify only height to maintain aspect ratio + caption overlay
#                 uniform_video_url = create_transformed_url(
#                     post["url"], "w-400,h-200,cm-pad_resize,bg-blurred"
#                 )
#                 st.video(uniform_video_url, width=300)
#                 st.caption(caption)

#             st.markdown("")  # Space between posts
#     else:
#         st.error("Failed to load feed")


# # Main app logic
# if st.session_state.user is None:
#     login_page()
# else:
#     # Sidebar navigation
#     st.sidebar.title(f"👋 Hi {st.session_state.user['email']}!")

#     if st.sidebar.button("Logout"):
#         st.session_state.user = None
#         st.session_state.token = None
#         st.rerun()

#     st.sidebar.markdown("---")
#     page = st.sidebar.radio("Navigate:", ["🏠 Feed", "📸 Upload"])

#     if page == "🏠 Feed":
#         feed_page()
#     else:
#         upload_page()


import base64
import requests
import streamlit as st
from urllib.parse import urljoin
from typing import Optional

# =========================
# Config
# =========================

API_BASE_URL = "http://localhost:8000"
st.set_page_config(
    page_title="Media Feed Frontend",
    page_icon="📸",
    layout="wide",
)


# =========================
# Helpers
# =========================


def get_api_url(path: str) -> str:
    """Safely build full API URL from base + path."""
    return urljoin(API_BASE_URL, path)


def init_session_state():
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None


def get_auth_headers() -> dict:
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def safe_rerun():
    """
    Streamlit version-safe rerun helper.
    Uses st.rerun() if available, otherwise falls back to st.experimental_rerun().
    """
    try:
        # Newer Streamlit versions
        st.rerun()
    except AttributeError:
        # Older Streamlit versions
        st.experimental_rerun()


# =========================
# API calls
# =========================


def api_login(email: str, password: str) -> Optional[str]:
    """
    Log in via fastapi-users JWT.
    NOTE: some setups expect 'email' instead of 'username'.
    Change the key if your backend differs.
    """
    url = get_api_url("/auth/jwt/login")
    data = {
        "username": email,  # change to "email" if your backend expects that
        "password": password,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=data, headers=headers)

    if resp.status_code != 200:
        st.error(f"Login failed: {resp.status_code} - {resp.text}")
        return None

    try:
        token = resp.json().get("access_token")
    except Exception:
        st.error("Unexpected login response format.")
        return None

    if not token:
        st.error("No access_token received from backend.")
        return None

    return token


def api_fetch_feed():
    url = get_api_url("/feed")
    headers = get_auth_headers()
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        st.error(f"Failed to fetch feed: {resp.status_code} - {resp.text}")
        return []

    data = resp.json()
    return data.get("posts", [])


def api_upload_post(file_bytes, filename: str, content_type: str, caption: str):
    url = get_api_url("/upload")
    headers = get_auth_headers()

    files = {
        "file": (filename, file_bytes, content_type),
    }
    data = {
        "caption": caption,
    }

    resp = requests.post(url, headers=headers, files=files, data=data)

    if resp.status_code not in (200, 201):
        st.error(f"Upload failed: {resp.status_code} - {resp.text}")
        return None

    return resp.json()


def api_delete_post(post_id: str):
    url = get_api_url(f"/post/{post_id}")
    headers = get_auth_headers()
    resp = requests.delete(url, headers=headers)

    if resp.status_code != 200:
        st.error(f"Failed to delete: {resp.status_code} - {resp.text}")
        return False

    return True


# =========================
# UI Components
# =========================


def sidebar_auth():
    st.sidebar.title("Auth")

    if st.session_state.access_token:
        st.sidebar.success(f"Logged in as\n{st.session_state.user_email}")
        if st.sidebar.button("Logout"):
            st.session_state.access_token = None
            st.session_state.user_email = None
            safe_rerun()
        st.sidebar.markdown("---")
    else:
        st.sidebar.info("Please log in to use the app.")

        with st.sidebar.form("login_form"):
            email = st.text_input("Email", key="sidebar_login_email")
            password = st.text_input(
                "Password", type="password", key="sidebar_login_password"
            )
            submit = st.form_submit_button("Login")

        if submit:
            if not email or not password:
                st.sidebar.error("Email and password are required.")
            else:
                token = api_login(email, password)
                if token:
                    st.session_state.access_token = token
                    st.session_state.user_email = email
                    st.sidebar.success("Logged in successfully.")
                    safe_rerun()


def draw_header():
    st.markdown(
        """
        <h1 style="text-align: center; margin-bottom: 0;">
            📸 Media Feed Frontend
        </h1>
        <p style="text-align: center; color: #888; margin-top: 0;">
            FastAPI + Streamlit client for upload & feed
        </p>
        <hr style="margin-top: 0.5rem; margin-bottom: 1.5rem;">
        """,
        unsafe_allow_html=True,
    )


def upload_section():
    st.subheader("Upload a new post")

    uploaded_file = st.file_uploader(
        "Choose an image or video",
        type=["png", "jpg", "jpeg", "gif", "mp4", "mov", "avi", "webm"],
    )
    caption = st.text_area("Caption", max_chars=2200, placeholder="Say something...")

    if uploaded_file:
        # Read all bytes once
        file_bytes = uploaded_file.getvalue()

        # Preview using base64 + HTML
        mime_type = uploaded_file.type or "application/octet-stream"
        if mime_type.startswith("image/"):
            b64 = base64.b64encode(file_bytes).decode("utf-8")
            st.markdown(
                f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <img src="data:{mime_type};base64,{b64}"
                         style="max-width: 400px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.25);" />
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif mime_type.startswith("video/"):
            st.video(file_bytes)

        if st.button("Upload", type="primary", use_container_width=True):
            if not caption.strip():
                st.warning("Please add a caption.")
            else:
                if not st.session_state.access_token:
                    st.error("You must be logged in to upload.")
                    return

                res = api_upload_post(
                    file_bytes=file_bytes,
                    filename=uploaded_file.name,
                    content_type=mime_type,
                    caption=caption.strip(),
                )
                if res:
                    st.success("Upload successful!")
                    safe_rerun()


def feed_section():
    st.subheader("Feed")

    if not st.session_state.access_token:
        st.info("Log in to view your feed.")
        return

    posts = api_fetch_feed()
    if not posts:
        st.info("No posts yet. Upload something!")
        return

    for post in posts:
        with st.container():
            st.markdown(
                """
                <div style="
                    border-radius: 16px;
                    padding: 1rem 1.5rem;
                    margin-bottom: 1.2rem;
                    background: linear-gradient(135deg, #1f2933, #111827);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                    color: #f9fafb;
                ">
                """,
                unsafe_allow_html=True,
            )

            # Header row: email + created_at + delete
            cols = st.columns([5, 3, 1])
            with cols[0]:
                st.markdown(
                    f"**{post.get('email', 'Unknown user')}**",
                )
                st.caption(f"Post ID: {post.get('id')}")

            with cols[1]:
                created_at = post.get("created_at")
                if created_at:
                    st.markdown(
                        f"<p style='text-align: right; color: #9ca3af; font-size: 0.85rem;'>"
                        f"{created_at}</p>",
                        unsafe_allow_html=True,
                    )

            with cols[2]:
                if post.get("is_owner"):
                    if st.button(
                        "🗑️",
                        key=f"delete_{post['id']}",
                        help="Delete this post",
                    ):
                        success = api_delete_post(post["id"])
                        if success:
                            st.success("Post deleted.")
                            safe_rerun()

            st.markdown("<hr style='border-color: #374151;'>", unsafe_allow_html=True)

            # Caption
            caption = post.get("caption", "")
            if caption:
                st.markdown(
                    f"<p style='font-size: 0.95rem; margin-bottom: 0.75rem;'>{caption}</p>",
                    unsafe_allow_html=True,
                )

            # Media
            url = post.get("url")
            file_type = post.get("file_type", "image")

            if url:
                if file_type == "image":
                    st.image(url, use_container_width=True)
                elif file_type == "video":
                    st.video(url)
                else:
                    st.markdown(
                        f"<a href='{url}' target='_blank'>Open file</a>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No media URL available.")

            st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Main app
# =========================


def main():
    init_session_state()
    sidebar_auth()
    draw_header()

    if st.session_state.access_token:
        tab_feed, tab_upload = st.tabs(["📜 Feed", "⬆️ Upload"])
        with tab_feed:
            feed_section()
        with tab_upload:
            upload_section()
    else:
        st.info("Log in from the sidebar to start using the app.")


if __name__ == "__main__":
    main()
