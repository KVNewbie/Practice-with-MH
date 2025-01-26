import yfinance as yf
import pandas as pd
from datetime import datetime

# 삼성전자 주식 심볼 (한국 주식은 .KS를 붙임)
symbol = "005930.KS"

# 데이터 시작일과 종료일 설정
start_date = "2024-01-01"
end_date = "2024-12-31"

# Yahoo Finance에서 데이터 가져오기
samsung_data = yf.download(symbol, start=start_date, end=end_date)

# 데이터 출력
print(samsung_data)

# CSV 파일로 저장 (선택사항)
samsung_data.to_csv("samsung_stock_data_2024.csv")
