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
            # CASE 1: OpenAI (GPT-4o) - 논리/분석 담당
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
            # CASE 2: Anthropic (Claude 3.5) - 감성/뉘앙스/고객 담당
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
            # CASE 3: Google (Gemini) - 창의성/중재 담당
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
# 2. 어벤져스 팀 구성 (페르소나 + 최적 모델 매칭)
# =========================================================

# 1. 통계학자 (GPT-4o): 논리적이고 딱딱한 계산은 GPT가 최고
statistician = MultiModelAgent(
    name="김박사(통계학자)",
    provider="openai",
    model_name="gpt-4o",
    role_desc="30년 경력의 보수적인 통계학자. 데이터 없는 주장은 혐오함.",
    style_desc="냉소적임. '유의미한가?', 'p-value는?' 같은 용어 사용."
)

# 2. 클라이언트 (Claude 3.5 Sonnet): 사람 같은 자연스러움과 '갑질' 뉘앙스는 클로드가 잘함
client = MultiModelAgent(
    name="최상무(클라이언트)",
    provider="anthropic",
    model_name="claude-3-5-sonnet-20240620",
    role_desc="성격 급한 마케팅 임원. 어려운 말 싫어하고 매출과 임팩트만 중요함.",
    style_desc="감정적이고 직설적임. '그래서 돈이 됩니까?', '확 와닿지가 않네' 등 사용."
)

# 3. PM/아이디어 (Gemini 1.5 Pro): 긴 문맥 이해와 중재, 창의적 제안은 제미나이
pm = MultiModelAgent(
    name="이PM(사회자)",
    provider="google",
    model_name="gemini-1.5-pro",
    role_desc="프로젝트 매니저. 두 사람 사이를 중재하고 현실적인 절충안을 제시함.",
    style_desc="부드럽고 정리하는 말투. '두 분 말씀의 핵심은...', '그럼 이렇게 하시죠' 사용."
)

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
