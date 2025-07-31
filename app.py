import streamlit as st
import openai

# OpenAI API 키 로딩
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(page_title="🏋️‍♂️ 개인 맞춤 운동 챗봇", page_icon="💪")

st.title("🏋️‍♀️ 개인 맞춤 운동 챗봇")
st.write("당신의 목표와 상황에 맞춘 운동 루틴을 추천해드립니다!")

# 사용자 기본 정보 입력
with st.sidebar:
    st.header("📝 나의 정보 입력")
    age = st.number_input("나이", min_value=10, max_value=100, value=30)
    gender = st.radio("성별", ["남성", "여성", "기타"])
    fitness_level = st.selectbox("운동 경험", ["초보자", "중급자", "고급자"])
    goal = st.selectbox("운동 목표", ["체중 감량", "근육 증가", "건강 유지", "유연성 향상"])

# 세션 상태로 대화 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""
당신은 운동 전문가입니다. 사용자의 나이, 성별, 운동 수준, 목표를 기반으로
개인 맞춤형 운동 루틴과 운동 팁을 대화 형식으로 제공합니다.

[사용자 정보]
- 나이: {age}세
- 성별: {gender}
- 운동 수준: {fitness_level}
- 목표: {goal}

정보를 기반으로 간단하고 실용적인 피트니스 조언을 제공합니다.
        """}
    ]

# 이전 메시지 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if user_prompt := st.chat_input("운동이나 식단에 대해 질문해보세요!"):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        with st.spinner("추천 중..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
