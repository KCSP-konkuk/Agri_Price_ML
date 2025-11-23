import pandas as pd
import os

# 1. 파일 경로 설정 (폴더 구조에 맞게 수정됨)
# notebooks 폴더에서 한 단계 위(..)로 가서 data/raw 폴더 안을 찾습니다.
input_path = './data/raw/weather_raw.csv'
output_path = './data/processed/weather_wide.csv'

# 2. 파일 불러오기
try:
    df = pd.read_csv(input_path, encoding='cp949')
except FileNotFoundError:
    print(f"❌ 파일을 찾을 수 없습니다. 경로를 확인해주세요: {input_path}")
    # 만약 에러가 나면 절대 경로로 확인해보기 위해 현재 위치 출력
    print(f"현재 파이썬 실행 위치: {os.getcwd()}")
    raise

# 3. 필요한 컬럼 선택 및 이름 단순화
df = df.rename(columns={
    '평균기온(°C)': '평균기온',
    '최저기온(°C)': '최저기온',
    '최고기온(°C)': '최고기온',
    '일강수량(mm)': '강수량',
    '평균 상대습도(%)': '습도',
    '합계 일조시간(hr)': '일조시간'
})

# 4. 피벗(Pivot): 지역을 컬럼으로 올리기
df_pivot = df.pivot(index='일시', columns='지점명', 
                    values=['평균기온', '최저기온', '최고기온', '강수량', '습도', '일조시간'])

# 5. 컬럼 이름 정리 (예: 부산_평균기온)
new_columns = []
for col_name, city in df_pivot.columns:
    new_columns.append(f'{city}_{col_name}')
    
df_pivot.columns = new_columns

# 6. 인덱스 리셋 및 결측치 처리
df_pivot = df_pivot.reset_index()

# 강수량 결측치는 0으로 채움
rain_cols = [c for c in df_pivot.columns if '강수량' in c]
df_pivot[rain_cols] = df_pivot[rain_cols].fillna(0)

# 7. 결과 저장 (processed 폴더에 저장)
# 만약 processed 폴더가 없으면 생성
os.makedirs('../data/processed', exist_ok=True)

df_pivot.to_csv(output_path, index=False, encoding='utf-8-sig')

# 결과 확인
print(f"✅ 변환 완료! 저장 위치: {output_path}")
print("데이터 크기:", df_pivot.shape)
print(df_pivot.head())