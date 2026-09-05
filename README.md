# 장구 연습 연구소 (Janggu Practice Lab)

개인 사물놀이 공연 연습 지원 시스템을 작은 실험부터 연구하는 저장소입니다. 현재 가장 중요한 사용자는 `단아솟동`에서 삼도 사물놀이 공연을 준비하며 장구를 연습하는 연주자 본인입니다.

> 이 저장소에서 실제로 구현된 범위는 **Phase 0A — 장구 타격 시점(Onset) 검출**뿐입니다. 아래의 나머지 내용은 검증 결과에 따라 바뀔 수 있는 장기 연구 방향이며, 구현 완료된 제품 요구사항이 아닙니다.

## 왜 시작했나

혼자 공연을 준비할 때는 박자를 맞추는 것만으로 충분하지 않습니다. 공연 전체의 가락과 순서, 각 가락의 반복과 맺음, 다음 가락으로 넘어가는 Cue와 Transition을 기억해야 합니다. 같은 가락도 공연의 위치와 반복에 따라 Tempo, Accent, Dynamics 및 악기별 역할이 달라질 수 있습니다. 다른 악기와 합주해야 할 부분을 혼자 연습하기 어렵고, 누락·추가 타격이나 점진적인 Tempo 변화도 스스로 판단하기 어렵습니다.

장기 목표는 단순한 장구 박자 분석기가 아니라 다음과 같은 개인 연습 시스템입니다.

> 사물놀이 공연의 전체 구성과 가락을 익히고 외우며, 다른 악기들과 실제 합주하듯 혼자 연습하고, 자신의 연주를 분석하여 공연 준비를 돕는 시스템

## 첫 번째 Reference Performance

이 프로젝트는 하나의 보편적이고 고정된 “삼도 사물놀이 정답”을 가정하지 않습니다. 첫 Reference Performance는 성남 지역 `우리소리연구회 솟대` 계열에서 김진형 사부님 등을 통해 배우고 전승·발전되어 온 **현재 단아솟동의 실제 삼도 사물놀이 공연과 연습**입니다. 향후 제공될 실제 가락보, 연습 녹음, 공연 영상과 배운 내용의 메모를 Source of Truth로 존중합니다.

