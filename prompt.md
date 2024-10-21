주어진 논문에서 추출된 텍스트를 분석하여 다음 단계에 따라 Mermaid 다이어그램을 한국어로 생성해주세요:

1단계: 논문 텍스트 내용 분석 및 1차 그래프 생성

1. 논문 전체 내용을 꼼꼼히 읽고 핵심 내용을 파악하세요.
2. 다이어그램 기본 설정:
    - 방향: 위에서 아래로 (TB)
    - 노드 스타일 정의:
    classDef question fill:#EF9A9A,stroke:#B71C1C,stroke-width:2px,color:#000;
    classDef solution fill:#BBDEFB,stroke:#0D47A1,stroke-width:2px,color:#000;
    classDef method fill:#C8E6C9,stroke:#1B5E20,stroke-width:2px,color:#000;
    classDef result fill:#FFF59D,stroke:#F57F17,stroke-width:2px,color:#000;
    classDef discussion fill:#FFCCBC,stroke:#BF360C,stroke-width:2px,color:#000;
    classDef conclusion fill:#C5E1A5,stroke:#33691E,stroke-width:2px,color:#000;
    classDef link fill:#FFECB3,stroke:#FF6F00,stroke-width:2px,color:#000;
3. 각 섹션별로 서브그래프 구성:
    Introduction:
    - 논문에서 명시된 주요 연구 문제 3개 추출
    - 논문의 주요 연구 목표 1개 식별
    - 논문에서 제안하는 주요 솔루션 2개 파악
    
    Method:
    
    - 논문에서 설명하는 주요 실험 방법 2개 추출
    - 사용된 데이터 수집 방법 1개 식별
    - 논문의 실험 설계 방식 1개 파악
    
    Results:
    
    - 논문에 명시된 주요 연구 결과 4개 추출
    
    Discussion:
    
    - 논문에서 주장하는 주요 연구 기여점 2개 식별
    - 저자가 언급한 연구의 한계점 2개 파악
    
    Conclusion:
    
    - 논문에서 제시하는 향후 연구 방향 2개 추출
4. 노드 연결:
    - 추출한 정보를 바탕으로 각 섹션 내 노드들 간의 관계를 화살표로 연결
    - 섹션 간 논리적 흐름을 나타내는 연결 추가
5. 각 노드의 내용을 PDF에서 추출한 실제 텍스트로 채우기

**2단계: 2차 그래프 생성** 

2차 그래프는 각 섹션별로 하나씩 모두 생성해야합니다.

1. 노드 스타일 정의:
classDef keynode fill:#FFECB3,stroke:#FF6F00,stroke-width:2px,color:#000;
classDef claim fill:#BBDEFB,stroke:#0D47A1,stroke-width:2px,color:#000;
classDef evidence fill:#C8E6C9,stroke:#1B5E20,stroke-width:2px,color:#000;
2. 각 섹션별로 다음 구조 생성:
    - 1차 그래프의 각 노드를 keynode로 사용
    - 각 keynode에 대한 Claim 노드 생성
    - 각 Claim에 대한 Evidence 노드 생성
    - 중요도 태그 ($H, $M, $L) 추가
3. 노드 연결:
    - keynode --> Claim --> Evidence 구조로 연결
    - 관련 있는 keynode들 간의 연결
    - 시간 흐름을 나타내는 점선 화살표 추가

**3단계: 최종 네트워크 생성**

1. 1차 그래프와 2차 그래프 통합:
    - 1차 그래프의 구조를 유지하면서 2차 그래프의 Claim-Evidence 구조 추가
    - 섹션 간 연결 유지
2. 추가 지침:
    - 모든 노드에 고유 ID 부여 (예: I1, S1, M1, R1, D1, C1)
    - Evidence에는 구체적인 실험 결과나 데이터 포함
    - 대학원생 및 교수 수준의 전문성 유지
    - 논문의 핵심 내용을 빠짐없이 포함
3. 최종 검토:
    - 전체 구조의 일관성 확인
    - 노드 간 연결이 논문의 논리 흐름을 정확히 나타내는지 확인
    - 한국어 표현의 자연스러움과 정확성 확인

주의사항:

- 모든 내용은 반드시 제공된 텍스트에서 직접 추출해야 합니다.
- 추측이나 일반화된 내용이 아닌, 텍스트에 명시적으로 언급된 정보만 사용하세요.
- 한국어로 번역 시, 원문의 의미를 정확히 전달하도록 주의하세요.
- 전문용어는 가능한 원어를 유지하고 필요시 한국어 설명을 병기하세요.

각 단계별로 Mermaid 다이어그램 코드를 생성해주세요. 최종 네트워크는 논문의 전체 구조와 텍스트에서 추출한 핵심 내용을 명확하게 표현해야 합니다. Your result should return the meramid code ONLY and do not return any accompanying text.