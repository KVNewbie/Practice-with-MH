from flask import Flask
# 두번째는 list를 보낼때 쓰는 모듈
from flask import render_template




# Flask 서버 자체가 app에 담겼습니다
# 즉 app이 플라스크 서버 그 자체라는 뜻
# 여기서 __name__은 __main__입니다(메인이라는 뜻)
app = Flask(__name__)


@app.route('/')
def home():
   return 'This is Home!'

@app.route('/index')
def signup():
    return render_template('index.html')
#branch 연습


# 0.0.0.0은 누구나 들어 올 수 있고
# port는 9000번
# 디버그 모드 작용
## 중요한 점은 절대 여기서 실행하지 말고 cmd에서 실행 할 것!!
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

