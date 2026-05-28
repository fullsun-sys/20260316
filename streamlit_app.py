import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from fractions import Fraction
import math

# Set the page configuration
st.set_page_config(
    page_title='삼각함수 기초 학습 도구',
    page_icon='📐',
    layout='wide'
)

st.title('📐 삼각비로 배우는 삼각함수')
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


def format_fraction(value):
    if value is None:
        return '정의되지 않음'
    if abs(value) < 1e-8:
        return '0'
    fraction = Fraction(value).limit_denominator(100)
    if abs(float(fraction) - value) < 1e-6:
        if fraction.denominator == 1:
            return str(fraction.numerator)
        return f"{fraction.numerator}/{fraction.denominator}"
    return f"{value:.2f}"

def format_ratio_string(numerator, denominator, numerator_display, denominator_display):
    if abs(denominator) < 1e-8:
        return '정의되지 않음'
    ratio = numerator / denominator
    fraction = Fraction(ratio).limit_denominator(100)
    if abs(float(fraction) - ratio) < 1e-6:
        if fraction.denominator == 1:
            return str(fraction.numerator)
        return f"{fraction.numerator}/{fraction.denominator}"
    return f"{numerator_display}/{denominator_display}"

# 사용자 입력: 좌표
st.markdown('## 입력 값')
col_input1, col_input2 = st.columns(2)
with col_input1:
    x_input = st.number_input('x 좌표 입력', value=1.0, step=0.1, format='%.4f')
with col_input2:
    y_input = st.number_input('y 좌표 입력', value=0.5, step=0.1, format='%.4f')

st.markdown('입력한 좌표에 대해 원점이 (0,0)인 원을 그리고, r = √(x² + y²)로 계산된 반지름과 함께 삼각함수 값을 표시합니다.')
st.markdown('---')

radius = np.hypot(x_input, y_input)
if radius > 1e-8:
    theta_rad = np.arctan2(y_input, x_input)
    if theta_rad < 0:
        theta_rad += 2 * np.pi
    theta_deg = np.degrees(theta_rad)
    angle_pi_display = format_angle_as_pi(theta_rad)
    angle_ascii_display = angle_pi_display.replace('π', 'pi').replace('θ', 'theta')
else:
    theta_rad = 0.0
    theta_deg = 0.0
    angle_pi_display = '정의되지 않음'
    angle_ascii_display = 'undefined'

# 삼각함수 값 계산
if radius > 1e-8:
    sin_val = y_input / radius
    cos_val = x_input / radius
else:
    sin_val = 0.0
    cos_val = 0.0

if abs(x_input) > 1e-8:
    tan_val = y_input / x_input
else:
    tan_val = None

# 점의 좌표
x_point = x_input
y_point = y_input
x_display = f"{x_input:.2f}"
y_display = f"{y_input:.2f}"
r_display = f"{radius:.2f}"

# 레이아웃: 왼쪽에 원, 오른쪽에 값
col1, col2 = st.columns([2, 1])

