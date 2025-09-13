"""
시스템 설정 파일
모든 매개변수와 설정을 중앙에서 관리
"""

# 🔐 로그인 설정
LOGIN_CONFIG = {
    'timeout': 120,                    # 로그인 타임아웃 (초)
    'retry_count': 3,                  # 재시도 횟수
    'auto_version_handle': True,       # 버전처리 자동 대응
    'auto_upgrade_close': True,        # 업그레이드 창 자동 닫기
}

# 📈 전략 설정 (1단계 - 심플 버전)
STRATEGY_CONFIG = {
    # 진입 조건
    'breakout_days': 20,               # 신고가 돌파 일수
    'volume_ratio': 2.0,               # 거래량 증가 비율 (200%)
    'trading_amount_limit': 1000,      # 거래대금 하한 (백만원)
    
    # 청산 조건
    'profit_target_1': 3.0,            # 1차 익절 목표 (%)
    'profit_target_2': 6.0,            # 2차 익절 목표 (%)
    'stop_loss': -2.0,                 # 손절 기준 (%)
    
    # 매매 시간
    'start_time': '10:30',             # 매매 시작 시간
    'end_time': '14:30',               # 매매 종료 시간
    'force_close_time': '14:30',       # 강제 청산 시간
}

# 🛡️ 리스크 관리 설정
RISK_CONFIG = {
    # 포지션 관리
    'position_size': 10.0,             # 종목당 투자 비중 (%)
    'max_positions': 5,                # 최대 동시 보유 종목수
    
    # 손실 한도
    'daily_loss_limit': -3.0,          # 일일 손실 한도 (%)
    'monthly_loss_limit': -10.0,       # 월간 손실 한도 (%)
    'consecutive_loss_limit': 3,       # 연속 손절 한도 (회)
    
    # 거래 제한
    'max_daily_trades': 10,            # 일일 최대 거래 횟수
    'min_gap_between_trades': 300,     # 거래간 최소 간격 (초)
}

# 📊 모니터링 종목 (거래대금 상위 200개 중 선별)
WATCH_LIST = [
    # 시가총액 Top 10
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
    
    # 거래량 활발 종목
    '003550',  # LG
    '017670',  # SK텔레콤
    '015760',  # 한국전력
    '009150',  # 삼성전기
    '010950',  # S-Oil
    '011200',  # HMM
    '259960',  # 크래프톤
    '373220',  # LG에너지솔루션
    '005380',  # 현대차
    '012330',  # 현대모비스
]

# 📡 실시간 데이터 설정
REALTIME_CONFIG = {
    'fids': '10,11,12,27,28',          # 수신할 FID (현재가,등락률,거래량 등)
    'screen_base': '1000',             # 화면번호 기준
    'max_stocks_per_screen': 50,       # 화면당 최대 종목수
}

# 📝 로깅 설정
LOGGING_CONFIG = {
    'level': 'INFO',                   # 로그 레벨
    'format': '%(asctime)s [%(levelname)s] %(message)s',
    'file_path': 'logs/trading.log',   # 로그 파일 경로
    'max_file_size': 10 * 1024 * 1024,  # 최대 파일 크기 (10MB)
    'backup_count': 5,                 # 백업 파일 개수
}

# 🔔 알림 설정 (선택사항)
NOTIFICATION_CONFIG = {
    'enabled': False,                  # 알림 사용 여부
    'telegram_bot_token': '',          # 텔레그램 봇 토큰
    'telegram_chat_id': '',            # 텔레그램 채팅 ID
    'slack_webhook_url': '',           # 슬랙 웹훅 URL
}

# 🔧 API 설정
API_CONFIG = {
    'request_delay': 0.5,              # TR 요청간 지연시간 (초)
    'max_retry': 3,                    # 최대 재시도 횟수
    'timeout': 30,                     # 요청 타임아웃 (초)
}

# 💾 데이터 저장 설정
DATA_CONFIG = {
    'save_trades': True,               # 거래 내역 저장 여부
    'save_path': 'data/',              # 데이터 저장 경로
    'backup_enabled': True,            # 백업 사용 여부
    'backup_interval': 3600,           # 백업 간격 (초)
}

# 🎯 백테스트 설정 (향후 확장)
BACKTEST_CONFIG = {
    'start_date': '2023-01-01',        # 백테스트 시작일
    'end_date': '2023-12-31',          # 백테스트 종료일
    'initial_cash': 10000000,          # 초기 자금 (1천만원)
    'commission': 0.00015,             # 수수료 (0.015%)
    'slippage': 0.001,                 # 슬리피지 (0.1%)
}

