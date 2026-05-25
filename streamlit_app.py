import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import math

# Set the page configuration
st.set_page_config(
    page_title='삼각함수 기초 학습 도구',
    page_icon='📐',
    layout='wide'
)

st.title('📐 단위원으로 배우는 삼각함수')
st.markdown('**고등학교 수학 - 삼각함수 기초**')
st.markdown('---')

# 표준 각도와 삼각함수 값 사전
standard_angles = [
    (0, '0'),
    (np.pi / 6, 'π/6'),
    (np.pi / 4, 'π/4'),
    (np.pi / 3, 'π/3'),
    (np.pi / 2, 'π/2'),
    (2 * np.pi / 3, '2π/3'),
    (3 * np.pi / 4, '3π/4'),
    (5 * np.pi / 6, '5π/6'),
    (np.pi, 'π'),
    (7 * np.pi / 6, '7π/6'),
    (5 * np.pi / 4, '5π/4'),
    (4 * np.pi / 3, '4π/3'),
    (3 * np.pi / 2, '3π/2'),
    (5 * np.pi / 3, '5π/3'),
    (7 * np.pi / 4, '7π/4'),
    (11 * np.pi / 6, '11π/6'),
    (2 * np.pi, '2π')
]

exact_trig_values = {
    '0': {'sin': '0', 'cos': '1', 'tan': '0', 'x': '1', 'y': '0'},
    'π/6': {'sin': '1/2', 'cos': '√3/2', 'tan': '1/√3', 'x': '√3/2', 'y': '1/2'},
    'π/4': {'sin': '√2/2', 'cos': '√2/2', 'tan': '1', 'x': '√2/2', 'y': '√2/2'},
    'π/3': {'sin': '√3/2', 'cos': '1/2', 'tan': '√3', 'x': '1/2', 'y': '√3/2'},
    'π/2': {'sin': '1', 'cos': '0', 'tan': '정의되지 않음', 'x': '0', 'y': '1'},
    '2π/3': {'sin': '√3/2', 'cos': '-1/2', 'tan': '-√3', 'x': '-1/2', 'y': '√3/2'},
    '3π/4': {'sin': '√2/2', 'cos': '-√2/2', 'tan': '-1', 'x': '-√2/2', 'y': '√2/2'},
    '5π/6': {'sin': '1/2', 'cos': '-√3/2', 'tan': '-1/√3', 'x': '-√3/2', 'y': '1/2'},
    'π': {'sin': '0', 'cos': '-1', 'tan': '0', 'x': '-1', 'y': '0'},
    '7π/6': {'sin': '-1/2', 'cos': '-√3/2', 'tan': '1/√3', 'x': '-√3/2', 'y': '-1/2'},
    '5π/4': {'sin': '-√2/2', 'cos': '-√2/2', 'tan': '1', 'x': '-√2/2', 'y': '-√2/2'},
    '4π/3': {'sin': '-√3/2', 'cos': '-1/2', 'tan': '√3', 'x': '-1/2', 'y': '-√3/2'},
    '3π/2': {'sin': '-1', 'cos': '0', 'tan': '정의되지 않음', 'x': '0', 'y': '-1'},
    '5π/3': {'sin': '-√3/2', 'cos': '1/2', 'tan': '-√3', 'x': '1/2', 'y': '-√3/2'},
    '7π/4': {'sin': '-√2/2', 'cos': '√2/2', 'tan': '-1', 'x': '√2/2', 'y': '-√2/2'},
    '11π/6': {'sin': '-1/2', 'cos': '√3/2', 'tan': '-1/√3', 'x': '√3/2', 'y': '-1/2'},
    '2π': {'sin': '0', 'cos': '1', 'tan': '0', 'x': '1', 'y': '0'}
}


def find_standard_angle(angle_rad):
    for rad, label in standard_angles:
        if abs(angle_rad - rad) < 0.02:
            return label
    return None


def format_angle_as_pi(angle_rad):
    label = find_standard_angle(angle_rad)
    if label is not None:
        return label
    multiple = angle_rad / np.pi
    return f"{multiple:.2f}π"


