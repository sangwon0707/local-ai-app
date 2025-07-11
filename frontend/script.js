document.getElementById('fortune-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // 폼 입력 값 가져오기
    const name = document.getElementById('name').value;
    const birthdate = document.getElementById('birthdate').value;
    const birthtime = parseInt(document.getElementById('birthtime').value);
    const gender = document.getElementById('gender').value;
    const mbti = document.getElementById('mbti').value;

    // 사용자 정보 형식화
    const formattedBirthdate = birthdate.replace(/-/g, '년 ') + '일';
    const formattedBirthtime = `${birthtime < 12 ? '오전' : '오후'} ${birthtime % 12 || 12}시`;
    const formattedGender = gender === 'male' ? '남자' : '여자';

    try {
        // 백엔드 서버로 데이터 전송
        const response = await fetch('/fortune', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, birthdate, birthtime, gender, mbti }),
        });

        // 서버 응답을 JSON 형태로 파싱 (백엔드에서 {"fortune": "..."} 형태로 반환)
        const data = await response.json();
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = ''; // 이전 결과 지우기

        // 운세 정보 표시 (입력값 사용)
        const userInfoHtml = `
            <h2>오늘의 운세</h2>
            <div class="fortune-section user-info-table">
                <table>
                    <tr><th>날짜</th><td>${new Date().toLocaleDateString('ko-KR')}</td></tr>
                    <tr><th>이름</th><td>${name}</td></tr>
                    <tr><th>생년월일</th><td>${formattedBirthdate}</td></tr>
                    <tr><th>태어난 시간</th><td>${formattedBirthtime}</td></tr>
                    <tr><th>성별</th><td>${formattedGender}</td></tr>
                    <tr><th>MBTI</th><td>${mbti}</td></tr>
                </table>
            </div>
        `;
        resultDiv.innerHTML += userInfoHtml;

        // 운세 내용 표시 (LLM 응답 사용)
        const fortuneContentHtml = `
            <div class="fortune-section">
                <h3>운세 내용</h3>
                <p>${data.fortune.replace(/\n/g, '<br>')}</p> <!-- 줄바꿈 처리 -->
            </div>
        `;
        resultDiv.innerHTML += fortuneContentHtml;

        // 폼 숨기고 결과 표시
        document.getElementById('fortune-form').style.display = 'none';
        resultDiv.style.display = 'block';
        resultDiv.classList.add('fortune-result-display'); // 새로운 클래스 추가

    } catch (error) {
        // 네트워크 오류 등 fetch 자체에서 발생한 오류 처리
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = `운세를 가져오는 중 오류가 발생했습니다: ${error.message}`;
        console.error('Fetch error:', error);
    }
});