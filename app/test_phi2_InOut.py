from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# 1. GGUF 모델 불러오기 (최초 실행 시 다운로드됨)
model_name = "hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF"
model_file = "llama-3.2-3b-instruct-q4_k_m.gguf"
model_path = hf_hub_download(repo_id=model_name, filename=model_file)

# 2. 모델 로드
llm = Llama(model_path=model_path, n_ctx=512, n_gpu_layers=-1, verbose=False)

while True:
    prompt = input("\n💬 질문을 입력하세요 (종료하려면 'exit'): ")
    if prompt.lower() == 'exit':
        print("종료합니다.")
        break

    output = llm.create_completion(prompt, max_tokens=100, stream=False)
    result = output['choices'][0]['text']


    print("\n🤖 답변:")
    print(result)
