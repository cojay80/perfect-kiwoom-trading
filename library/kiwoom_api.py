"""
완벽한 키움 API 클래스
GitHub THANOS-PROJECT/makemoney 프로젝트를 참고하여 완전히 새로 제작
"""

import os
import sys
import time
import pythoncom
import win32gui
import win32con
import win32api
import multiprocessing as mp
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class KiwoomAPI(QAxWidget):
    """완벽한 키움 OpenAPI 클래스"""
    
    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        
        # 상태 변수
        self.connected = False
        self.account_num = None
        self.login_event_loop = None
        self.tr_event_loop = None
        
        # 데이터 저장
        self.tr_data = {}
        self.real_data = {}
        
        # 이벤트 연결
        self._connect_events()
        
        print("✅ KiwoomAPI 초기화 완료")
    
    def _connect_events(self):
        """이벤트 핸들러 연결"""
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveRealData.connect(self._receive_real_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        
    def login(self, user_id=None, password=None, auto_login=True):
        """로그인 (자동/수동 선택 가능)"""
        print("🔐 키움 로그인 시작...")
        
        if auto_login and user_id and password:
            return self._auto_login(user_id, password)
        else:
            return self._manual_login()
    
    def _manual_login(self):
        """수동 로그인 (기존 방식)"""
        try:
            print("📱 수동 로그인 창을 띄웁니다...")
            
            ret = self.dynamicCall("CommConnect()")
            if ret != 0:
                print(f"❌ 로그인 요청 실패: {ret}")
                return False
            
            self.login_event_loop = QEventLoop()
            self.login_event_loop.exec_()
            
            return self.connected
            
        except Exception as e:
            print(f"❌ 수동 로그인 오류: {e}")
            return False
    
    def _auto_login(self, user_id, password):
        """자동 로그인 (GitHub 프로젝트 방식)"""
        try:
            print("🤖 자동 로그인 프로세스 시작...")
            self._handle_login_window(user_id, password)
            return self.connected
            
        except Exception as e:
            print(f"❌ 자동 로그인 오류: {e}")
            return False
    
    def _handle_login_window(self, user_id, password):
        """로그인 창 자동 처리"""
        print("🪟 로그인 창 찾는 중...")
        
        timeout = 60
        for attempt in range(timeout):
            hwnd = self._find_window("Open API Login")
            
            if hwnd != 0:
                print("✅ 로그인 창 발견!")
                self._fill_login_form(hwnd, user_id, password)
                break
            
            time.sleep(1)
        
        # 로그인 완료 대기
        self._wait_for_login_complete()
    
    def _find_window(self, caption):
        """윈도우 찾기"""
        hwnd = win32gui.FindWindow(None, caption)
        if hwnd == 0:
            def enum_handler(hwnd, windows):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
            
            windows = []
            win32gui.EnumWindows(enum_handler, windows)
            
            for handle, title in windows:
                if caption in title:
                    hwnd = handle
                    break
        
        return hwnd
    
    def _fill_login_form(self, hwnd, user_id, password):
        """로그인 폼 자동 입력"""
        try:
            print("⌨️ 로그인 정보 자동 입력 중...")
            
            time.sleep(2)
            
            edit_id = win32gui.GetDlgItem(hwnd, 0x3E8)
            edit_pass = win32gui.GetDlgItem(hwnd, 0x3E9)
            btn_login = win32gui.GetDlgItem(hwnd, 0x1)
            
            # 모의투자 체크박스
            if not win32gui.IsWindowEnabled(win32gui.GetDlgItem(hwnd, 0x3EA)):
                checkbox_demo = win32gui.GetDlgItem(hwnd, 0x3ED)
                if checkbox_demo:
                    self._click_button(checkbox_demo)
            
            # ID 입력
            self._enter_text(edit_id, user_id)
            time.sleep(0.5)
            
            # 비밀번호 입력
            self._enter_text(edit_pass, password)
            time.sleep(0.5)
            
            # 로그인 버튼 클릭
            self._click_button(btn_login)
            print("✅ 로그인 버튼 클릭 완료")
            
        except Exception as e:
            print(f"❌ 로그인 폼 입력 오류: {e}")
    
    def _enter_text(self, hwnd, text):
        """텍스트 입력"""
        win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1)
        win32api.SendMessage(hwnd, win32con.EM_REPLACESEL, 0, text)
        time.sleep(0.1)
    
    def _click_button(self, hwnd):
        """버튼 클릭"""
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
        time.sleep(0.1)
    
    def _wait_for_login_complete(self):
        """로그인 완료 대기"""
        print("⏳ 로그인 처리 대기 중...")
        
        for secs in range(120):
            remaining = 120 - secs
            if remaining % 10 == 0:
                print(f"⏱️ 로그인 대기: {remaining}초 남음")
            
            # 버전처리 창 확인
            version_hwnd = self._find_window("opstarter")
            if version_hwnd != 0:
                print("🔄 버전처리 감지 - 자동 처리 중...")
                self._handle_version_update(version_hwnd)
            
            # 업그레이드 확인창
            upgrade_hwnd = self._find_window("업그레이드 확인")
            if upgrade_hwnd != 0:
                print("📥 업그레이드 창 자동 닫기")
                win32gui.PostMessage(upgrade_hwnd, win32con.WM_CLOSE, 0, 0)
            
            time.sleep(1)
    
    def _handle_version_update(self, hwnd):
        """버전처리 자동 처리"""
        try:
            static_hwnd = win32gui.GetDlgItem(hwnd, 0xFFFF)
            text = win32gui.GetWindowText(static_hwnd)
            
            if '버전처리' in text:
                print("✅ 버전처리 확인 - 자동 승인")
                close_btn = win32gui.GetDlgItem(hwnd, 0x2)
                if close_btn:
                    self._click_button(close_btn)
        except:
            pass
    
    def _event_connect(self, err_code):
        """로그인 이벤트 처리"""
        if err_code == 0:
            print("🎉 API 연결 성공!")
            self.connected = True
            self._get_account_info()
        else:
            print(f"❌ API 연결 실패: {err_code}")
            self.connected = False
        
        if self.login_event_loop:
            self.login_event_loop.exit()
    
    def _get_account_info(self):
        """계좌 정보 조회"""
        try:
            account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
            if account_list:
                self.account_num = account_list.split(';')[0]
                print(f"💳 계좌번호: {self.account_num}")
            
            user_id = self.dynamicCall("GetLoginInfo(QString)", "USER_ID")
            user_name = self.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
            server_gubun = self.dynamicCall("GetLoginInfo(QString)", "GetServerGubun")
            
            print(f"👤 사용자: {user_name} ({user_id})")
            
            if server_gubun == "1":
                print("🔵 모의투자 서버 접속")
            else:
                print("🔴 실거래 서버 접속")
                
        except Exception as e:
            print(f"❌ 계좌 정보 조회 오류: {e}")
    
    def get_current_price(self, code):
        """현재가 조회"""
        try:
            self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
            
            ret = self.dynamicCall("CommRqData(QString, QString, int, QString)", 
                                 "현재가조회", "opt10001", 0, "0001")
            
            if ret == 0:
                self.tr_event_loop = QEventLoop()
                self.tr_event_loop.exec_()
                
                return self.tr_data.get('현재가조회', {})
            else:
                print(f"❌ 현재가 조회 요청 실패: {ret}")
                return {}
                
        except Exception as e:
            print(f"❌ 현재가 조회 오류: {e}")
            return {}
    
    def send_order(self, rqname, screen_no, order_type, code, qty, price, hoga_type):
        """주문 전송"""
        try:
            if not self.account_num:
                print("❌ 계좌번호가 없습니다")
                return False
            
            ret = self.dynamicCall(
                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                [rqname, screen_no, self.account_num, order_type, code, qty, price, hoga_type, ""]
            )
            
            if ret == 0:
                print(f"✅ 주문 전송 성공: {code} {qty}주")
                return True
            else:
                print(f"❌ 주문 전송 실패: {ret}")
                return False
                
        except Exception as e:
            print(f"❌ 주문 전송 오류: {e}")
            return False
    
    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, prev_next, data_len, err_code, msg1, msg2):
        """TR 데이터 수신"""
        try:
            if rqname == "현재가조회":
                self._parse_current_price_data(trcode, rqname)
            
            if self.tr_event_loop:
                self.tr_event_loop.exit()
                
        except Exception as e:
            print(f"❌ TR 데이터 처리 오류: {e}")
    
    def _parse_current_price_data(self, trcode, rqname):
        """현재가 데이터 파싱"""
        try:
            name = self.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                  trcode, rqname, 0, "종목명").strip()
            price = self.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                   trcode, rqname, 0, "현재가").strip()
            change = self.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                    trcode, rqname, 0, "전일대비").strip()
            rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                  trcode, rqname, 0, "등락률").strip()
            
            self.tr_data['현재가조회'] = {
                'name': name,
                'price': abs(int(price)) if price else 0,
                'change': int(change) if change else 0,
                'rate': float(rate) if rate else 0.0
            }
            
        except Exception as e:
            print(f"❌ 현재가 데이터 파싱 오류: {e}")
            self.tr_data['현재가조회'] = {}
    
    def _receive_real_data(self, code, real_type, real_data):
        """실시간 데이터 수신"""
        try:
            if real_type == "주식체결":
                price = abs(int(self.dynamicCall("GetCommRealData(QString, int)", code, 10)))
                print(f"📈 {code} 실시간: {price:,}원")
                
        except Exception as e:
            print(f"❌ 실시간 데이터 처리 오류: {e}")
    
    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        """체결 데이터 수신"""
        print(f"📨 체결 알림: {gubun}")
    
    def start_real_data(self, codes, fids="10"):
        """실시간 데이터 시작"""
        try:
            if isinstance(codes, str):
                codes = [codes]
            
            codes_str = ";".join(codes)
            ret = self.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                 "1000", codes_str, fids, "1")
            
            print(f"📡 실시간 데이터 구독: {codes}")
            return ret == 0
            
        except Exception as e:
            print(f"❌ 실시간 데이터 시작 오류: {e}")
            return False
    
    def stop_real_data(self, screen_no="1000"):
        """실시간 데이터 중지"""
        try:
            self.dynamicCall("SetRealRemove(QString, QString)", screen_no, "ALL")
            print("⏹️ 실시간 데이터 구독 중지")
            
        except Exception as e:
            print(f"❌ 실시간 데이터 중지 오류: {e}")


# 편의 함수들
def create_kiwoom_api():
    """키움 API 객체 생성"""
    return KiwoomAPI()

def quick_login(user_id=None, password=None):
    """빠른 로그인"""
    api = create_kiwoom_api()
    
    if api.login(user_id, password):
        return api
    else:
        return None
