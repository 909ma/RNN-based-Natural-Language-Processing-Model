# JSON 파일을 읽어오는 함수
# 텔레그램에서 추출한 대화 데이터 파일을 user, text 형태의 csv파일로 추출
# 특정인의 발언만 기록하는 기능 개선
import json
import csv


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def extract_actor_text_to_csv(json_data, output_csv_file, target_name):
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Actor", "Text"])
        for message in json_data.get("messages", []):
            actor = message.get("from", "") if message.get(
                "from") else message.get("actor", "")
            text = message.get("text", "")

            try:
                # 'text' 필드가 문자열이 아닌 경우 처리
                if not isinstance(text, str):
                    text = str(text)  # 문자열로 변환

                # 텍스트가 없거나 'link'를 포함하면 무시
                if not text or any('link' in item.get('type', '') for item in message.get("text_entities", [])):
                    continue

                # 줄 바꿈 문자를 공백으로 대체
                text = text.replace("\n", " ")

                if actor == target_name:
                    # 추출 대상 사용자와 일치하면 CSV 파일에 쓰기
                    writer.writerow([actor, text])

            except Exception as e:
                print(f"오류 발생! 메시지: {message}")
                print(f"에러 메시지: {str(e)}")
                # break # 오류가 많이 나면 주석을 푸세요


# JSON 파일 경로
json_file_path = 'result_test.json'  # 실제 JSON 파일 경로로 변경하세요.

# 추출하고자 하는 특정 대상
target_name = '홍길동'  # 실제 대상 이름으로 변경하세요.

# CSV 파일 경로
output_csv_file_path = f'output_{target_name}.csv'

json_data = read_json_file(json_file_path)
extract_actor_text_to_csv(json_data, output_csv_file_path, target_name)
print(f"데이터 추출 및 저장이 완료되었습니다. {output_csv_file_path} 파일을 확인하세요.")
