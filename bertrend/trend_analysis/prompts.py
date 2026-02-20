#  Copyright (c) 2024, RTE (https://www.rte-france.com)
#  See AUTHORS.txt
#  SPDX-License-Identifier: MPL-2.0
#  This file is part of BERTrend.
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from bertrend import OUTPUT_PATH
from bertrend.trend_analysis.data_structure import SignalAnalysis, TopicSummaryList

# Global variables for prompts
SIGNAL_INTRO = {
    "en": """As an elite strategic foresight analyst with extensive expertise across multiple domains and industries, your task is to conduct a comprehensive evaluation of a potential signal derived from the following topic summary:

{summary_from_first_prompt}

Leverage your knowledge and analytical skills to provide an in-depth analysis of this signal's potential impact and evolution:
""",
    "fr": """En tant qu'analyste de prospective stratégique d'élite avec une expertise étendue dans de multiples domaines et industries, votre tâche est de mener une évaluation complète d'un signal potentiel dérivé du résumé de sujet suivant :

{summary_from_first_prompt}

Utilisez vos connaissances et compétences analytiques pour fournir une analyse approfondie de l'impact potentiel et de l'évolution de ce signal :
""",
    "ko": """당신은 다양한 산업과 도메인에 대한 전문성을 갖춘 최고 수준의 전략적 미래예측 분석가입니다. 아래 주제 요약으로부터 도출된 잠재 신호를 종합 평가하세요.

{summary_from_first_prompt}

제공된 내용을 근거로 이 신호의 잠재 영향과 진화 방향을 심층 분석하세요:
""",
}

