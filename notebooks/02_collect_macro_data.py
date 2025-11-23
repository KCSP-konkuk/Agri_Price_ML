import pandas as pd
import yfinance as yf
import os

# ----------------------------------------------------------
# 1. 저장 경로 설정 (자동으로 폴더를 만들어 줍니다)
# ----------------------------------------------------------
# 현재 위치(notebooks)에서 상위(..) -> data -> raw -> macro 폴더로 이동
output_dir = './data/raw/macro'
os.makedirs(output_dir, exist_ok=True) # 폴더가 없으면 생성

# ----------------------------------------------------------
# 2. 데이터 다운로드 (Yahoo Finance 서버에서 가져옴)
# ----------------------------------------------------------
# CL=F : WTI 유가 (Crude Oil)
# KRW=X : 원/달러 환율
tickers = {
    'BZ=F': 'Brent_Oil',  # CL=F (WTI) 대신 BZ=F (브렌트유) 사용
    'KRW=X': 'Exchange_Rate'
}

print("⏳ 인터넷에서 데이터 다운로드 중...")

# 2015년부터 오늘까지의 데이터를 가져옵니다
try:
    df = yf.download(list(tickers.keys()), start='2015-01-01', progress=False)
    
    # 컬럼이 복잡하게(MultiIndex) 나오므로 'Close'(종가)만 선택
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Close']
    
    # 컬럼 이름 변경 (CL=F -> WTI_Oil 등)
    df = df.rename(columns=tickers)
    
    # 날짜 인덱스를 컬럼으로 꺼내기
    df = df.reset_index()
    
    # 날짜 형식 정리 (YYYY-MM-DD)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    # 주말/공휴일 데이터 채우기 (직전 값으로 채움)
    df = df.ffill()

    # ----------------------------------------------------------
    # 3. 파일로 저장
    # ----------------------------------------------------------
    output_path = os.path.join(output_dir, 'oil_exchange.csv')
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"✅ 다운로드 성공!")
    print(f"📂 파일 저장 위치: {output_path}")
    print(df.head())

except Exception as e:
    print(f"❌ 다운로드 실패: {e}")
    print("인터넷 연결을 확인하거나, 라이브러리를 설치해주세요 (pip install yfinance)")