# 🌐 웹 대시보드 설정 (향후 확장)
WEB_CONFIG = {
    'enabled': False,                  # 웹 대시보드 사용 여부
    'host': '127.0.0.1',              # 호스트 주소
    'port': 5000,                      # 포트 번호
    'debug': False,                    # 디버그 모드
}

# 📈 성과 분석 설정
PERFORMANCE_CONFIG = {
    'benchmark': 'KOSPI',              # 벤치마크 지수
    'risk_free_rate': 0.03,            # 무위험 이자율 (3%)
    'report_frequency': 'daily',       # 리포트 주기 (daily/weekly/monthly)
}

# 🔐 보안 설정
SECURITY_CONFIG = {
    'encrypt_credentials': True,       # 인증정보 암호화
    'log_sensitive_data': False,       # 민감정보 로깅 금지
    'auto_logout_minutes': 480,        # 자동 로그아웃 (8시간)
}

# 📱 시스템 모니터링
SYSTEM_CONFIG = {
    'health_check_interval': 60,       # 헬스체크 간격 (초)
    'memory_limit_mb': 1024,           # 메모리 사용 한도 (MB)
    'cpu_limit_percent': 80,           # CPU 사용 한도 (%)
    'auto_restart_on_error': True,     # 오류시 자동 재시작
}

# 🎨 UI 설정
UI_CONFIG = {
    'theme': 'dark',                   # 테마 (dark/light)
    'font_size': 12,                   # 폰트 크기
    'refresh_rate': 1000,              # 화면 갱신 주기 (ms)
    'show_debug_info': False,          # 디버그 정보 표시
}

# 🏷️ 환경별 설정
ENVIRONMENT = {
    'mode': 'development',             # development/production
    'demo_mode': True,                 # 데모 모드 (모의투자 강제)
    'safe_mode': True,                 # 안전 모드 (추가 검증)
}

# 📊 전략별 설정 (향후 확장)
STRATEGIES = {
    'breakout': {
        'enabled': True,
        'priority': 1,
        'config': STRATEGY_CONFIG
    },
    'momentum': {
        'enabled': False,
        'priority': 2,
        'config': {}
    },
    'mean_reversion': {
        'enabled': False,
        'priority': 3,
        'config': {}
    }
}

# 📋 설정 검증 함수
def validate_config():
    """설정값 유효성 검증"""
    errors = []
    
    # 필수 설정 확인
    if STRATEGY_CONFIG['stop_loss'] >= 0:
        errors.append("손절 기준은 음수여야 합니다")
    
    if RISK_CONFIG['position_size'] <= 0 or RISK_CONFIG['position_size'] > 20:
        errors.append("포지션 크기는 0~20% 범위여야 합니다")
    
    if RISK_CONFIG['max_positions'] <= 0 or RISK_CONFIG['max_positions'] > 10:
        errors.append("최대 포지션 수는 1~10개 범위여야 합니다")
    
    if len(WATCH_LIST) == 0:
        errors.append("모니터링 종목이 설정되지 않았습니다")
    
    # 시간 설정 확인
    try:
        from datetime import datetime
        start = datetime.strptime(STRATEGY_CONFIG['start_time'], '%H:%M')
        end = datetime.strptime(STRATEGY_CONFIG['end_time'], '%H:%M')
        if start >= end:
            errors.append("매매 시작시간이 종료시간보다 늦습니다")
    except:
        errors.append("시간 형식이 올바르지 않습니다 (HH:MM)")
    
    if errors:
        print("❌ 설정 오류:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ 설정 검증 완료")
    return True

# 설정 요약 출력 함수
def print_config_summary():
    """설정 요약 출력"""
    print("📋 시스템 설정 요약")
    print("=" * 50)
    print(f"🎯 전략: 20일 신고가 돌파")
    print(f"💰 익절: {STRATEGY_CONFIG['profit_target_1']}% / {STRATEGY_CONFIG['profit_target_2']}%")
    print(f"🛡️ 손절: {STRATEGY_CONFIG['stop_loss']}%")
    print(f"📊 포지션: 종목당 {RISK_CONFIG['position_size']}%, 최대 {RISK_CONFIG['max_positions']}개")
    print(f"⏰ 매매시간: {STRATEGY_CONFIG['start_time']} ~ {STRATEGY_CONFIG['end_time']}")
    print(f"📈 모니터링: {len(WATCH_LIST)}개 종목")
    print(f"🔔 일일한도: {RISK_CONFIG['daily_loss_limit']}%")
    print("=" * 50)

if __name__ == "__main__":
    # 설정 검증 및 요약 출력
    if validate_config():
        print_config_summary()