SIGNAL_INSTRUCTIONS = {
    "en": """
Analyze this signal only if the input data is sufficiently complete and substantive. If the subject summary lacks completeness, substance, specificity, or novelty, respond with an empty JSON dictionary: {}

=== DECISION RULES (STRICT SUFFICIENCY) ===
- Overall Sufficiency: Proceed with analysis only if the topic summary contains enough concrete, non-trivial information to support evidence-based reasoning across at least one analysis dimension (Impact, Evolution, Interconnections, Drivers/Inhibitors).
- Section Sufficiency: For each analysis section (Impact, Evolution Scenarios, Interconnections and Synergies, Drivers and Inhibitors), include the section ONLY if the input contains enough detail to meet the Minimum Quality Requirements. If not, omit the section entirely (do not include placeholders).
- Evidence-First: Prefer omission over speculation. Do not infer facts not supported by the provided summary.

For substantial signals, provide the following sections (include only those that meet the standards; omit any that do not):

1. Potential Impact Analysis:
   - Examine potential effects on sectors, industries, and societal aspects.
   - Cover immediate (1–2 years), medium (3–5 years), and long-term (5–10 years) horizons.
   - Include ripple effects and second-order consequences when supportable.

2. Evolution Scenarios:
   - Describe plausible future developments and manifestation paths.
   - Identify factors shaping the trajectory.
   - Provide both optimistic and pessimistic scenarios only if both are sufficiently supported; otherwise include the supported one(s) and omit the rest.

3. Interconnections and Synergies:
   - Identify interactions with current trends or emerging phenomena.
   - Discuss synergies or conflicts with existing systems or paradigms.

4. Drivers and Inhibitors:
   - Analyze accelerants and amplifiers of the signal.
   - Examine barriers, constraints, or resistances.

Your analysis should be thorough and nuanced, going beyond surface-level observations, and grounded in the provided content. Make well-reasoned predictions only when they are logically supported by the input. If analysis cannot be substantiated with clear reasoning, omit that section.

=== OUTPUT QUALITY STANDARDS ===
Avoid:
- Vague generalizations
- Obvious conclusions without new insight
- Insufficient evidence
- Generic observations
- Circular reasoning
- Superficial treatment
- Unsubstantiated speculation
- Outdated perspectives

=== MINIMUM QUALITY REQUIREMENTS (APPLY PER SECTION) ===
Each included section must demonstrate at least 2 of:
- Specific Context: Clear temporal, geographic, or sectoral boundaries with examples
- Concrete Evidence: Quantifiable insights, verifiable examples, or substantiated claims from the input
- Novel Perspectives: Non-obvious connections or emerging patterns grounded in the input
- Actionable Intelligence: Guidance that enables decision-making or planning
- Cross-Domain Impact: Implications across multiple sectors or domains
- Measurable Dimensions: Metrics, indicators, or tracking mechanisms
- Causal Analysis: Clear cause-and-effect or contributing factors
- Strategic Relevance: Direct link to business, policy, or societal decisions

=== OUTPUT REQUIREMENTS ===
- Section-Level Omission: Omit any section that cannot meet the Minimum Quality Requirements with the provided information.
- Evidence-Based: Use specific, quantifiable language with concrete examples derived from the input.
- Confidence Levels: Clearly distinguish high-confidence assessments from speculative insights.
- Decision-Focused: Prioritize actionable intelligence for strategic decision-makers.
- Balanced Objectivity: Maintain rigor while acknowledging uncertainties and limitations.
- Temporal Structure: Organize insights across immediate (1–2 years), medium (3–5 years), and long-term (5–10 years) where applicable.
- Final Validation: Before finalizing, remove any statement that cannot be traced to or logically derived from the provided summary.

If no section can meet these standards, return an empty JSON dictionary: {}
""",
    "fr": """
Analysez ce signal uniquement si les données d’entrée sont suffisamment complètes et substantielles. Si le résumé du sujet manque de complétude, de substance, de spécificité ou de nouveauté, répondez avec un dictionnaire JSON vide : {}

=== RÈGLES DE DÉCISION (SUFFISANCE STRICTE) ===
- Suffisance Globale : Poursuivez l’analyse uniquement si le résumé contient des informations concrètes et non triviales permettant un raisonnement fondé sur des preuves sur au moins une dimension d’analyse (Impact, Évolution, Interconnexions, Facteurs moteurs/Freins).
- Suffisance par Section : Pour chaque section d’analyse (Impact, Scénarios d’évolution, Interconnexions et synergies, Facteurs moteurs et freins), incluez la section UNIQUEMENT si les informations d’entrée satisfont les Exigences Minimales de Qualité. Sinon, omettez entièrement la section (sans placeholder).
- Priorité aux preuves : Préférez l’omission à la spéculation. N’inférez aucun fait non appuyé par le résumé fourni.

Pour les signaux substantiels, fournissez les sections suivantes (incluez uniquement celles qui respectent les standards ; omettez celles qui ne les respectent pas) :

1. Analyse des Impacts Potentiels :
   - Examinez les effets potentiels sur les secteurs, les industries et les dimensions sociétales.
   - Couvrez les horizons court terme (1–2 ans), moyen terme (3–5 ans) et long terme (5–10 ans).
   - Incluez les effets de second ordre lorsque c’est justifiable.

2. Scénarios d’Évolution :
   - Décrivez des trajectoires plausibles d’évolution future.
   - Identifiez les facteurs influençant cette trajectoire.
   - Fournissez des scénarios optimistes et pessimistes uniquement s’ils sont tous deux suffisamment étayés ; sinon, incluez uniquement ceux qui sont justifiables.

3. Interconnexions et Synergies :
   - Identifiez les interactions avec les tendances actuelles ou phénomènes émergents.
   - Discutez les synergies ou conflits avec les systèmes/paradigmes existants.

4. Facteurs Moteurs et Freins :
   - Analysez les accélérateurs et amplificateurs du signal.
   - Examinez les barrières, contraintes et résistances.

Votre analyse doit être approfondie, nuancée et strictement ancrée dans le contenu fourni. Formulez des anticipations uniquement lorsqu’elles sont logiquement soutenues par l’entrée. Si une section n’est pas suffisamment étayée, omettez-la.

=== STANDARDS DE QUALITÉ DE SORTIE ===
Évitez :
- Les généralisations vagues
- Les conclusions évidentes sans valeur ajoutée
- Les preuves insuffisantes
- Les observations génériques
- Les raisonnements circulaires
- Les traitements superficiels
- Les spéculations non étayées
- Les perspectives obsolètes

=== EXIGENCES MINIMALES DE QUALITÉ (PAR SECTION) ===
Chaque section incluse doit démontrer au moins 2 des éléments suivants :
- Contexte précis : bornes temporelles, géographiques ou sectorielles explicites avec exemples
- Preuves concrètes : éléments quantifiables, exemples vérifiables ou affirmations étayées par l’entrée
- Perspectives originales : connexions non triviales ou signaux émergents ancrés dans l’entrée
- Valeur actionnable : recommandations utiles à la décision ou à la planification
- Impact transverse : implications sur plusieurs secteurs/domaines
- Dimensions mesurables : métriques, indicateurs ou mécanismes de suivi
- Analyse causale : relation de cause à effet explicite
- Pertinence stratégique : lien direct avec des décisions business, publiques ou sociétales

=== EXIGENCES DE SORTIE ===
- Omission par section : supprimez toute section qui ne satisfait pas les Exigences Minimales de Qualité.
- Fondé sur les preuves : utilisez un langage spécifique et, si possible, quantifié avec des exemples concrets tirés de l’entrée.
- Niveaux de confiance : distinguez clairement les évaluations à forte confiance des points plus spéculatifs.
- Orientation décision : priorisez les informations actionnables pour les décideurs stratégiques.
- Objectivité équilibrée : maintenez la rigueur tout en explicitant incertitudes et limites.
- Structure temporelle : organisez les éléments selon court (1–2 ans), moyen (3–5 ans), long terme (5–10 ans) si applicable.
- Validation finale : avant rendu final, retirez toute affirmation qui ne peut être retracée ou logiquement dérivée du résumé fourni.

Si aucune section ne respecte ces standards, renvoyez un dictionnaire JSON vide : {}
""",
    "ko": """
입력 데이터가 충분히 완전하고 실질적인 경우에만 이 신호를 분석하세요. 주제 요약이 완전성, 구체성, 실질성, 신규성을 충족하지 못하면 빈 JSON 객체 {} 를 반환하세요.

=== 판단 규칙 (엄격한 충분성 기준) ===
- 전체 충분성: 주제 요약에 최소 1개 이상의 분석 축(영향, 진화, 상호연계, 촉진/저해요인)에 대해 근거 기반 추론이 가능한 구체적이고 비자명한 정보가 있을 때만 분석을 수행하세요.
- 섹션 충분성: 각 분석 섹션(잠재 영향, 진화 시나리오, 상호연계·시너지, 촉진요인·저해요인)은 최소 품질 기준을 만족할 때만 포함하세요. 만족하지 못하면 섹션을 완전히 생략하세요(placeholder 금지).
- 근거 우선: 추측보다 생략을 우선하세요. 입력 요약에 없는 사실을 추론/창작하지 마세요.

분석이 가능한 신호에 대해서는 아래 섹션을 작성하되, 기준을 만족하는 섹션만 포함하세요.

1. 잠재 영향 분석
   - 산업/섹터/사회 영역에 미칠 영향을 분석하세요.
   - 단기(1~2년), 중기(3~5년), 장기(5~10년) 관점을 포함하세요.
   - 근거가 있을 때 2차 파급효과까지 제시하세요.

2. 진화 시나리오
   - 향후 전개될 수 있는 현실적 경로를 제시하세요.
   - 경로를 좌우하는 요인을 명시하세요.
   - 낙관/비관 시나리오는 각각 근거가 충분할 때만 포함하고, 한쪽만 충분하면 해당 시나리오만 제시하세요.

3. 상호연계 및 시너지
   - 현재 트렌드/신흥 현상과의 상호작용을 식별하세요.
   - 기존 시스템/패러다임과의 시너지 또는 충돌을 설명하세요.

4. 촉진요인과 저해요인
   - 신호를 가속·증폭하는 요인을 분석하세요.
   - 확산을 막는 장벽·제약·저항 요인을 분석하세요.

분석은 피상적 요약을 넘어서야 하며, 반드시 입력 내용에 근거해야 합니다. 논리적으로 뒷받침되지 않는 예측은 작성하지 말고 해당 섹션을 생략하세요.

=== 출력 품질 기준 ===
다음을 피하세요:
- 모호한 일반론
- 새로운 통찰 없는 당연한 결론
- 근거 부족 주장
- 진부한 관찰
- 순환논리
- 피상적 설명
- 무근거 추측
- 시대에 뒤처진 관점

=== 최소 품질 요구사항 (섹션별 적용) ===
포함되는 각 섹션은 아래 항목 중 최소 2개를 충족해야 합니다.
- 구체적 맥락: 시간/지역/산업 범위가 명확하고 예시가 있음
- 구체적 근거: 정량 정보, 검증 가능한 사례, 입력 기반 근거 제시
- 새로운 관점: 비자명한 연결고리나 신흥 패턴 도출
- 실행 가능성: 의사결정/기획에 바로 활용 가능한 시사점
- 교차 도메인 영향: 여러 산업·도메인에 대한 함의
- 측정 가능성: 지표/메트릭/추적 방법 제시
- 인과 분석: 원인-결과 또는 기여요인 구조가 명확함
- 전략적 관련성: 비즈니스/정책/사회 의사결정과 직접 연결됨

=== 출력 요구사항 ===
- 섹션 생략 원칙: 최소 품질 기준을 못 맞추는 섹션은 제외하세요.
- 근거 기반 표현: 입력에서 도출 가능한 구체적·가능하면 정량적 언어를 사용하세요.
- 신뢰도 표기: 고신뢰 판단과 가설적 판단을 명확히 구분하세요.
- 의사결정 중심: 전략적 의사결정자 관점의 실행 인사이트를 우선하세요.
- 균형 잡힌 객관성: 불확실성과 한계를 함께 명시하세요.
- 시간축 구조화: 가능하면 단기(1~2년), 중기(3~5년), 장기(5~10년)로 구조화하세요.
- 최종 검증: 입력 요약에서 추적·논리 도출 불가능한 문장은 최종 출력에서 제거하세요.

어떤 섹션도 기준을 충족하지 못하면 빈 JSON 객체 {} 를 반환하세요.
""",
}

