from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

model_name = "hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF"
model_file = "llama-3.2-3b-instruct-q4_k_m.gguf"
model_path = hf_hub_download(repo_id=model_name, filename=model_file)

llm = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=-1, verbose=False)

class UserData(BaseModel):
    name: str
    birthdate: str
    birthtime: int
    gender: str
    mbti: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fortune")
async def get_fortune(user_data: UserData):
    prompt = f"""
다음 사용자 정보를 참고하여, 오늘의 운세를 작성하세요:
- 이름: {user_data.name}
- 생일: {user_data.birthdate}
- 태어난 시간: {user_data.birthtime}시
- 성별: {user_data.gender}
- MBTI: {user_data.mbti}

✨ 작성 규칙:
1. 오늘의 운세는 반드시 아래 형식을 따릅니다.
2. '오늘의 운세 내용'과 '오늘의 행동 조언'을 명확하게 구분하여 작성하세요.
3. 운세 내용과 행동 조언은 각각 200자 이내로 작성합니다.
4. Emoji를 적절히 사용해 긍정적이고 따뜻한 분위기를 만듭니다.
5. 같은 내용이나 비슷한 표현을 반복하지 마세요.
6. 문장 사이에 불필요한 줄바꿈 없이 자연스럽게 작성하세요.
7. 운세 내용은 유머러스하지만 진중한 톤으로 작성하고, 행동 조언은 실용적이고 명확한 조언으로 작성하세요.
8. 반드시 사용자 정보를 활용해 운세를 작성하며, 정보와 관련 없는 일반적인 내용은 작성하지 마세요.
9. **중요: 행동 조언은 운세 내용을 절대 복사하거나 반복하지 말고, 운세 내용을 참고하여 오늘 실천할 수 있는 구체적인 행동만 작성하세요.**

✨ 반드시 아래 형식을 그대로 따르세요 (괄호 안 문구는 절대 출력하지 마세요):

--- 오늘의 운세 ---

✨ 오늘의 운세 :
(여기에 운세 내용 입력, 150자 이내)

✨ 행동 조언:
(여기에 행동 조언 입력, 150자 이내)

--- 운세 끝 ---
"""
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 최고의 한국 운세 전문가이자 MBTI 심리 상담가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    raw_result = output['choices'][0]['message']['content']

    return {"fortune": raw_result}
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 최고의 한국 운세 전문가이자 MBTI 심리 상담가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    raw_result = output['choices'][0]['message']['content']

    return {"fortune": raw_result}
