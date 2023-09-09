import streamlit as st 
import random 
import json
import pandas as pd

def show_lottonum(obj, num):
    img = f'./static/assets/no_{num}.png'
    obj.image(img, width=64)
    
def show_plus(obj):
    img = f'./static/assets/plus.png'
    obj.image(img, width=64)

# 로또번호 여러 세트를 생성 함수
def generateLottoNumbers(set_count):
    lotto_sets = []
    for _ in range(set_count):
        lotto = generateSingleLottoSet()
        bonus = generateBonusNumber(lotto)
        lotto.append(bonus)
        lotto_sets.append(lotto)
    return lotto_sets

# 로또번호 한 세트 생성 함수
# 1~45 사이의 숫자 6개를 랜덤으로 뽑아서 정렬하여 리스트로 반환
# 번호의 중복은 없음
# 보너스 번호는 포함하지 않음
def generateSingleLottoSet():
    numbers = []
    while len(numbers) < 6:
        num = random.randint(1, 45)
        if num not in numbers:
            numbers.append(num) 
    numbers.sort()
    return numbers

# 로또번호 한 세트에 없는 보너스 번호 추가 함수
def generateBonusNumber(numbers):
    bonus = random.randint(1, 45)
    while bonus in numbers:
        bonus = random.randint(1, 45)
    return bonus

# lotto_pretty.json 분석
# 지난 기간 로또번호의 빈도수 분석하여 차트로 표시하는 함수
def analyzeAndDrawFrequencyChart():
    frequency = [0] * 45
    print(frequency)
    # load json file from lotto_pretty.json
    f = open('lotto_pretty.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    # print(data)
    for lotto_set in data:
        for i in range(6):
            numberkey = '번호' + str(i+1)
            number = lotto_set[numberkey]
            frequency[number-1] += 1
        bonusNumber = lotto_set['보너스번호']
        frequency[bonusNumber-1] += 1 
    print(frequency)
    
    # pandas dataframe으로 변환
    # df = pd.DataFrame(frequency)
    df = pd.DataFrame(frequency, columns=['빈도수'])
    df.index = df.index + 1
    print(df)
    return df



######################################
set_count = 4
lotto_sets = generateLottoNumbers(set_count)
df = analyzeAndDrawFrequencyChart()

######################################
# 화면 출력 부분
st.title("로또번호AI 생성기")
st.divider()

for l in lotto_sets:
    c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(8)
    show_lottonum(c1, l[0])
    show_lottonum(c2, l[1])
    show_lottonum(c3, l[2])
    show_lottonum(c4, l[3])
    show_lottonum(c5, l[4])
    show_lottonum(c6, l[5])
    show_plus(c7)
    show_lottonum(c8, l[6])
    st.empty()
st.divider()

st.title("로또번호 빈도수 분석")
st.bar_chart(df)
st.write("로또번호AI 생성기를 이용해 주셔서 감사합니다.")