TOPIC_SUMMARY_PROMPT = {
    "en": """
As an expert analyst specializing in trend analysis and strategic foresight, your task is to provide a comprehensive evolution summary of Topic {topic_number}. Use only the information provided below:

{content_summary}

Structure your analysis as follows:

For the first timestamp:

## [Concise yet impactful title capturing the essence of the topic at this point]
### Date: [Relevant date or time frame - format %Y-%m-%d]
### Key Developments
- [Bullet point summarizing a major development or trend]
- [Additional bullet points as needed]

### Analysis
[2-3 sentences maximum providing deeper insights into the developments, their potential implications, and their significance in the broader context of the topic's evolution]

For all subsequent timestamps:

## [Concise yet impactful title capturing the essence of the topic at this point]
### Date: [Relevant date or time frame - format %Y-%m-%d]
### Key Developments
- [Bullet point summarizing a major development or trend]
- [Additional bullet points as needed]

### Analysis
[2-3 sentences maximum providing deeper insights into the developments, their potential implications, and their significance in the broader context of the topic's evolution]

### What's New
[1-2 sentences maximum highlighting how this period differs from the previous one, focusing on new elements or significant changes]

Provide your analysis using only this format, based solely on the information given. Do not include any additional summary or overview sections beyond what is specified in this structure.
""",
    "fr": """
En tant qu'analyste expert spécialisé dans l'analyse des tendances et la prospective stratégique, votre tâche est de fournir un résumé complet de l'évolution du Sujet {topic_number}. Utilisez uniquement les informations fournies ci-dessous :

{content_summary}

Structurez votre analyse comme suit :

Pour le premier timestamp :

## [Titre concis mais percutant capturant l'essence du sujet à ce moment]
### Date : [Date ou période pertinente - format %Y-%m-%d]
### Développements Clés
- [Point résumant un développement majeur ou une tendance]
- [Points supplémentaires si nécessaire]

### Analyse
[2-3 phrases maximum fournissant des insights plus profonds sur les développements, leurs implications potentielles et leur importance dans le contexte plus large de l'évolution du sujet]

Pour tous les timestamps suivants :

## [Titre concis mais percutant capturant l'essence du sujet à ce moment]
### Date : [Date ou période pertinente - format %Y-%m-%d]
### Développements Clés
- [Point résumant un développement majeur ou une tendance]
- [Points supplémentaires si nécessaire]

### Analyse
### Analyse
[2-3 phrases maximum fournissant des insights plus profonds sur les développements, leurs implications potentielles et leur importance dans le contexte plus large de l'évolution du sujet]

### Nouveautés
[1-2 phrases maximum soulignant en quoi cette période diffère de la précédente, en se concentrant sur les nouveaux éléments ou les changements significatifs]

Fournissez votre analyse en utilisant uniquement ce format, basé uniquement sur les informations données. N'incluez pas de sections de résumé ou d'aperçu supplémentaires au-delà de ce qui est spécifié dans cette structure.
""",
    "ko": """
당신은 트렌드 분석과 전략적 미래예측 분야의 전문 분석가입니다. 아래 정보만 사용하여 Topic {topic_number}의 시점별 진화 요약을 작성하세요.

{content_summary}

반드시 아래 형식만 사용하세요.

첫 번째 시점:

## [해당 시점의 핵심을 압축적으로 보여주는 제목]
### Date: [관련 날짜/기간 - 형식 %Y-%m-%d]
### Key Developments
- [주요 변화/흐름 1개]
- [필요 시 추가 bullet]

### Analysis
[해당 변화의 의미, 잠재적 함의, 전체 진화 맥락에서의 중요성을 2~3문장 이내로 서술]

두 번째 시점 이후 모든 시점:

## [해당 시점의 핵심을 압축적으로 보여주는 제목]
### Date: [관련 날짜/기간 - 형식 %Y-%m-%d]
### Key Developments
- [주요 변화/흐름 1개]
- [필요 시 추가 bullet]

### Analysis
[해당 변화의 의미, 잠재적 함의, 전체 진화 맥락에서의 중요성을 2~3문장 이내로 서술]

### What's New
[직전 시점 대비 새롭게 나타난 요소 또는 유의미한 변화를 1~2문장으로 서술]

반드시 위 형식만 사용하세요. 입력 정보 바깥의 내용을 추가하지 마세요. 별도의 총평/요약 섹션을 임의로 추가하지 마세요.
""",
}


