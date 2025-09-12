"""
완벽한 키움 자동매매 시스템 메인 실행 파일
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from library.kiwoom_api import quick_login
import time

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🚀 완벽한 키움 자동매매 시스템 v1.0")
    print("   GitHub THANOS-PROJECT 기반으로 완전히 새로 제작")
    print("=" * 60)
    
    # PyQt5 애플리케이션 생성
    app = QApplication(sys.argv)
    
    try:
        # 로그인 방식 선택
        print("\n📋 로그인 방식을 선택하세요:")
        print("1. 수동 로그인 (팝업창 직접 입력)")
        print("2. 자동 로그인 (ID/PW 자동 입력)")
        
        choice = input("\n선택 (1 또는 2): ").strip()
        
        kiwoom = None
        
        if choice == "2":
            print("\n🤖 자동 로그인 선택")
            user_id = input("사용자 ID: ").strip()
            password = input("비밀번호: ").strip()
            
            if user_id and password:
                kiwoom = quick_login(user_id, password)
            else:
                print("❌ ID 또는 비밀번호가 입력되지 않았습니다")
                return
        else:
            print("\n📱 수동 로그인 선택")
            kiwoom = quick_login()
        
        if not kiwoom:
            print("❌ 로그인 실패")
            return
        
        print("\n" + "=" * 60)
        print("🎉 로그인 성공! 자동매매 시스템 시작")
        print("=" * 60)
        
        # 기본 기능 테스트
        test_basic_functions(kiwoom)
        
        # 자동매매 전략 선택
        run_trading_strategy(kiwoom)
        
        # 메인 루프
        print("\n🔄 시스템이 실행 중입니다...")
        print("   종료하려면 Ctrl+C를 누르세요")
        
        try:
            app.exec_()
        except KeyboardInterrupt:
            print("\n👋 시스템 종료 중...")
            kiwoom.stop_real_data()
            
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        import traceback
        traceback.print_exc()

def test_basic_functions(kiwoom):
    """기본 기능 테스트"""
    print("\n📊 기본 기능 테스트 중...")
    
    # 1. 삼성전자 현재가 조회
    print("\n1️⃣ 삼성전자 현재가 조회 테스트")
    samsung_data = kiwoom.get_current_price("005930")
    
    if samsung_data:
        print(f"   ✅ {samsung_data['name']}: {samsung_data['price']:,}원 ({samsung_data['rate']:+.2f}%)")
    else:
        print("   ❌ 삼성전자 현재가 조회 실패")
    
    # 2. LG전자 현재가 조회
    print("\n2️⃣ LG전자 현재가 조회 테스트")
    lg_data = kiwoom.get_current_price("066570")
    
    if lg_data:
        print(f"   ✅ {lg_data['name']}: {lg_data['price']:,}원 ({lg_data['rate']:+.2f}%)")
    else:
        print("   ❌ LG전자 현재가 조회 실패")
    
    # 3. 실시간 데이터 테스트
    print("\n3️⃣ 실시간 데이터 구독 테스트")
    if kiwoom.start_real_data(["005930", "066570"]):
        print("   ✅ 실시간 데이터 구독 성공")
        print("   📡 삼성전자, LG전자 실시간 모니터링 시작")
        
        # 5초간 실시간 데이터 확인
        print("   ⏱️ 5초간 실시간 데이터 확인...")
        time.sleep(5)
        
    else:
        print("   ❌ 실시간 데이터 구독 실패")

def run_trading_strategy(kiwoom):
    """자동매매 전략 실행"""
    print("\n🎯 자동매매 전략을 선택하세요:")
    print("1. 20일 신고가 돌파 전략")
    print("2. 실시간 모니터링만")
    print("3. 건너뛰기")
    
    strategy_choice = input("\n전략 선택 (1, 2, 3): ").strip()
    
    if strategy_choice == "1":
        print("\n🚀 20일 신고가 돌파 전략 시작!")
        from strategy.breakout_strategy import BreakoutStrategy
        
        strategy = BreakoutStrategy(kiwoom)
        strategy.start()
        
    elif strategy_choice == "2":
        print("\n📡 실시간 모니터링 모드")
        monitoring_stocks = ["005930", "066570", "035420"]  # 삼성전자, SK하이닉스, NAVER
        
        print(f"   📋 모니터링 종목: {monitoring_stocks}")
        kiwoom.start_real_data(monitoring_stocks)
        
    else:
        print("\n⏭️ 전략 실행 건너뛰기")

if __name__ == "__main__":
    main()
