<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>프리미엄 재테크 통합 계산기</title>
    <!-- 고퀄리티 프리텐다드 폰트 & Chart.js -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #007AFF;
            --primary-gradient: linear-gradient(135deg, #007AFF 0%, #0056b3 100%);
            --bg: #f2f2f7;
            --card: rgba(255, 255, 255, 0.9);
            --text: #1d1d1f;
            --text-sub: #6e6e73;
            --border: rgba(0, 0, 0, 0.08);
            --success: #34c759;
        }

        body {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            margin: 0;
            padding: 20px 10px;
            color: var(--text);
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 550px;
            margin: 0 auto;
            background: var(--card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 30px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .tabs {
            display: flex;
            background: rgba(118, 118, 128, 0.12);
            padding: 4px;
            margin: 20px;
            border-radius: 14px;
            gap: 2px;
        }

        .tab-btn {
            flex: 1;
            border: none;
            padding: 10px 2px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            background: transparent;
            color: var(--text-sub);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap;
        }

        .tab-btn.active {
            background: white;
            color: var(--text);
            box-shadow: 0 3px 8px rgba(0,0,0,0.12), 0 3px 1px rgba(0,0,0,0.04);
        }

        .content {
            padding: 0 30px 35px 30px;
            display: none;
        }

        .content.active {
            display: block;
            animation: slideUp 0.5s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 { font-size: 22px; margin: 0 0 10px 0; font-weight: 700; letter-spacing: -0.5px; }
        .description { font-size: 14px; color: var(--text-sub); margin-bottom: 25px; font-weight: 400; }

        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 8px; color: var(--text); padding-left: 4px; }
        .input-wrapper { position: relative; display: flex; align-items: center; }
        .input-wrapper input {
            width: 100%;
            padding: 16px;
            font-size: 16px;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: #f5f5f7;
            outline: none;
            transition: all 0.3s;
            font-weight: 600;
        }
        .input-wrapper input:focus { 
            background: #fff;
            border-color: var(--primary); 
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1); 
        }
        .input-wrapper .unit { position: absolute; right: 16px; font-size: 14px; font-weight: 600; color: var(--text-sub); }

        .calc-btn {
            width: 100%;
            padding: 18px;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 18px;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.3s;
            box-shadow: 0 10px 20px -5px rgba(0, 122, 255, 0.3);
        }
        .calc-btn:hover { transform: translateY(-2px); box-shadow: 0 15px 25px -5px rgba(0, 122, 255, 0.4); }

        .result-box {
            margin-top: 35px;
            padding: 30px;
            background: linear-gradient(180deg, #f9f9fb 0%, #f2f2f7 100%);
            border-radius: 24px;
            display: none;
            border: 1px solid #fff;
        }
        .result-title { font-size: 14px; color: var(--text-sub); text-align: center; font-weight: 500; }
        .result-main { font-size: 32px; font-weight: 800; color: var(--primary); text-align: center; margin: 12px 0; letter-spacing: -1px; }
        .result-sub { font-size: 14px; color: #444; text-align: center; line-height: 1.6; }

        canvas { margin-top: 25px; border-radius: 12px; }

        @media (max-width: 480px) {
            .container { border-radius: 0; margin: -10px; }
            .content { padding: 0 20px 30px 20px; }
            .tab-btn { font-size: 11px; padding: 10px 0; }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('lifecycle', event)">생애주기</button>
        <button class="tab-btn" onclick="showTab('paradise', event)">낙원계산기</button>
        <button class="tab-btn" onclick="showTab('dsr', event)">DSR 계산</button>
        <button class="tab-btn" onclick="showTab('compound', event)">복리 계산</button>
    </div>

    <!-- 1. 생애주기 계산기 -->
    <div id="lifecycle" class="content active">
        <h2>🗓️ 생애주기 시뮬레이션</h2>
        <p class="description">은퇴 전까지 얼마를 모으고, 은퇴 후 자산이 어떻게 변할까요?</p>
        <div class="input-group">
            <label>현재 나이 & 은퇴 예상 나이</label>
            <div style="display: flex; gap: 12px;">
                <div class="input-wrapper" style="flex:1;"><input type="text" id="life-age" value="30" oninput="formatInput(this)"><span class="unit">세</span></div>
                <div class="input-wrapper" style="flex:1;"><input type="text" id="life-retire" value="60" oninput="formatInput(this)"><span class="unit">세</span></div>
            </div>
        </div>
        <div class="input-group">
            <label>현재 보유 자산</label>
            <div class="input-wrapper"><input type="text" id="life-asset" value="50,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <div class="input-group">
            <label>매월 저축액(은퇴전) & 매월 생활비(은퇴후)</label>
            <div style="display: flex; gap: 12px;">
                <div class="input-wrapper" style="flex:1;"><input type="text" id="life-save" value="2,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
                <div class="input-wrapper" style="flex:1;"><input type="text" id="life-spend" value="3,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
            </div>
        </div>
        <button class="calc-btn" onclick="calcLifecycle()">미래 자산 그래프 확인</button>
        <div id="res-lifecycle" class="result-box">
            <div class="result-title">자산 정점 (은퇴 시점)</div>
            <div class="result-main" id="life-max-val">0원</div>
            <canvas id="lifeChart"></canvas>
        </div>
    </div>

    <!-- 2. 낙원 계산기 -->
    <div id="paradise" class="content">
        <h2>🏝️ 경제적 자유 낙원계산기</h2>
        <p class="description">숨만 쉬어도 돈이 들어오는 시스템 수익의 목표치를 계산합니다.</p>
        <div class="input-group">
            <label>한 달에 쓰고 싶은 금액 (현재 물가 기준)</label>
            <div class="input-wrapper"><input type="text" id="p-spend" value="3,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <div class="input-group">
            <label>연간 기대 수익률 (배당/이자/임대 등)</label>
            <div class="input-wrapper"><input type="text" id="p-rate" value="5" oninput="formatInput(this, true)"><span class="unit">%</span></div>
        </div>
        <button class="calc-btn" onclick="calcParadise()">필요한 은퇴 자산은?</button>
        <div id="res-paradise" class="result-box">
            <div class="result-title">나의 경제적 자유 자산</div>
            <div class="result-main" id="p-result">0원</div>
            <div class="result-sub" id="p-detail">로딩 중...</div>
        </div>
    </div>

    <!-- 3. DSR 계산기 -->
    <div id="dsr" class="content">
        <h2>🏦 DSR(부채원리금상환비율)</h2>
        <p class="description">내 소득에서 대출 원리금이 차지하는 비중을 계산합니다.</p>
        <div class="input-group">
            <label>연간 총 소득 (세전)</label>
            <div class="input-wrapper"><input type="text" id="d-income" value="50,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <div class="input-group">
            <label>연간 총 주담대 상환액</label>
            <div class="input-wrapper"><input type="text" id="d-mort" value="12,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <div class="input-group">
            <label>연간 기타 대출 상환액 (신용대출 등)</label>
            <div class="input-wrapper"><input type="text" id="d-other" value="5,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <button class="calc-btn" onclick="calcDSR()">내 DSR 지수 확인</button>
        <div id="res-dsr" class="result-box">
            <div class="result-title">나의 DSR 지수</div>
            <div class="result-main" id="d-result">0%</div>
            <div class="result-sub" id="d-detail">로딩 중...</div>
        </div>
    </div>

    <!-- 4. 복리 계산기 -->
    <div id="compound" class="content">
        <h2>📈 복리의 마법 계산기</h2>
        <p class="description">시간과 수익률이 만나 자산이 불어나는 과정을 확인하세요.</p>
        <div class="input-group">
            <label>시작 금액</label>
            <div class="input-wrapper"><input type="text" id="c-p" value="10,000,000" oninput="formatInput(this)"><span class="unit">원</span></div>
        </div>
        <div class="input-group">
            <label>연평균 수익률 & 투자 기간</label>
            <div style="display: flex; gap: 12px;">
                <div class="input-wrapper" style="flex:1;"><input type="text" id="c-r" value="10" oninput="formatInput(this, true)"><span class="unit">%</span></div>
                <div class="input-wrapper" style="flex:1;"><input type="text" id="c-y" value="20" oninput="formatInput(this)"><span class="unit">년</span></div>
            </div>
        </div>
        <button class="calc-btn" onclick="calcCompound()">미래 가치 계산</button>
        <div id="res-compound" class="result-box">
            <div class="result-title">예상 자산 결과</div>
            <div class="result-main" id="c-result">0원</div>
            <div class="result-sub">단순 합산 대비 약 <span id="c-diff" style="color:var(--success); font-weight:700;">0원</span> 더 많습니다.</div>
        </div>
    </div>
</div>

<script>
    let myChart = null;

    // 실시간 숫자 포맷팅 함수
    function formatInput(el, isFloat = false) {
        let value = el.value.replace(/[^0-9.]/g, ""); // 숫자와 점만 남김
        if (!isFloat) value = value.replace(/\./g, ""); // 정수면 점 제거
        
        const parts = value.split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ","); // 3자리마다 콤마
        el.value = parts.join(".");
    }

    // 콤마 제거 후 숫자로 변환
    function getNum(id) {
        const val = document.getElementById(id).value.replace(/,/g, "");
        return parseFloat(val) || 0;
    }

    function showTab(tabId, event) {
        document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    function fmt(num) { return Math.floor(num).toLocaleString('ko-KR'); }

    function calcLifecycle() {
        const age = getNum('life-age');
        const retire = getNum('life-retire');
        const asset = getNum('life-asset');
        const save = getNum('life-save') * 12;
        const spend = getNum('life-spend') * 12;

        let currentAsset = asset;
        let labels = [];
        let data = [];
        let maxAsset = 0;

        for (let i = age; i <= 95; i++) {
            labels.push(i + '세');
            data.push(currentAsset);
            if (i < retire) {
                currentAsset += save;
                maxAsset = currentAsset;
            } else {
                currentAsset -= spend;
            }
            if (currentAsset < 0) currentAsset = 0;
        }

        document.getElementById('res-lifecycle').style.display = 'block';
        document.getElementById('life-max-val').innerText = fmt(maxAsset) + ' 원';

        if (myChart) myChart.destroy();
        const ctx = document.getElementById('lifeChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '자산',
                    data: data,
                    borderColor: '#007AFF',
                    borderWidth: 3,
                    backgroundColor: 'rgba(0, 122, 255, 0.08)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { 
                    x: { grid: { display: false } },
                    y: { 
                        beginAtZero: true,
                        ticks: { callback: v => (v >= 100000000) ? (v/100000000).toFixed(1) + '억' : (v/10000).toLocaleString() + '만' } 
                    }
                }
            }
        });
        document.getElementById('res-lifecycle').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function calcParadise() {
        const spend = getNum('p-spend') * 12;
        const rate = getNum('p-rate') / 100;
        if(rate <= 0) { alert('수익률을 0보다 크게 입력해주세요.'); return; }
        const target = spend / rate;

        document.getElementById('res-paradise').style.display = 'block';
        document.getElementById('p-result').innerText = fmt(target) + ' 원';
        document.getElementById('p-detail').innerHTML = `연 <b>${document.getElementById('p-rate').value}%</b>의 수익이 발생할 때,<br>자본을 깎지 않고 매달 <b>${fmt(spend/12)}원</b>을 평생 쓸 수 있습니다.`;
    }

    function calcDSR() {
        const income = getNum('d-income');
        const mort = getNum('d-mort');
        const other = getNum('d-other');
        if(income <= 0) { alert('연소득을 입력해주세요.'); return; }
        const dsr = ((mort + other) / income) * 100;

        document.getElementById('res-dsr').style.display = 'block';
        document.getElementById('d-result').innerText = dsr.toFixed(2) + ' %';
        const detail = document.getElementById('d-detail');
        if (dsr <= 40) {
            detail.innerHTML = '✅ <span style="color:#34c759; font-weight:700;">안정권:</span> 시중은행 대출 기준(40%) 이내입니다.';
        } else {
            detail.innerHTML = '⚠️ <span style="color:#ff3b30; font-weight:700;">주의:</span> 소득 대비 원리금 부담이 매우 높습니다.';
        }
    }

    function calcCompound() {
        const p = getNum('c-p');
        const r = getNum('c-r') / 100;
        const y = getNum('c-y');
        const result = p * Math.pow((1 + r), y);
        const simple = p + (p * r * y);

        document.getElementById('res-compound').style.display = 'block';
        document.getElementById('c-result').innerText = fmt(result) + ' 원';
        document.getElementById('c-diff').innerText = fmt(result - simple) + '원';
    }
</script>

</body>
</html>