def get_prompt(
    language: str,
    prompt_type: str,
    topic_number: int = None,
    content_summary: str = None,
    summary_from_first_prompt: str = None,
):
    language_map = {
        "English": "en",
        "French": "fr",
        "Korean": "ko",
    }
    lang = language_map.get(language, "ko")

    if prompt_type == "weak_signal":
        prompt = (
            SIGNAL_INTRO[lang].format(
                summary_from_first_prompt=summary_from_first_prompt
            )
            + SIGNAL_INSTRUCTIONS[lang]
        )

    elif prompt_type == "topic_summary":
        prompt = TOPIC_SUMMARY_PROMPT[lang].format(
            topic_number=topic_number, content_summary=content_summary
        )
    else:
        raise ValueError(f"Unsupported prompt type: {prompt_type}")

    return prompt


def save_html_output(html_output, output_file="signal_llm.html"):
    """Function to save the model's output as HTML"""
    output_path = OUTPUT_PATH / output_file

    # Save the cleaned HTML
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)
    logger.debug(f"Cleaned HTML output saved to {output_path}")


def fill_html_template(
    topic_summary_list: TopicSummaryList,
    signal_analysis: SignalAnalysis,
    language: str = "fr",
) -> str:
    """Fill the HTML template with appropriate data"""
    # Setup Jinja2 environment
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(template_dir),
    )
    template = env.get_template(
        "signal_llm_template_en.html"
        if language == "en"
        else "signal_llm_template_fr.html"
    )

    # Sort the list by date from most recent to least recent
    try:
        sorted_topic_summary_by_time_period = sorted(
            topic_summary_list.topic_summary_by_time_period,
            key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"),
            reverse=True,
        )
        topic_summary_list.topic_summary_by_time_period = (
            sorted_topic_summary_by_time_period
        )
    except Exception:
        logger.warning("Cannot sort summaries by date, probably wrong date format")

    # Render the template with the provided data
    rendered_html = template.render(
        topic_summary_list=topic_summary_list, signal_analysis=signal_analysis
    )

    # FIXME: many \n are added...
    rendered_html = rendered_html.replace("\n", "")
    rendered_html = rendered_html.replace("\\'", "'")

    return rendered_html
