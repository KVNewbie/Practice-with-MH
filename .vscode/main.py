# import yfinance as yf

# 삼성전자 주식 데이터 가져오기
# symbol = "005930.KS"
# end_date = "2024-12-31"

import pandas as pd

# 파일 경로
file_path = r'C:\Users\e2hgc\Documents\GitHub\Practice-with-MH\.vscode\samsung_stock_data_2024.csv'

# CSV 파일 읽기 및 데이터 정리
samsung_data = pd.read_csv(file_path)

# 2, 3행 삭제
samsung_data = samsung_data.drop([0, 1])

# 열 이름 정리
samsung_data = samsung_data.rename(columns={'Price': 'Date'})

# 데이터 타입 변환
samsung_data['Date'] = pd.to_datetime(samsung_data['Date'], errors='coerce')  # 'Date' 열 변환
numeric_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
for col in numeric_columns:
    samsung_data[col] = pd.to_numeric(samsung_data[col], errors='coerce')

# NaN 제거
samsung_data = samsung_data.dropna()

# Date를 인덱스로 설정
samsung_data = samsung_data.set_index('Date')

# 정리된 데이터 확인 (필요시 출력)
# print(samsung_data.head())

# 거래 내역을 출력하는 함수 정의
def print_trade_history(trade_history, data):
    print("\n거래 내역:")
    cumulative_profit = 0  # 누적 수익을 추적
    for trade in trade_history:
        cumulative_profit += trade[4]  # 각 거래의 수익을 더함
        if trade[0] == 'Buy':
            print(f"{trade[0]} - 날짜: {data.index[trade[1]].date()}, 수량: {trade[2]}, 가격: {trade[3]:,.0f}원")
        else:
            print(f"{trade[0]} - 날짜: {data.index[trade[1]].date()}, 수량: {trade[2]}, 가격: {trade[3]:,.0f}원, 수익: {trade[4]:,.0f}원, 누적 수익: {cumulative_profit:,.0f}원")

# 매매 로직 함수 수정 (trade_history에 누적 수익 추가)
def trading_logic(data):
    initial_balance = 100 * data.iloc[0]['Close']  # 초기 자산 (100주 기준)
    balance = initial_balance
    shares = 100
    entry_price = data.iloc[0]['Close']
    trades = []
    total_profit = 0

    for i in range(1, len(data)):
        current_price = data['Close'].iloc[i]

        if shares > 0:  # 주식을 보유 중일 때
            if current_price >= entry_price + 3000:  # 수익 실현
                sell_amount = shares * current_price
                profit = sell_amount - (shares * entry_price)
                total_profit += profit
                balance = sell_amount
                trades.append(('Sell', i, shares, current_price, profit))
                shares = 0
            elif current_price <= entry_price - 1000:  # 손실 매도
                sell_amount = shares * current_price
                profit = sell_amount - (shares * entry_price)
                total_profit += profit
                balance = sell_amount
                trades.append(('Sell', i, shares, current_price, profit))
                shares = 0
        else:  # 주식이 없는 상태일 때
            if i < len(data) - 1:  # 마지막 날 제외
                entry_price = data['Close'].iloc[i + 1]
                shares = int(balance / entry_price)
                balance -= shares * entry_price
                trades.append(('Buy', i + 1, shares, entry_price, 0))  # 매입 시 수익은 0

    # 마지막 날 보유 주식 정산
    if shares > 0:
        final_sell_amount = shares * data['Close'].iloc[-1]
        final_profit = final_sell_amount - (shares * entry_price)
        total_profit += final_profit
        balance = final_sell_amount
        trades.append(('Final Sell', len(data)-1, shares, data['Close'].iloc[-1], final_profit))

    return initial_balance, balance, total_profit, trades

# 매매 로직 실행
initial_balance, final_balance, total_profit, trade_history = trading_logic(samsung_data)

# 결과 출력
print(f"초기 자산: {initial_balance:,.0f}원")
print(f"최종 자산: {final_balance:,.0f}원")
print(f"총 수익: {total_profit:,.0f}원")
print(f"수익률: {(total_profit / initial_balance * 100):.2f}%")

# 거래 내역 출력
print_trade_history(trade_history, samsung_data)
