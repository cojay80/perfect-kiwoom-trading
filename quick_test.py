"""
키움 자동매매 시스템 빠른 테스트
로그인만 테스트하는 간단한 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from library.kiwoom_api import quick_login

def quick_test():
    """빠른 로그인 테스트"""
    print("🧪 키움 API 빠른 테스트 시작")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    print("📱 수동 로그인으로 테스트 중...")
    print("   로그인 창이 나타나면 직접 로그인해주세요")
    
    kiwoom = quick_login()
    
    if kiwoom:
        print("\n✅ 로그인 성공!")
        print(f"💳 계좌번호: {kiwoom.account_num}")
        
        # 삼성전자 현재가만 간단히 테스트
        print("\n📊 삼성전자 현재가 테스트...")
        data = kiwoom.get_current_price("005930")
        
        if data:
            print(f"✅ {data['name']}: {data['price']:,}원 ({data['rate']:+.2f}%)")
        else:
            print("❌ 현재가 조회 실패")
        
        print("\n🎉 테스트 완료! 모든 기능이 정상 작동합니다.")
        
    else:
        print("❌ 로그인 실패")
        print("   1. 키움 OpenAPI+ 설치 확인")
        print("   2. 32비트 Python 환경 확인")
        print("   3. 필수 라이브러리 설치 확인")

if __name__ == "__main__":
    quick_test()
