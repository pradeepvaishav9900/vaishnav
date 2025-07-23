# Lura Messenger - Streamlit App (Phase 1)
# Features: Signup/Login, Chat, Admin Dashboard

import streamlit as st
from datetime import datetime
import json
import os

# In-memory user store and message log
if "users" not in st.session_state:
    st.session_state.users = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

# Admin credentials (hardcoded for now)
ADMIN_EMAIL = "admin@lura.com"
ADMIN_PASSWORD = "admin123"

def save_to_file():
    with open("users.json", "w") as f:
        json.dump(st.session_state.users, f)
    with open("messages.json", "w") as f:
        json.dump(st.session_state.messages, f)

def load_from_file():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            st.session_state.users = json.load(f)
    if os.path.exists("messages.json"):
        with open("messages.json", "r") as f:
            st.session_state.messages = json.load(f)

# Load stored data
load_from_file()

# UI: Sidebar - Login/Signup
st.sidebar.title("Lura Messenger")
auth_mode = st.sidebar.radio("Choose Option", ["Login", "Signup"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if auth_mode == "Signup":
    name = st.sidebar.text_input("Name")
    if st.sidebar.button("Create Account"):
        if email in st.session_state.users:
            st.sidebar.warning("User already exists.")
        else:
            st.session_state.users[email] = {"name": name, "password": password}
            save_to_file()
            st.sidebar.success("Account created! Please login.")

elif auth_mode == "Login":
    if st.sidebar.button("Login"):
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state["user"] = "admin"
        elif email in st.session_state.users and st.session_state.users[email]["password"] == password:
            st.session_state["user"] = email
        else:
            st.sidebar.error("Invalid login credentials.")

# After login:
if "user" in st.session_state:
    if st.session_state.user == "admin":
        st.title("🔒 Admin Dashboard - Lura")
        st.subheader("All Registered Users")
        st.json(st.session_state.users)
        st.subheader("Chat Logs")
        st.json(st.session_state.messages)
    else:
        st.title("💬 Lura Messenger")
        user_email = st.session_state.user
        user_name = st.session_state.users[user_email]["name"]
        st.success(f"Logged in as: {user_name}")

        # Chat area
        receiver = st.selectbox("Send message to:", [u for u in st.session_state.users if u != user_email])
        msg = st.text_input("Type your message")
        if st.button("Send"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.messages.append({
                "from": user_email,
                "to": receiver,
                "message": msg,
                "time": timestamp
            })
            save_to_file()

        # Show conversation
        st.subheader("📨 Your Chats")
        for chat in st.session_state.messages:
            if (chat["from"] == user_email and chat["to"] == receiver) or \
               (chat["from"] == receiver and chat["to"] == user_email):
                st.text(f"[{chat['time']}] {chat['from']} ➤ {chat['message']}")
