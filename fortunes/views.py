from django.shortcuts import render
from .utils import get_star_info, get_zodiac_info, generate_fortune
from .models import FortuneHistory
from datetime import datetime
import random

def fortune_home(request):
    """
    사용자의 생년월일을 입력받아 동서양 융합 운세를 생성하고 
    그래프 점수 산출 및 DB에 기록하는 메인 뷰입니다.
    """
    result = None
    history = None
    birth_date_str = ""

    if request.method == "POST":
        birth_str = request.POST.get("birth_date")
        if birth_str:
            try:
                # 1. 입력받은 날짜 처리
                birth_date = datetime.strptime(birth_str, "%Y-%m-%d")
                birth_date_str = birth_str
                
                # 2. 별자리 및 띠 정보 추출
                star_name, star_icon = get_star_info(birth_date.month, birth_date.day)
                zodiac_name, zodiac_icon = get_zodiac_info(birth_date.year)
                
                # 3. 운세 본문 생성
                star_res = generate_fortune(star_name, birth_str, is_star=True)
                zodiac_res = generate_fortune(zodiac_name, birth_str, is_star=False)
                
                # 4. 그래프용 점수 산출 (변수명 통일)
                final_star_score = random.randint(75, 100)
                final_zodiac_score = random.randint(75, 100)
                
                # 5. DB(FortuneHistory 모델)에 저장
                # 필드명(좌측)은 models.py 정의와 같아야 하며, 값(우측)은 위에서 만든 변수명입니다.
                FortuneHistory.objects.create(
                    birth_date=birth_date,
                    star_name=star_name,
                    star_text=star_res['text'],
                    star_score=final_star_score, 
                    zodiac_name=zodiac_name,
                    zodiac_text=zodiac_res['text'],
                    zodiac_score=final_zodiac_score 
                )
                
                # 6. 화면에 보낼 데이터 구성
                result = {
                    "star_name": star_name,
                    "star_icon": star_icon,
                    "star_f": star_res,
                    "star_score": final_star_score,
                    "zodiac_name": zodiac_name,
                    "zodiac_icon": zodiac_icon,
                    "zodiac_f": zodiac_res,
                    "zodiac_score": final_zodiac_score,
                    "today": datetime.now().strftime("%Y년 %m월 %d일")
                }
                
                # 7. 해당 생일 사용자의 과거 기록 상위 5건 가져오기
                history = FortuneHistory.objects.filter(birth_date=birth_date)[:5]
                
            except ValueError:
                pass

    return render(request, "fortunes/index.html", {
        "result": result, 
        "history": history, 
        "birth_date": birth_date_str
    })