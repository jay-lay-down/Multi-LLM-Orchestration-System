import openai
import google.generativeai as genai
import anthropic
import time
import os

# =========================================================
# [설정] API 키 입력 (깃허브 올릴 땐 필히 환경변수 처리!)
# =========================================================
OPENAI_API_KEY = "sk-..."       # GPT용
GEMINI_API_KEY = "AIza..."      # 제미나이용
CLAUDE_API_KEY = "sk-ant-..."   # 클로드용

# 라이브러리 초기화
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# =========================================================
# 1. 하이브리드 에이전트 클래스 (3사 통합)
# =========================================================
class MultiModelAgent:
    def __init__(self, name, provider, model_name, role_desc, style_desc):
        self.name = name
        self.provider = provider  # "openai", "google", "anthropic"
        self.model_name = model_name
        
        # 시스템 프롬프트 구성
        self.system_prompt = f"""
        [Role]: {name}
        [Description]: {role_desc}
        [Style]: {style_desc}
        
        지금 우리는 비즈니스 좌담회 중입니다. 
        대화 흐름을 파악하고 당신의 역할에 맞춰 3문장 이내로 날카롭게 발언하세요.
        """

    def speak(self, history_log):
        """
        history_log: 지금까지의 대화 내용 (List of dicts or String)
        """
        print(f"🤖 {self.name} ({self.model_name}) 생각 중...")
        
        try:
            # -------------------------------------------------
            # CASE 1: OpenAI 
            # -------------------------------------------------
            if self.provider == "openai":
                messages = [{"role": "system", "content": self.system_prompt}]
                # 기록된 대화 내용을 User 메시지로 압축해서 전달
                messages.append({"role": "user", "content": f"대화 기록:\n{history_log}"})
                
                response = openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7
                )
                return response.choices[0].message.content

            # -------------------------------------------------
            # CASE 2: Anthropic 
            # -------------------------------------------------
            elif self.provider == "anthropic":
                # 클로드는 시스템 프롬프트가 파라미터로 따로 빠짐
                response = anthropic_client.messages.create(
                    model=self.model_name,
                    max_tokens=1024,
                    system=self.system_prompt,
                    messages=[
                        {"role": "user", "content": f"지금까지의 대화 흐름을 보고 답변하세요:\n{history_log}"}
                    ]
                )
                return response.content[0].text

            # -------------------------------------------------
            # CASE 3: Gemini
            # -------------------------------------------------
            elif self.provider == "google":
                model = genai.GenerativeModel(self.model_name)
                # 제미나이는 프롬프트 합쳐서 보내는 게 젤 편함
                full_prompt = f"{self.system_prompt}\n\n[현재 대화 로그]\n{history_log}\n\n[당신의 발언]:"
                response = model.generate_content(full_prompt)
                return response.text

        except Exception as e:
            return f"❌ [Error] {self.provider} 호출 실패: {str(e)}"

# =========================================================
# 2. 어벤져스 팀 구성 (페르소나)
# =========================================================

# 페르소나에 따라 각자 봇에 역할 부여

# =========================================================
# 3. 좌담회 실행 루프
# =========================================================
def run_debate(topic):
    history_text = f"주제: {topic}\n"
    print(f"🔥 [AI 좌담회 시작] 주제: {topic}\n")
    print("="*60)

    # 발언 순서: 클라이언트(불평) -> 통계학자(반박) -> PM(중재) -> 클라이언트(재반박)...
    speakers = [client, statistician, pm, client, pm]

    for speaker in speakers:
        # 1. 말하기
        msg = speaker.speak(history_text)
        
        # 2. 출력
        print(f"\n[{speaker.name}]:\n{msg}")
        print("-" * 60)
        
        # 3. 기록 (다음 타자가 읽을 수 있게 누적)
        history_text += f"\n[{speaker.name}]: {msg}"
        
        # 4. 딜레이 (사람이 읽을 시간)
        time.sleep(1.5)

if __name__ == "__main__":
    run_debate("우리 회사 신제품에 'AI 챗봇' 기능을 넣어야 할까?")
