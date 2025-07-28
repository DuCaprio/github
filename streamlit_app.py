import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title='SMART QUIZ',
    page_icon='🎯',
    layout='centered'
)
st.markdown("# 🎯<span style = 'color:Green;'>SMART QUIZ</span>", unsafe_allow_html=True)
st.write("**STREAMLIT**의 퀴즈를 풀어보세요❗️")

quiz_questions = [
    {
        "type": "radio",
        "question": "다음 중 Streamlit에서 제목을 표시하는 함수는?",
        "options": ["st.title", "st.header", "st.subheader", "st.write"],
        "correct": 0,
        "explanation": "st.title()은 가장 큰 제목을 표시하는 함수입니다."
    },
    {
        "type": "text",
        "question": "Streamlit에서 텍스트를 입력받는 위젯은? (st.text_input에서 st. 제외하고 입력)",
        "correct": ["text_input"],
        "explanation": "st.text_input은 사용자로부터 텍스트를 입력받는 위젯입니다."
    },
    {
        "type": "slider",
        "question": "Streamlit 앱을 실행할 때 기본 포트 번호는?",
        "min_val": 8000,
        "max_val": 9000,
        "correct": 8501,
        "tolerance": 10,
        "explanation": "Streamlit 앱의 기본 포트는 8501번입니다."
    },
    {
        "type": "number",
        "question": "st.columns(3)을 사용하면 몇 개의 열이 생성되나요?",
        "correct": 3,
        "explanation": "st.columns(3)은 3개의 열을 생성합니다."
    },
    {
        "type": "selectbox",
        "question": "다음 중 Streamlit의 버튼 요소가 아닌 것은?",
        "options": ["st.button", "st.download_button", "st.slider", "st.form_submit_button"],
        "correct": 2,
        "explanation": "st.slider는 슬라이더 위젯이며 버튼 요소가 아닙니다."
    }
]

# 상태 변수 초기화
if 'quiz_started' not in st.session_state:
    st.session_state['quiz_started'] = False
if 'answer_submitted' not in st.session_state:
    st.session_state['answer_submitted'] = False 
if 'show_result' not in st.session_state:
    st.session_state['show_result'] = False
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False 
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'show_result_page' not in st.session_state:
    st.session_state['show_result_page'] = False
if 'is_correct' not in st.session_state:
    st.session_state['is_correct'] = False

def check_answer(question, user_answer):
    if question['type'] in ['radio', 'selectbox', 'number']:
        return user_answer == question['correct']
    elif question['type'] == 'text':
        return str(user_answer).lower().strip() in [ans.lower() for ans in question['correct']]
    elif question['type'] == 'slider':
        return abs(user_answer - question['correct']) <= question['tolerance']
    return False

# 퀴즈 시작 전
if not st.session_state['quiz_started']:
    st.header("📚퀴즈 소개")
    st.markdown("""
        - **총 문제 수**: 5문제
        - **문제 유형**: 객관식/주관식/슬라이더/숫자형
        - **제한 시간**: 없음
        - **채점 방식**: 즉시 피드백 
    """)
    st.info("⬇️ **아래 버튼**을 클릭해서 퀴즈를 시작하세요.")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("START🏃‍♂️", type='primary'):
            st.session_state['quiz_started'] = True
            st.session_state['answer_submitted'] = False
            st.session_state['show_result'] = False
            st.session_state['quiz_finished'] = False
            st.session_state['current_question'] = 0
            st.session_state['answers'] = []
            st.session_state['score'] = 0
            st.session_state['show_result_page'] = False
            st.session_state['is_correct'] = False
            st.rerun()
    st.divider()
    st.subheader("👀문제 미리보기")
    for i, q in enumerate(quiz_questions):
        st.write(f"**문제{i+1}**: {q['question']} ({q['type']} 유형)")

