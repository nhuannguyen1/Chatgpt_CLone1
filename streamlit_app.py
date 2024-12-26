import streamlit as st
from openai import OpenAI


with open("requirements.txt", "r", encoding="utf-8") as file:
    content_sys = file.read()

print(content_sys)


with open("sys_xchao.txt", "r", encoding="utf-8") as file:
    sys_xchao = file.read()
print(sys_xchao)


# Căn chỉnh tiêu đề vào giữa m
st.markdown(
    """
    <h1 style="text-align: center;">Xin Chào, Mình Là Trợ Lý Pyan</h1>
    """,
    unsafe_allow_html=True
)

# Lấy OpenAI API key từ `st.secrets`.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

system = st.secrets.get("system_train")

# Tạo OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Khởi tạo lời nhắn "system" để định hình hành vi mô hình.
INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content": content_sys,
}

# Khởi tạo lời nhắn ví dụ từ vai trò "assistant".
INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content":sys_xchao,
}

# Khởi tạo lời nhắn ví dụ từ vai trò "user".
INITIAL_USER_MESSAGE = {
    "role": "user",
    "content": (
        "Xin chào trợ lý Pyan! Tôi muốn tìm hiểu thêm về cách sử dụng dịch vụ của bạn. "
        "Bạn có thể giúp tôi được không?"
    ),
}

# Tạo một biến trạng thái session để lưu trữ các tin nhắn nếu chưa tồn tại.
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# Loại bỏ INITIAL_SYSTEM_MESSAGE khỏi giao diện hiển thị.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Tạo ô nhập liệu cho người dùng.
if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):

    # Lưu trữ và hiển thị tin nhắn của người dùng.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo phản hồi từ API OpenAI.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Hiển thị và lưu phản hồi của trợ lý.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