중요한 외부 Reference Source로 [솟대예감TV](https://www.youtube.com/@sodo96)를 기록합니다. 링크·제목·출처·설명 등의 Metadata를 관리하는 것을 우선하며, 원본 영상을 저장소에 무단 복제하거나 재배포하지 않습니다. 현재 YouTube 수집·다운로드·분석은 구현하지 않습니다.

## 공연과 가락을 보는 관점

핵심은 `공연 구조 + 가락 데이터 + 실제 연주`가 재생, 분석, 연습 피드백으로 이어지는 것입니다. 실제 자료를 보기 전에 정확한 구조나 용어를 임의로 확정하지 않지만, 다음 계층과 각 계층 안의 음악적 흐름을 연구 대상으로 봅니다.

```text
공연(Performance)
├── 작품 / 큰 연주 파트(Repertoire / Piece)
│   ├── 주요 가락 / 구간
│   │   ├── 세부 가락 / Pattern
│   │   ├── Repeat
│   │   └── Transition
│   └── Tempo, Dynamics, 고조·이완, 맺음
└── 악기별 Part: 꽹과리, 징, 장구, 북
```

전체 공연뿐 아니라 굿거리·자진모리·휘모리 등의 각 구간과 세부 가락 내부에도 반복, 고조, 맺음과 전환이 있을 수 있습니다. Tempo Change, Dynamics, Accent, Crescendo/Diminuendo, 악기별 상대 음량과 역할, Cue, Rest, 진입·퇴장도 장기 연구 대상이지만 지금 Schema로 고정하지 않습니다.

장기적으로는 사용자가 한 악기를 맡고 나머지 Part가 Reference Performance에 따라 연주되는 Virtual Samulnori Ensemble, 그리고 처음에는 현재/다음 가락·반복 횟수·Cue를 보여 주다가 안내를 줄여 가는 암기 Scaffold를 지향합니다.

## 자료와 Provenance 원칙

- **Personal Practice First / Real Performance First:** 개인의 실제 공연 연습과 단아솟동 자료에서 출발합니다.
- **Performance & Garak-centered:** 단순 박자보다 공연과 가락 구조를 중심에 둡니다.
- **Provenance Matters:** 공연, 계열, 지도, 사용 목적, 시기, 원자료와 Version을 추적합니다.
- **Source Material Preservation:** 원본(Source)과 변환·분석 결과(Derived)를 분리하고 원본을 덮어쓰지 않습니다.
- **Human Authority / Human-in-the-loop:** 자동 분석보다 연주자와 사부님의 판단 및 검수를 우선합니다.
- **Existing Standards First:** 자체 DSL보다 정간보, 구음, 기존 가락보, MusicXML, MIDI와 percussion notation 등 기존 표준을 먼저 조사합니다.
- **Small Steps / Validate Before Build:** 실제 연습 가치가 확인된 뒤 다음 단계로 갑니다.
- **Simple Architecture:** 현재 검증에 필요하지 않은 Framework나 추상화를 도입하지 않습니다.

실제 자료가 들어오면 먼저 원형을 보존하고 공연 구성, 가락 순서와 이름, 구음, 박/장단, Pattern, Repeat, Transition, Cue, Tempo, Dynamics, 악기별 Part, 맺음과 암기 방식을 분석합니다. 향후 `source/`와 `derived/` 분리를 검토하되, 자료 특성을 보기 전에는 디렉터리나 Schema를 확정하지 않습니다. 저작권·초상권·공유 범위를 확인하고 큰 원본 Audio/Video는 Git 대신 접근 통제된 외부 저장소와 식별자/Checksum으로 연결하는 방식을 권장합니다.

## 연구·개발 로드맵

다음은 확정 사양이 아니라 현재의 연구 방향입니다.

| 단계 | 연구 방향 | 상태 |
|---|---|---|
| 0A | 10~20초 장구 Audio의 타격 시점(Onset) 검출 | **현재 구현** |
| 0B | 녹음 → 분석을 위한 작은 Test UI | 미구현, 0A 검증 후 판단 |
| 1 | 단아솟동 실제 가락보·공연·연습 자료 정리 | 미구현 |
| 2 | 국악/사물놀이 표기와 음악 데이터 표준 조사 | 미구현 |
| 3 | 실제 작은 가락 하나의 Machine-readable Prototype | 미구현 |
| 4 | 가락 데이터 → 악기 Sample Audio 재생 | 미구현 |
| 5 | 여러 가락 연결, Repeat, Transition | 미구현 |
| 6 | Tempo, Dynamics, Accent, 악기별 역할 | 미구현 |
| 7 | Reference와 실제 연주의 Timing·누락·추가·전환 비교 | 미구현 |
| 8 | 취약 가락/Transition 부분 반복과 공연 암기 | 미구현 |
| 9 | 선택 악기를 제외한 Virtual Samulnori Ensemble | 미구현 |
| 10 | 실제 연주의 Dynamics 분석 | 미구현 |
| 11 | Reference Audio/Video의 반자동 구조·가락 Annotation | 미구현 |
| 12 | Audio/Video → 사람이 검수할 가락보 초안 | 미구현 |
| 13 | 검수 데이터로 분석 개선, 필요할 때만 ML 검토 | 미구현 |
| 14 | 공연 구조·연습 이력 기반 AI Practice Coach | 미구현 |
| 15 | 연습 장소용 스마트폰 Prototype | 미구현 |
| 16 | 가치 검증 후 Camera/Motion 자세 분석 | 미구현 |

## 현재 구현: Phase 0A

Audio를 mono로 불러오고 파형(Waveform)에서 onset strength envelope를 계산한 뒤 peak를 선택합니다. 검출 시점을 초 단위로 출력하고, 원본 파형과 검출선을 비교할 수 있는 PNG를 만듭니다. AI/ML은 사용하지 않습니다.

### 새 PC / 임시 Code Server에서 GitHub 준비

Git 작성자 설정과 SSH 개인키는 보안상 Repository에 저장되지 않습니다. 따라서 새 PC나 새 EC2 Code Server에서는 한 번씩 설정해야 합니다. 이 프로젝트에서는 다른 Repository의 작성자 설정을 바꾸지 않도록 저장소 안에서 `--local`을 사용합니다.

```bash
git config --local user.name "Seungsuk Ryoo"
git config --local user.email "seungsuk.training@gmail.com"
git config --local --list
```

GitHub 계정은 `seungsuk-training`입니다. 새 환경에서 SSH 인증이 필요하면 환경마다 별도의 키를 만드는 방식을 권장합니다.

```bash
ssh-keygen -t ed25519 -C "seungsuk.training@gmail.com"
cat ~/.ssh/id_ed25519.pub
```

출력된 **공개키(`.pub`)만** GitHub의 `Settings → SSH and GPG keys → New SSH key`에 등록하고 연결을 확인합니다.

```bash
ssh -T git@github.com
git clone git@github.com:seungsuk-training/janggu-practice-lab.git
```

개인키인 `~/.ssh/id_ed25519`는 Git, README, 메신저 또는 공개 Cloud Storage에 올리지 않습니다. 일시적인 교육용 EC2가 사라지면 새 환경에서 새 키를 만들고 공개키를 다시 등록하는 것으로 충분합니다. 더 이상 사용하지 않는 EC2의 키는 GitHub SSH key 목록에서 삭제합니다. 오래 유지할 개인 PC의 키를 백업해야 한다면 암호화된 Password Manager나 암호화된 오프라인 저장소만 사용하고, 복호화 암호는 별도로 보관합니다.

여러 GitHub 계정을 한 PC에서 사용할 때만 `~/.ssh/config`에 계정별 Host alias를 둘 수 있습니다. 이 저장소의 현재 remote처럼 `github-seungsuk-training` alias를 사용한다면 새 환경에도 다음 설정이 필요합니다.

```sshconfig
Host github-seungsuk-training
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

```bash
git remote set-url origin git@github-seungsuk-training:seungsuk-training/janggu-practice-lab.git
ssh -T git@github-seungsuk-training
```

GitHub 계정이 하나뿐이면 alias 없이 `git@github.com:seungsuk-training/janggu-practice-lab.git`을 사용하는 편이 단순합니다. Repository를 clone한 뒤에는 `git remote -v`, `git config --local --list`, `ssh -T ...` 세 가지로 설정을 확인합니다.

### 설치 (Ubuntu)

Python 3.10 이상을 권장합니다. WAV만 사용할 경우 추가 시스템 Package 없이 시작할 수 있습니다. MP3/M4A 등은 환경에 따라 FFmpeg가 필요하므로 첫 실험은 WAV를 권장합니다.

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 테스트 Audio 준비

10~20초 동안 장구를 한 번씩 분명히 치는 구간에서 시작해 `samples/janggu-test.wav`로 둡니다. `samples/`의 Audio/Video는 Git에서 무시됩니다.

Ubuntu에서는 녹음기 앱 또는 아래 명령을 사용할 수 있습니다(장치 이름은 환경에 따라 다름).

```bash
sudo apt install alsa-utils
arecord -f S16_LE -r 48000 -c 1 -d 15 samples/janggu-test.wav
```

스마트폰에서는 자동 음량 조절(AGC), 소음 제거, 음성 강조를 끌 수 있는 무압축 녹음 앱을 권장합니다. 장구에서 1~2m 떨어진 고정 위치에 두고 clipping이 없도록 시험 타격 후 WAV/PCM으로 내보내세요. 권장 형식은 mono WAV, 24-bit 또는 16-bit PCM, 48 kHz(최소 44.1 kHz)입니다. 메신저 전송은 압축/음량 변경 가능성이 있으므로 파일 전송이나 USB를 사용합니다.

### 실행

```bash
python src/detect_onsets.py samples/janggu-test.wav
```

검출 시점과 분석 설정이 터미널에 출력되고 기본 결과는 `samples/janggu-test-onsets.png`에 저장됩니다. 창으로도 보려면 `--show`를 추가합니다.

```bash
python src/detect_onsets.py samples/janggu-test.wav --show
python src/detect_onsets.py samples/janggu-test.wav --delta 0.12 --wait-ms 70
python src/detect_onsets.py --help
```

`--delta`는 주변 평균보다 얼마나 뚜렷한 peak만 고를지 정하는 민감도 문턱입니다. 값이 작으면 더 많은 타격을, 크면 더 확실한 타격만 검출합니다. `--wait-ms`는 두 검출 사이 최소 간격입니다. 빠른 연타가 빠지면 줄이고, 한 타격이 여러 번 잡히면 늘립니다. `--hop-length`는 시간 해상도와 계산량을 조절하는 고급 Parameter입니다.

### 실제 테스트와 판정

1. 연주하며 타격 수와 대략적인 시점을 메모하거나 손뼉 같은 시작 표식을 남깁니다.
2. Audio를 직접 들으며 PNG의 세로선이 실제 타격과 맞는지 확인합니다.
3. 누락(false negative), 추가 검출(false positive), 한 타격의 중복 검출을 각각 기록합니다.
4. 궁편/채편, 약·강 타격, 느린 타격과 빠른 연타를 나누어 시험합니다.
5. 같은 설정으로 3회 이상 녹음해 우연이 아닌지 확인합니다.

자동화된 기본 확인은 다음과 같습니다.

```bash
python -m compileall src
python src/detect_onsets.py --help
```

실제 성공 기준은 완벽한 정확도가 아니라, 10~20초 실제 장구 녹음에서 사람이 듣고 파형과 비교했을 때 연습에 쓸 가능성이 보일 정도로 타격 시점이 맞는 것입니다.

## 알려진 한계와 조정 순서

잔향이 긴 공간, 주변 악기/말소리, microphone clipping, 스마트폰의 AGC, 매우 약한 타격과 빠른 연타에서는 누락이나 중복이 생길 수 있습니다. 현재 구현은 “타격이 언제 있었는가”만 검출하며 궁편/채편, 손/채, 강약, 박자, Tempo, 가락을 분류하지 않습니다. PNG는 긴 파일에서 조밀해지므로 현재 목표인 짧은 녹음에 맞습니다.

결과가 좋지 않으면 먼저 녹음 level과 clipping을 확인하고, 다음 순서로 조정합니다.

1. 너무 적게 검출되면 `--delta`를 낮추고, 너무 많으면 높입니다.
2. 빠른 연타가 합쳐지면 `--wait-ms`를 낮추고, 중복이면 높입니다.
3. 미세한 Timing이 중요하면 `--hop-length`를 256으로 낮춥니다.

궁편/채편 구분에는 타격별로 정답 Label이 붙은 다양한 연주자·장구·공간의 Dataset, onset 주변의 spectrum/timbre feature, microphone 위치 변화에 강한 분류법과 교차 검증이 필요합니다. Dynamics 연구에는 AGC/limiter를 끄고 같은 microphone·거리·각도·gain을 유지하며 clipping을 피해야 합니다. Calibration 타격과 연주자의 강약 Label을 함께 기록해야 물리적 음량과 음악적 강약을 혼동하지 않을 수 있습니다.

## 향후 연구 과제

Audio/Video에서 가락보 초안으로 발전할 때는 겹쳐 울리는 네 악기의 source separation, 궁편/채편과 타격 주법 분류, 잔향·잡음에 강한 onset, 변화하는 Tempo/박 구조 추정, 유사 Pattern과 Repeat/Transition 경계 탐색, 영상·음향 동기화, 서로 다른 전승/Version의 Provenance, 불확실성을 사람이 효율적으로 고치는 Annotation UI가 주요 난점입니다.

외부 Reference URL은 향후 별도 Metadata 파일에 URL, 채널/제작자, 제목, 게시일, 열람일, 관련 공연/구간, 사용 목적, 권리 메모를 함께 기록하는 방식을 검토합니다. 링크가 사라질 수 있으므로 원본을 무단 복제하는 대신 안정적인 ID와 필요한 범위의 연구 메모를 남깁니다.

Phase 0B로 넘어갈 기준은 (1) 서로 다른 실제 10~20초 장구 녹음 여러 개에서 Parameter 조정으로 유용한 검출 결과를 반복해서 얻고, (2) 녹음→파일 복사→CLI 실행 과정이 실제 연습을 방해하는 핵심 마찰로 확인되며, (3) UI에서 보여 줄 최소 정보와 실패 사례를 설명할 수 있을 때입니다. 그 전에는 실제 Audio로 0A를 조정하고 기록합니다.