with col1:
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    
    # 축 설정
    axis_limit = max(1.5, abs(x_point), abs(y_point), radius) * 1.2
    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.8)
    ax.axvline(x=0, color='k', linewidth=0.8)
    ax.grid(True, alpha=0.3)
    
    # 원 그리기
    circle = plt.Circle((0, 0), radius, color='blue', fill=False, linewidth=2)
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
    # 직각삼각형의 변에 값을 라벨로 추가 (밑변과 높이 옆에 배치, 삼각형과 겹치지 않게)
    offset = axis_limit * 0.06
    # 밑변(x) 레이블: 밑변 중앙, y 위치는 삼각형과 겹치지 않게 아래/위로 약간 이동
    if y_point >= 0:
        base_y = -offset
        base_va = 'top'
    else:
        base_y = offset
        base_va = 'bottom'
    ax.text(x_point / 2, base_y, f'x = {x_display}',
            fontsize=10, ha='center', va=base_va, color='orange', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

    # 높이(y) 레이블: 높이 중앙, x 위치는 삼각형과 겹치지 않게 좌/우로 약간 이동
    if x_point >= 0:
        side_x = x_point + offset
        side_ha = 'left'
    else:
        side_x = x_point - offset
        side_ha = 'right'
    ax.text(side_x, y_point / 2, f'y = {y_display}',
            fontsize=10, ha=side_ha, va='center', color='green', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))
    
    # 각도 호 그리기 (0도에서 현재 각도까지)
    arc_radius = 0.3
    angle_arc = Arc((0, 0), 2 * arc_radius, 2 * arc_radius, 
                    angle=0, theta1=0, theta2=np.degrees(theta_rad), 
                    color='purple', linewidth=2)
    ax.add_patch(angle_arc)
    
    # 각도 텍스트 추가 (삼각형과 겹치지 않게 바깥쪽으로 배치)
    text_radius = 0.8
    text_angle = theta_rad / 2
    tx = text_radius * np.cos(text_angle)
    ty = text_radius * np.sin(text_angle)
    # 사분면 방향으로 바깥쪽 오프셋 적용
    offs = axis_limit * 0.1
    sign_x = np.sign(np.cos(text_angle)) if np.cos(text_angle) != 0 else 1.0
    sign_y = np.sign(np.sin(text_angle)) if np.sin(text_angle) != 0 else 1.0
    label_x = tx + offs * sign_x
    label_y = ty + offs * sign_y
    ha = 'left' if sign_x >= 0 else 'right'
    va = 'bottom' if sign_y >= 0 else 'top'
    ax.text(label_x, label_y,
            f'theta = {angle_ascii_display}\n({theta_deg:.2f} degrees)',
            fontsize=10, color='purple', weight='bold', ha=ha, va=va,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))
    
    # 축 레이블
    ax.set_xlabel('x', fontsize=14, weight='bold')
    ax.set_ylabel('y', fontsize=14, weight='bold')
    # 축 레이블 위치를 그래프 오른쪽( x )과 위쪽( y )에 시각적으로 표시
    ax.text(axis_limit * 0.98, 0.0, 'x', fontsize=11, weight='bold', ha='left', va='center')
    ax.text(0.0, axis_limit * 0.98, 'y', fontsize=11, weight='bold', ha='center', va='bottom')

    st.pyplot(fig, use_container_width=True)
    plt.close()

with col2:
    st.markdown('### 삼각함수 값')
    
    # 현재 각도 정보
    st.markdown(f'#### 각도: {angle_pi_display}')
    if radius > 1e-8:
        st.markdown(f'({theta_deg:.2f}° = {theta_rad:.2f} rad)')
    else:
        st.markdown('(원점 입력 시 각도는 정의되지 않습니다)')
    st.markdown('---')
    
    # 직각삼각형 정보
    st.markdown('### 📐 직각삼각형 정보')
    st.markdown(f'**x = {x_display}**')
    st.markdown(f'**y = {y_display}**')
    st.markdown(f'**r = {r_display}**')
    st.markdown('---')
    
    # Sin 값
    sin_display = f"{sin_val:.2f}"
    st.markdown('**sin θ = y/r**')
    st.metric(label='sin θ', value=sin_display, delta=f'{y_display}/{r_display}')
    
    st.markdown('---')
    
    # Cos 값
    cos_display = f"{cos_val:.2f}"
    st.markdown('**cos θ = x/r**')
    st.metric(label='cos θ', value=cos_display, delta=f'{x_display}/{r_display}')
    
    st.markdown('---')
    
    # Tan 값
    st.markdown('**tan θ = y/x**')
    if tan_val is None:
        st.metric(label='tan θ', value='정의되지 않음', delta='x = 0')
    else:
        tan_display = format_fraction(tan_val)
        st.metric(label='tan θ', value=tan_display, delta=f'{y_display}/{x_display}')

# 설명 섹션
st.markdown('---')
st.markdown('### 📚 학습 포인트')

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown('**sin θ (사인)**')
    st.markdown('- 높이 / 빗변')
    st.markdown('- 좌표평면에서 **y / r**')

with col_info2:
    st.markdown('**cos θ (코사인)**')
    st.markdown('- 밑변 / 빗변')
    st.markdown('- 좌표평면에서 **x / r**')

with col_info3:
    st.markdown('**tan θ (탄젠트)**')
    st.markdown('- 높이 / 밑변')
    st.markdown('- **y / x**')
    st.markdown('- 밑변(x)=0일 때 정의되지 않음')