def format_trig_value(angle_rad, kind):
    label = find_standard_angle(angle_rad)
    if label is not None:
        return exact_trig_values[label][kind]
    if kind == 'tan' and abs(np.cos(angle_rad)) < 1e-6:
        return '정의되지 않음'
    value = np.sin(angle_rad) if kind == 'sin' else np.cos(angle_rad) if kind == 'cos' else np.tan(angle_rad)
    return f"{value:.4f}"


def format_coordinate(angle_rad, kind):
    label = find_standard_angle(angle_rad)
    if label is not None:
        return exact_trig_values[label][kind]
    value = np.cos(angle_rad) if kind == 'x' else np.sin(angle_rad)
    return f"{value:.4f}"

# 표준 각도 프리셋
angle_presets = [
    ('0', 0),
    ('π/6 (30°)', np.pi / 6),
    ('π/4 (45°)', np.pi / 4),
    ('π/3 (60°)', np.pi / 3),
    ('π/2 (90°)', np.pi / 2),
    ('2π/3 (120°)', 2 * np.pi / 3),
    ('3π/4 (135°)', 3 * np.pi / 4),
    ('5π/6 (150°)', 5 * np.pi / 6),
    ('π (180°)', np.pi),
    ('7π/6 (210°)', 7 * np.pi / 6),
    ('5π/4 (225°)', 5 * np.pi / 4),
    ('4π/3 (240°)', 4 * np.pi / 3),
    ('3π/2 (270°)', 3 * np.pi / 2),
    ('5π/3 (300°)', 5 * np.pi / 3),
    ('7π/4 (315°)', 7 * np.pi / 4),
    ('11π/6 (330°)', 11 * np.pi / 6),
    ('2π (360°)', 2 * np.pi)
]

preset_labels = [label for label, value in angle_presets]
selected_preset = st.selectbox('자주 쓰는 각도 선택', preset_labels, index=2)
selected_angle = dict(angle_presets)[selected_preset]

# 슬라이더 - 각도 선택 (0~2π)
theta_rad = st.slider(
    '각도 선택 (0~2π)',
    min_value=0.0,
    max_value=2 * np.pi,
    value=selected_angle,
    step=0.01,
    format='%.2f'
)

# 파이 형태로 표시
angle_pi_display = format_angle_as_pi(theta_rad)
st.markdown(f"### 선택된 각도: **{angle_pi_display}** ({np.degrees(theta_rad):.1f}°)")
st.markdown('---')

# 라디안을 도로 변환
theta_deg = np.degrees(theta_rad)

# 삼각함수 값 계산
sin_val = np.sin(theta_rad)
cos_val = np.cos(theta_rad)
tan_val = np.tan(theta_rad)
radius = 1

# 점의 좌표 (원 위의 점)
x_point = radius * cos_val
y_point = radius * sin_val
x_display = format_coordinate(theta_rad, 'x')
y_display = format_coordinate(theta_rad, 'y')

# 레이아웃: 왼쪽에 원, 오른쪽에 값
col1, col2 = st.columns([2, 1])

