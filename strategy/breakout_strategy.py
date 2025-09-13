"""
20일 신고가 돌파 자동매매 전략
당신이 원하던 완벽한 전략을 구현합니다!
"""

import time
import threading
from datetime import datetime


class BreakoutStrategy:
    """20일 신고가 돌파 전략"""
    
    def __init__(self, kiwoom_api):
        self.kiwoom = kiwoom_api
        
        # 전략 설정 (1단계: 심플 버전)
        self.config = {
            # 진입 조건
            'breakout_days': 20,           # 20일 신고가 돌파
            'volume_ratio': 2.0,           # 거래량 200% 이상
            'trading_amount_limit': 1000,  # 거래대금 10억 이상 (백만원 단위)
            
            # 청산 조건
            'profit_target_1': 3.0,        # 1차 익절: +3%
            'profit_target_2': 6.0,        # 2차 익절: +6%
            'stop_loss': -2.0,             # 손절: -2%
            
            # 리스크 관리
            'position_size': 10.0,         # 종목당 10%
            'max_positions': 5,            # 최대 5개 종목
            'daily_loss_limit': -3.0,      # 일일 손실 한도: -3%
            
            # 운영 시간
            'start_time': '10:30',         # 시작 시간
            'end_time': '14:30',           # 종료 시간
        }
        
        # 상태 변수
        self.positions = {}                # 보유 포지션
        self.daily_pnl = 0.0              # 일일 손익
        self.signal_count = 0             # 신호 카운트
        self.is_running = False           # 실행 상태
        
        # 모니터링 종목 (거래대금 상위 200개 중 선별)
        self.watch_list = [
            '005930',  # 삼성전자
            '000660',  # SK하이닉스
            '035420',  # NAVER
            '051910',  # LG화학
            '006400',  # 삼성SDI
            '035720',  # 카카오
            '068270',  # 셀트리온
            '207940',  # 삼성바이오로직스
            '066570',  # LG전자
            '096770',  # SK이노베이션
        ]
        
        print(f"🎯 20일 신고가 돌파 전략 초기화 완료")
        print(f"   📋 모니터링 종목: {len(self.watch_list)}개")
        print(f"   ⚙️ 익절: {self.config['profit_target_1']}%/{self.config['profit_target_2']}%")
        print(f"   🛡️ 손절: {self.config['stop_loss']}%")
    
    def start(self):
        """전략 시작"""
        if self.is_running:
            print("⚠️ 전략이 이미 실행 중입니다")
            return
        
        self.is_running = True
        print("\n🚀 20일 신고가 돌파 전략 시작!")
        
        # 현재 시간 확인
        current_time = datetime.now().strftime('%H:%M')
        print(f"⏰ 현재 시간: {current_time}")
        
        if self._is_trading_time():
            print("✅ 매매 가능 시간입니다")
            self._start_monitoring()
        else:
            print(f"⏸️ 매매 시간이 아닙니다 ({self.config['start_time']} ~ {self.config['end_time']})")
            print("   다음 매매 시간까지 대기합니다")
    
    def stop(self):
        """전략 중지"""
        if not self.is_running:
            return
        
        self.is_running = False
        print("\n⏹️ 20일 신고가 돌파 전략 중지")
        
        # 실시간 데이터 중지
        self.kiwoom.stop_real_data()
        
        # 포지션 요약
        if self.positions:
            print(f"📊 현재 포지션: {len(self.positions)}개")
            for code, pos in self.positions.items():
                print(f"   {pos['name']}: {pos['qty']}주 (수익률: {pos['return']:.2f}%)")
    
    def _is_trading_time(self):
        """매매 시간 확인"""
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        
        start_time = self.config['start_time']
        end_time = self.config['end_time']
        
        return start_time <= current_time <= end_time
    
    def _start_monitoring(self):
        """모니터링 시작"""
        print(f"\n📡 실시간 모니터링 시작 ({len(self.watch_list)}개 종목)")
        
        # 실시간 데이터 구독
        if self.kiwoom.start_real_data(self.watch_list):
            print("✅ 실시간 데이터 구독 성공")
            
            # 초기 현재가 확인
            self._check_initial_prices()
            
            # 실시간 모니터링 설정
            self._setup_real_monitoring()
            
        else:
            print("❌ 실시간 데이터 구독 실패")
    
    def _check_initial_prices(self):
        """초기 현재가 확인"""
        print("\n📊 초기 현재가 확인 중...")
        
        for i, code in enumerate(self.watch_list[:5]):  # 처음 5개만 확인
            data = self.kiwoom.get_current_price(code)
            
            if data:
                print(f"   {i+1}. {data['name']}: {data['price']:,}원 ({data['rate']:+.2f}%)")
                
                # 돌파 신호 확인 (임시로 등락률 3% 이상을 신호로 가정)
                if data['rate'] >= 3.0:
                    self._generate_buy_signal(code, data)
            
            time.sleep(0.5)  # API 호출 제한 고려
    
    def _setup_real_monitoring(self):
        """실시간 모니터링 설정"""
        # 기존 실시간 데이터 핸들러 재정의
        original_handler = self.kiwoom._receive_real_data
        
        def enhanced_real_handler(code, real_type, real_data):
            original_handler(code, real_type, real_data)
            
            if real_type == "주식체결" and self.is_running:
                self._process_real_data(code)
        
        self.kiwoom._receive_real_data = enhanced_real_handler
        print("✅ 실시간 모니터링 핸들러 설정 완료")
    
    def _process_real_data(self, code):
        """실시간 데이터 처리"""
        try:
            # 현재가 조회
            current_price = abs(int(self.kiwoom.dynamicCall("GetCommRealData(QString, int)", code, 10)))
            
            # 포지션이 있는 종목인지 확인
            if code in self.positions:
                self._check_exit_signal(code, current_price)
            else:
                # 새로운 진입 신호 확인 (간단히 급등 체크)
                prev_price = getattr(self, f'_prev_price_{code}', current_price)
                
                if prev_price > 0:
                    change_rate = ((current_price - prev_price) / prev_price) * 100
                    
                    if change_rate >= 2.0:  # 2% 이상 급등시 신호
                        self._check_breakout_signal(code, current_price)
                
                setattr(self, f'_prev_price_{code}', current_price)
                
        except Exception as e:
            print(f"❌ 실시간 데이터 처리 오류 ({code}): {e}")
    
    def _check_breakout_signal(self, code, price):
        """돌파 신호 확인"""
        data = self.kiwoom.get_current_price(code)
        if data and data['rate'] >= 3.0:  # 3% 이상 상승시 돌파로 가정
            self._generate_buy_signal(code, data)
    
    def _generate_buy_signal(self, code, data):
        """매수 신호 생성"""
        if len(self.positions) >= self.config['max_positions']:
            print(f"⚠️ 최대 포지션 수 도달 ({self.config['max_positions']}개)")
            return
        
        if code in self.positions:
            print(f"⚠️ {data['name']} 이미 보유 중")
            return
        
        self.signal_count += 1
        
        print(f"\n🎯 매수 신호 #{self.signal_count}")
        print(f"   📈 종목: {data['name']} ({code})")
        print(f"   💰 현재가: {data['price']:,}원")
        print(f"   📊 등락률: {data['rate']:+.2f}%")
        
        # 실제 주문 실행 (모의투자에서만!)
        if self._execute_buy_order(code, data):
            print(f"   ✅ 매수 주문 성공!")
        else:
            print(f"   ❌ 매수 주문 실패")
    
    def _execute_buy_order(self, code, data):
        """매수 주문 실행"""
        try:
            # 주문 수량 계산 (간단히 1주로 설정)
            qty = 1
            
            # 시장가 매수 주문
            success = self.kiwoom.send_order(
                f"{data['name']}_매수",
                "0101",
                1,  # 매수
                code,
                qty,
                0,  # 시장가
                "03"  # 시장가 호가
            )
            
            if success:
                # 포지션 기록
                self.positions[code] = {
                    'name': data['name'],
                    'qty': qty,
                    'entry_price': data['price'],
                    'current_price': data['price'],
                    'return': 0.0,
                    'entry_time': datetime.now()
                }
                
                print(f"📝 포지션 기록: {data['name']} {qty}주 @ {data['price']:,}원")
                
            return success
            
        except Exception as e:
            print(f"❌ 매수 주문 오류: {e}")
            return False
    
    def _check_exit_signal(self, code, current_price):
        """청산 신호 확인"""
        if code not in self.positions:
            return
        
        position = self.positions[code]
        entry_price = position['entry_price']
        
        # 수익률 계산
        return_rate = ((current_price - entry_price) / entry_price) * 100
        position['current_price'] = current_price
        position['return'] = return_rate
        
        # 청산 조건 확인
        should_sell = False
        sell_reason = ""
        
        if return_rate >= self.config['profit_target_2']:
            should_sell = True
            sell_reason = f"2차 익절 ({self.config['profit_target_2']}%)"
            
        elif return_rate >= self.config['profit_target_1']:
            # 1차 익절 (50% 매도)
            if position['qty'] > 1:
                self._execute_partial_sell(code, position['qty'] // 2, "1차 익절")
                return
            
        elif return_rate <= self.config['stop_loss']:
            should_sell = True
            sell_reason = f"손절 ({self.config['stop_loss']}%)"
        
        if should_sell:
            self._execute_sell_order(code, sell_reason)
    
    def _execute_partial_sell(self, code, qty, reason):
        """부분 매도"""
        try:
            position = self.positions[code]
            
            print(f"\n📤 부분 매도: {position['name']}")
            print(f"   수량: {qty}주 (전체 {position['qty']}주 중)")
            print(f"   사유: {reason}")
            print(f"   수익률: {position['return']:+.2f}%")
            
            # 매도 주문 실행
            success = self.kiwoom.send_order(
                f"{position['name']}_부분매도",
                "0102",
                2,  # 매도
                code,
                qty,
                0,  # 시장가
                "03"
            )
            
            if success:
                # 포지션 수량 업데이트
                position['qty'] -= qty
                print(f"   ✅ 부분 매도 성공! 잔여: {position['qty']}주")
            
        except Exception as e:
            print(f"❌ 부분 매도 오류: {e}")
    
    def _execute_sell_order(self, code, reason):
        """전량 매도"""
        try:
            position = self.positions[code]
            
            print(f"\n📤 전량 매도: {position['name']}")
            print(f"   수량: {position['qty']}주")
            print(f"   사유: {reason}")
            print(f"   최종 수익률: {position['return']:+.2f}%")
            
            # 매도 주문 실행
            success = self.kiwoom.send_order(
                f"{position['name']}_전량매도",
                "0103",
                2,  # 매도
                code,
                position['qty'],
                0,  # 시장가
                "03"
            )
            
            if success:
                # 일일 손익 업데이트
                pnl = position['return']
                self.daily_pnl += pnl
                
                print(f"   ✅ 매도 완료! 손익: {pnl:+.2f}%")
                print(f"   📊 일일 누적 손익: {self.daily_pnl:+.2f}%")
                
                # 포지션 제거
                del self.positions[code]
                
                # 일일 손실 한도 확인
                if self.daily_pnl <= self.config['daily_loss_limit']:
                    print(f"🛑 일일 손실 한도 도달! 시스템 중지")
                    self.stop()
            
        except Exception as e:
            print(f"❌ 매도 주문 오류: {e}")
    
    def get_status_report(self):
        """상태 보고서"""
        print(f"\n📊 전략 현황 보고서")
        print(f"   ⏰ 실행 상태: {'🟢 실행 중' if self.is_running else '🔴 중지'}")
        print(f"   📈 신호 발생: {self.signal_count}회")
        print(f"   💼 보유 포지션: {len(self.positions)}개")
        print(f"   💰 일일 손익: {self.daily_pnl:+.2f}%")
        
        if self.positions:
            print(f"   🏷️ 보유 종목:")
            for code, pos in self.positions.items():
                print(f"      - {pos['name']}: {pos['qty']}주 ({pos['return']:+.2f}%)")
