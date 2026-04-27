import streamlit as st
import pandas as pd

st.set_page_config(page_title="피키스 관리자", layout="wide")

st.markdown("""
    <style>
    .num-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 8px; margin-top: 15px; }
    .num-box { border: 1px solid #ddd; border-radius: 6px; padding: 10px 2px; text-align: center; font-size: 14px; }
    .taken { background-color: #ffd966; color: #000; font-weight: bold; border: 1px solid #f1c232; }
    .resting { background-color: #c9daf8; color: #000; font-weight: bold; border: 1px solid #a4c2f4; }
    .empty { background-color: #ffffff; color: #ced4da; }
    .num-label { font-size: 11px; margin-bottom: 4px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 기본 PC 화면용 제목 크기 */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        padding-bottom: 20px;
    }
    /* 모바일 화면(768px 이하)일 때 제목 크기 줄이기 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 22px !important; 
        }
    }
    </style>
    <div class="main-title">🏒 피키스</div>
    """, unsafe_allow_html=True)
menu = st.sidebar.radio("메뉴 이동", ["1. 회원 명단 및 등번호", "2. 조직도", "3. 임원진 R&R", "4. 입금 내역 관리"])

if menu == "1. 회원 명단 및 등번호":
    st.subheader("📋 1. 회원 정보 및 등번호 현황")
    
    active_url = "https://docs.google.com/spreadsheets/d/1oZAp291Ad1xZ6u5-XfdgY9_DH9Ox_GM27ltbEDY4UBc/export?format=csv&gid=1023493049"
    rest_url = "https://docs.google.com/spreadsheets/d/1oZAp291Ad1xZ6u5-XfdgY9_DH9Ox_GM27ltbEDY4UBc/export?format=csv&gid=1208100019"
    
    try:
        # 데이터 로드 (header=0으로 제목줄 인식)
        df_active = pd.read_csv(active_url)
        df_rest = pd.read_csv(rest_url)
        
        col_left, col_right = st.columns([4, 6])
        
        with col_left:
            st.markdown("#### 🏃 활동 회원 명단")
            st.dataframe(df_active, use_container_width=True, hide_index=True, height=400)
            st.write("") 
            st.markdown("#### 🛌 장기 휴식 회원 명단")
            st.dataframe(df_rest, use_container_width=True, hide_index=True, height=250)
            
        with col_right:
            st.markdown("#### 🎽 전체 배번(Back Number) 사용 현황")
            st.markdown("<small>🟡 활동 회원 | 🔵 장기 휴식 회원 | ⚪ 비어있음</small>", unsafe_allow_html=True)

            # 등번호 매핑 함수 (열 이름 대신 '순서'로 접근)
            def get_num_map_safe(df):
                if df.empty or len(df.columns) < 2: return {}
                
                # iloc를 사용해 첫 번째 열(0)을 등번호, 두 번째 열(1)을 성명으로 강제 지정
                # 혹시 열 순서가 [성명, 등번호]라면 아래 숫자를 (1, 0)으로 바꿔야 합니다.
                temp = df.iloc[:, [0, 1]].copy() 
                temp.columns = ['num', 'name']
                
                temp['num'] = pd.to_numeric(temp['num'], errors='coerce')
                temp = temp.dropna(subset=['num', 'name'])
                return dict(zip(temp['num'].astype(int), temp['name']))

            map_active = get_num_map_safe(df_active)
            map_rest = get_num_map_safe(df_rest)
            
            grid_html = '<div class="num-grid">'
            for i in range(1, 100):
                if i in map_active:
                    grid_html += f'<div class="num-box taken"><div class="num-label">{i}</div>{map_active[i]}</div>'
                elif i in map_rest:
                    grid_html += f'<div class="num-box resting"><div class="num-label">{i}</div>{map_rest[i]}</div>'
                else:
                    grid_html += f'<div class="num-box empty"><div class="num-label">{i}</div>-</div>'
            grid_html += "</div>"
            st.markdown(grid_html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
# ----------------------------------------------------
# 2. 조직도 페이지 (이름 직접 입력 방식)
# ----------------------------------------------------
elif menu == "2. 조직도":  # <- 메뉴 이름 정확히 일치시킴!
    st.subheader("🏢 임원 조직도")
    
    # 최상위: 피키스
    st.markdown('<div class="main-box"><h3>Fickeys (피키스)</h3></div>', unsafe_allow_html=True)
    
    # 4개 컬럼으로 나누기
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="group-title">👤 감독 / 코치</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>감독</b><br>최성우</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>코치</b><br>이한 / 김수영</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>총무</b><br>박윤조</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="group-title">🏠 피키스 (Div3)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>주장</b><br>장선호</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>부주장</b><br>강인후 / 김창현 / 김상진</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>총무</b><br>김상진</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="group-title">🏠 피키스 (Div 8)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>주장</b><br>박윤조</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>부주장</b><br>강유진 / 장동윤 / 김다열</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>총무</b><br>장동윤</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="group-title">🧊 큐키스</div>', unsafe_allow_html=True) # <- </Div8> 오타 수정
        st.markdown('<div class="sub-box"><b>주장</b><br>박윤조</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-box"><b>부주장</b><br>최소이 / 김하린 / 성수지</div>', unsafe_allow_html=True)
# 3. 임원진 R&R
# ----------------------------------------------------
elif menu == "3. 임원진 R&R":
    st.subheader("🤝 임원진 역할 및 책임 (R&R)")
    
    rr_url = "https://docs.google.com/spreadsheets/d/1oZAp291Ad1xZ6u5-XfdgY9_DH9Ox_GM27ltbEDY4UBc/export?format=csv&gid=1436566518"
    
    try:
        df_rr = pd.read_csv(rr_url)
        
        # 1. 'no.' 열의 '.0' 소수점 제거 로직
        # 'no.'라는 이름의 열이 있다면 실행
        if 'no.' in df_rr.columns:
            # 데이터를 정수형(Int64)으로 강제 변환하여 .0을 떼어내고, 다시 문자열로 바꿈
            df_rr['no.'] = pd.to_numeric(df_rr['no.'], errors='coerce').astype('Int64').astype(str)
            # 비어있던 칸이 '<NA>'로 표시되는 것을 깔끔한 빈칸으로 지워줌
            df_rr['no.'] = df_rr['no.'].replace('<NA>', '')
            
        # 2. 나머지 모든 빈칸(NaN)을 깔끔하게 빈칸으로 처리
        df_rr = df_rr.fillna("")
        
        # 3. 화면에 꽉 차는 예쁜 표로 출력
        st.dataframe(df_rr, use_container_width=True, hide_index=True, height=600)
                                
    except Exception as e:
        st.error(f"R&R 데이터를 불러올 수 없습니다. 상세 오류: {e}")
