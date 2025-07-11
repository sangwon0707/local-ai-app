from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import datetime
import sys # sys 모듈 임포트

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

model_name = "hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF"
model_file = "llama-3.2-3b-instruct-q4_k_m.gguf"
model_path = hf_hub_download(repo_id=model_name, filename=model_file)

# 운영체제에 따라 n_gpu_layers 설정
if sys.platform == "darwin":
    # macOS (Apple Silicon)의 경우 Metal GPU를 최대한 활용
    gpu_layers = -1
    print("macOS detected: n_gpu_layers set to -1 (Metal GPU acceleration).")
else:
    # Windows/Linux 등 다른 OS의 경우 CPU만 사용 (GPU 가속을 원하면 사용자가 직접 설정 필요)
    gpu_layers = 0
    print(f"{sys.platform} detected: n_gpu_layers set to 0 (CPU only). Adjust this value for GPU acceleration if available.")

llm = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=gpu_layers, verbose=False)

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
너는 최고의 한국 운세 전문가이자 MBTI 심리 상담가입니다. 사용자의 개인 정보와 MBTI를 바탕으로, 사주 운세처럼 흥미롭고 깊이 있는 통찰을 담아 오늘의 운세와 행동 조언을 작성해 주세요. 운세 내용은 유머러스하지만 진중한 톤으로, 긍정적이고 희망적인 문장으로 구성하고, Emoji를 적절히 사용하여 친근하고 예쁜 느낌을 더해주세요. 불필요한 줄바꿈 없이 자연스러운 문단 흐름을 유지해야 합니다.

--- 오늘의 운세 ---

사용자 정보:
- 이름: {user_data.name}
- 생일: {user_data.birthdate}
- 태어난 시간: {user_data.birthtime}시
- 성별: {user_data.gender}
- MBTI: {user_data.mbti}

오늘의 운세 내용: (200자 이내로 작성)

오늘의 행동 조언: (200자 이내로 작성)

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