with col1:
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    
    # 축 설정
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.8)
    ax.axvline(x=0, color='k', linewidth=0.8)
    ax.grid(True, alpha=0.3)
    
    # 단위원 그리기
    circle = plt.Circle((0, 0), 1, color='blue', fill=False, linewidth=2)
    ax.add_patch(circle)
    
    # 원 위의 점 표시
    ax.plot(x_point, y_point, 'ro', markersize=10)
    ax.text(x_point + 0.05, y_point + 0.05, f'P ({x_display}, {y_display})',
            fontsize=10, color='red', weight='bold')
    
    # 원점에서 점으로 가는 직선 (반지름)
    ax.plot([0, x_point], [0, y_point], 'r-', linewidth=2)
    
    # 직각삼각형 표시
    ax.plot([x_point, x_point], [0, y_point], 'g--', linewidth=2)
    ax.plot([0, x_point], [y_point, y_point], 'orange', linestyle='--', linewidth=2)
    
    # 직각삼각형의 변에 값을 라벨로 추가
    ax.text(x_point / 2, y_point + 0.15, f'x = {x_display}', 
            fontsize=10, ha='center', color='orange', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    ax.text(x_point + 0.2, y_point / 2, f'y = {y_display}', 
            fontsize=10, ha='left', color='green', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    mid_x = x_point / 2 - 0.15
    mid_y = y_point / 2 + 0.15
    ax.text(mid_x, mid_y, f'r = {radius}', 
            fontsize=10, ha='center', color='red', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # 각도 호 그리기 (0도에서 현재 각도까지)
    arc_radius = 0.3
    angle_arc = Arc((0, 0), 2 * arc_radius, 2 * arc_radius, 
                    angle=0, theta1=0, theta2=np.degrees(theta_rad), 
                    color='purple', linewidth=2)
    ax.add_patch(angle_arc)
    
    # 각도 텍스트 추가
    text_radius = 0.5
    text_angle = theta_rad / 2
    ax.text(text_radius * np.cos(text_angle), text_radius * np.sin(text_angle),
            f'$\\theta = {angle_pi_display}$\n({theta_deg:.1f}°)', 
            fontsize=10, color='purple', weight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))
    
    # 축 레이블
    ax.set_xlabel(r'$\\cos\\theta$ (x)', fontsize=12, weight='bold')
    ax.set_ylabel(r'$\\sin\\theta$ (y)', fontsize=12, weight='bold')
    ax.set_title('Unit circle (radius = 1)', fontsize=14, weight='bold')
    
    # 좌표축 표시
    ax.text(1.2, -0.1, 'x (cos)', fontsize=11, weight='bold')
    ax.text(-0.15, 1.2, 'y (sin)', fontsize=11, weight='bold')
    
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col2:
    st.markdown('### 삼각함수 값')
    
    # 현재 각도 정보
    st.markdown(f'#### 각도: {angle_pi_display}')
    st.markdown(f'({theta_deg:.1f}° = {theta_rad:.3f} rad)')
    st.markdown('---')
    
    # 직각삼각형 정보
    x_display = format_coordinate(theta_rad, 'x')
    y_display = format_coordinate(theta_rad, 'y')
    st.markdown('### 📐 직각삼각형 정보')
    st.markdown(f'**x (가로) = {x_display} ({x_point:.4f})**')
    st.markdown(f'**y (세로) = {y_display} ({y_point:.4f})**')
    st.markdown(f'**r (빗변/반지름) = 1**')
    st.markdown('---')
    
    # Sin 값
    sin_display = format_trig_value(theta_rad, 'sin')
    st.markdown('**sin θ = y/r**')
    st.metric(label='sin θ', value=sin_display, delta=f'{y_display}/1')
    
    st.markdown('---')
    
    # Cos 값
    cos_display = format_trig_value(theta_rad, 'cos')
    st.markdown('**cos θ = x/r**')
    st.metric(label='cos θ', value=cos_display, delta=f'{x_display}/1')
    
    st.markdown('---')
    
    # Tan 값
    tan_display = format_trig_value(theta_rad, 'tan')
    st.markdown('**tan θ = y/x**')
    if tan_display == '정의되지 않음':
        st.metric(label='tan θ', value=tan_display, delta='x = 0')
    else:
        st.metric(label='tan θ', value=tan_display, delta=f'{y_display}/{x_display}')

# 설명 섹션
st.markdown('---')
st.markdown('### 📚 학습 포인트')

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown('**sin θ (사인)**')
    st.markdown('- 높이 / 빗변')
    st.markdown('- 단위원에서 **y 좌표**')
    st.markdown('- 범위: [-1, 1]')

with col_info2:
    st.markdown('**cos θ (코사인)**')
    st.markdown('- 빗변 / 밑변')
    st.markdown('- 단위원에서 **x 좌표**')
    st.markdown('- 범위: [-1, 1]')

with col_info3:
    st.markdown('**tan θ (탄젠트)**')
    st.markdown('- 높이 / 밑변')
    st.markdown('- **y/x** (sin/cos)')
    st.markdown('- cos θ = 0일 때 정의되지 않음')