# 퀴즈 진행
elif st.session_state['quiz_started'] and not st.session_state['quiz_finished']:
    current_quiz = st.session_state['current_question']
    questions = quiz_questions[current_quiz]
    progress_ratio = (current_quiz) / len(quiz_questions)
    st.progress(progress_ratio)
    st.write(f"현재 진행률: **{int(progress_ratio*100)}**%입니다.")
    st.subheader(f"**문제{current_quiz+1}**")
    st.write(questions['question'])

    if not st.session_state['answer_submitted']:
        user_answer = None
        if questions['type'] == 'radio':
            user_answer = st.radio("정답을 선택하세요",
                options=list(range(len(questions['options']))),
                format_func=lambda x: questions['options'][x],
                key=f"radio_{current_quiz}")
        elif questions['type'] == 'text':
            user_answer = st.text_input("정답을 입력하세요", placeholder='정답 입력칸').strip().lower()
        elif questions['type'] == 'slider':
            user_answer = st.slider("슬라이더를 조정하세요",
                max_value=questions['max_val'],
                min_value=questions['min_val'],
                value=((questions['min_val']+questions['max_val'])//2))
        elif questions['type'] == 'number':
            user_answer = st.number_input("숫자를 입력하세요", step=1)
        elif questions['type'] == 'selectbox':
            user_answer = st.selectbox("정답을 선택하세요",
                options=list(range(len(questions['options']))),
                format_func=lambda x: questions['options'][x],
                key=f"selectbox_{current_quiz}")
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("답안 제출", type='primary'):
                is_correct = check_answer(questions, user_answer)
                idx = st.session_state['current_question']
                # 답변이 이미 있으면 업데이트, 아니면 append
                if len(st.session_state['answers']) > idx:
                    # 이미 답이 있으면 오직 덮어쓰기 (점수 변화 없음)
                    st.session_state['answers'][idx] = {
                        'question': questions['question'],
                        'user_answer': user_answer,
                        'correct_answer': questions['correct'],
                        'is_correct': is_correct,
                        'explanation': questions['explanation']
                    }
                else:
                    st.session_state['answers'].append({
                        'question': questions['question'],
                        'user_answer': user_answer,
                        'correct_answer': questions['correct'],
                        'is_correct': is_correct,
                        'explanation': questions['explanation']
                    })
                    if is_correct:
                        st.session_state['score'] += 1
                st.session_state['is_correct'] = is_correct
                st.session_state['answer_submitted'] = True
                st.session_state['show_result'] = True
                st.rerun()
    else:
        if st.session_state['show_result']:
            if st.session_state['is_correct']:
                st.success("정답입니다🎊")
                st.info(questions['explanation'])
            else:
                st.error("오답입니다☠️")
                st.info(questions['explanation'])

        col1, col2, col3 = st.columns(3)
        with col2:
            if st.session_state['is_correct']:
                if current_quiz == len(quiz_questions)-1:
                    if st.button("결과 보기", type='primary'):
                        st.session_state['quiz_finished'] = True
                        st.session_state['show_result_page'] = True
                        st.rerun()
                else:
                    if st.button("NEXT", type='primary'):
                        st.session_state['current_question'] += 1
                        st.session_state['answer_submitted'] = False
                        st.session_state['show_result'] = False
                        st.session_state['is_correct'] = False
                        st.rerun()
            else:
                if st.button("AGAIN🏃‍♂️", type='primary'):
                    st.session_state['answer_submitted'] = False
                    st.session_state['show_result'] = False
                    st.session_state['is_correct'] = False
                    st.rerun()

# 결과 페이지
elif st.session_state['quiz_finished'] or st.session_state['show_result_page']:
    st.header("🎊 퀴즈 완료!")

    total_questions = len(quiz_questions)
    score_percentage = (st.session_state['score'] / total_questions) * 100

    def display_stat(title, value):
        st.markdown(f"""
            <div style="
                padding: 1rem; 
                background-color: var(--stat-bg, #f0f2f6); 
                border: 1px solid var(--stat-border, transparent);
                border-radius: 10px; 
                text-align: center;
                box-shadow: var(--stat-shadow, 0 1px 3px rgba(0,0,0,0.1));
            ">
                <div style="
                    font-size: 18px; 
                    font-weight: bold; 
                    color: var(--title-color, #262730);
                    margin-bottom: 0.5rem;
                ">{title}</div>
                <div style="
                    font-size: 32px; 
                    font-weight: bold; 
                    color: var(--text-color, #262730);
                ">{value}</div>
            </div>
            <style>
                :root {{
                    --stat-bg: #f0f2f6;
                    --stat-border: transparent;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    --title-color: #262730;
                    --text-color: #262730;
                }}
                @media (prefers-color-scheme: dark) {{
                    :root {{
                        --stat-bg: #2b2b35;
                        --stat-border: #404040;
                        --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                        --title-color: #fafafa;
                        --text-color: #fafafa;
                    }}
                }}
                [data-theme="dark"] {{
                    --stat-bg: #2b2b35;
                    --stat-border: #404040;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    --title-color: #fafafa;
                    --text-color: #fafafa;
                }}
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        display_stat("총 문제 수", total_questions)
    with col2:
        display_stat("맞힌 문제", st.session_state['score'])
    with col3:
        display_stat("정답률", f"{score_percentage:.1f}%")

    # 성취도에 따른 메시지
    if score_percentage == 100:
        st.success("🏆 완벽합니다! 모든 문제를 맞히셨네요!")
    elif score_percentage >= 80:
        st.success("🌟 훌륭해요! 대부분의 문제를 맞히셨습니다!")
    elif score_percentage >= 60:
        st.info("👍 괜찮아요! 조금 더 공부하면 완벽할 거예요!")
    else:
        st.error("💪 다시 도전해보세요! 더 좋은 결과가 있을 거예요!")

    st.divider()

    st.subheader("📊 상세 결과")
    for i, answer in enumerate(st.session_state['answers']):
        with st.expander(f"문제 {i+1}: {'✅' if answer['is_correct'] else '❌'}"):
            st.write(f"**문제**: {answer['question']}")
            if isinstance(answer['user_answer'], int) and 'options' in quiz_questions[i]:
                st.write(f"**내 답**: {quiz_questions[i]['options'][answer['user_answer']]}")
                st.write(f"**정답**: {quiz_questions[i]['options'][answer['correct_answer']]}")
            else:
                st.write(f"**내 답**: {answer['user_answer']}")
                if isinstance(answer['correct_answer'], list):
                    st.write(f"**정답**: {', '.join(str(x) for x in answer['correct_answer'])}")
                else:
                    st.write(f"**정답**: {answer['correct_answer']}")
            st.write(f"**해설**: {answer['explanation']}")

    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("**퀴즈 종료**", type="primary"):
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['answers'] = []
            st.session_state['quiz_started'] = False
            st.session_state['quiz_finished'] = False
            st.session_state['answer_submitted'] = False
            st.session_state['show_result'] = False
            st.session_state['is_correct'] = False
            st.session_state['show_result_page'] = False
            st.rerun()

