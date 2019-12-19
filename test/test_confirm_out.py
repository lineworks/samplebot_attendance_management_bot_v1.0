from calender.actions.confirm_out import confirm_out_message
from unittest.mock import patch
import calender.common.local_timezone

@patch('calender.common.local_timezone.load_time_zone')
def test_confirm_out(mocked):
    mocked.return_value = 'Asia/Seoul'
    # Wednesday, November 13, 2019 4:52:15 PM GMT+09:00
    message = confirm_out_message(1573631535, 3, 20)
    assert {
        'i18nTexts':
            [{'language': 'en_US',
              'text': 'Clock-out time has been registered. The total working '
                      'hours for Wednesday, November 13 is 3 hours and 20 '
                      'minutes.'},
             {'language': 'ja_JP',
              'text': '退勤時間の登録が完了しました。11月 13日 水曜日の合計勤務時間は 3時間 20分です。'},
             {'language': 'ko_KR',
              'text': '퇴근 시간 등록이 완료되었습니다. 11월 13일 수요일 총 근무 시간은 3시간 20분입니다.'}],
        'text': 'Clock-out time has been registered. The total working hours for '
                'Wednesday, November 13 is 3 hours and 20 minutes.',
        'type': 'text'} == message
