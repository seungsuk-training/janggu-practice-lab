# 새 PC·Code Server의 Git/GitHub SSH 설정

이 문서는 새 PC 또는 임시 EC2 Code Server에서 `seungsuk-training/janggu-practice-lab` 작업 환경을 안전하게 재현하는 절차입니다. 현재 저장소는 SSH Host Alias `github-seungsuk-training`을 사용합니다.

## 0. 적용 범위와 기본 도구

명령은 Bash 기준입니다. Ubuntu·EC2, macOS, Windows의 WSL 또는 Git Bash에서는 경로와 설치 명령이 다를 수 있습니다. Windows에서는 WSL 또는 Git Bash 중 하나를 정해 일관되게 사용합니다.

```bash
git --version
ssh -V
```

Ubuntu 또는 EC2에 없다면 설치합니다.

```bash
sudo apt update
sudo apt install -y git openssh-client
```

macOS는 Xcode Command Line Tools 또는 Homebrew, WSL은 해당 Linux 배포판의 Package Manager, Git Bash는 Git for Windows의 공식 설치 방법을 따릅니다.

## 1. 새 환경 설정 순서

```text
Git·OpenSSH 확인
→ ~/.ssh 준비
→ ED25519 SSH Key Pair 생성
→ Public Key만 GitHub에 등록
→ ~/.ssh/config에 Host Alias 추가
→ SSH 인증 확인
→ Repository Clone
→ Repository-local 작성자 설정
→ Remote·Branch·작성자·Working Tree 확인
→ VS Code로 열기
```

### 1.1 SSH 디렉터리와 Key Pair 준비

PC 또는 임시 EC2마다 전용 Key Pair를 생성합니다. 아래 파일명은 새 환경용 예시입니다.

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh

ssh-keygen -t ed25519 \
  -C "seungsuk.training@gmail.com" \
  -f ~/.ssh/id_ed25519_seungsuk_training
```

가능하면 안전한 Passphrase를 설정합니다. 권한을 정리한 뒤 **Public Key만** 출력합니다.

```bash
chmod 600 ~/.ssh/id_ed25519_seungsuk_training
chmod 644 ~/.ssh/id_ed25519_seungsuk_training.pub
cat ~/.ssh/id_ed25519_seungsuk_training.pub
```

출력된 Public Key를 GitHub의 `Settings → SSH and GPG keys → New SSH key`에 등록합니다. Key 제목에는 PC 이름, `code-server`, EC2 이름이나 생성일처럼 환경을 식별할 정보를 넣습니다.

### 1.2 SSH Host Alias 설정

`~/.ssh/config`를 통째로 덮어쓰지 말고 다음 Block을 기존 파일에 추가합니다. 여러 계정의 SSH Alias는 하나의 `~/.ssh/config`에 공존할 수 있습니다.

```bash
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

```sshconfig
Host github-seungsuk-training
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_seungsuk_training
  IdentitiesOnly yes
```

`IdentityFile`은 실제로 생성한 Private Key 경로와 일치해야 합니다. `github-seungsuk-training`은 로컬 Alias이므로 새 환경마다 다시 설정합니다.

```bash
ssh -T git@github-seungsuk-training
```

GitHub 인증 성공 메시지 뒤의 Shell Access 제한 안내는 정상입니다. 인증된 계정이 `seungsuk-training`인지 확인합니다.

### 1.3 Clone과 Repository-local 작성자 설정

```bash
git clone \
  git@github-seungsuk-training:seungsuk-training/janggu-practice-lab.git
cd janggu-practice-lab

git config --local user.name "Seungsuk Ryoo"
git config --local user.email "seungsuk.training@gmail.com"
```

`--local` 값은 현재 Clone의 `.git/config`에만 저장됩니다. GitHub에 Commit되지 않고 다른 Repository에 영향을 주지 않으며, 새 Clone·PC·EC2에서는 다시 설정해야 합니다.

```bash
git remote -v
git branch --show-current
git config --local --get user.name
git config --local --get user.email
git status
```

현재 기대값은 다음과 같습니다.

| 항목 | 값 |
|---|---|
| Repository | `seungsuk-training/janggu-practice-lab` |
| SSH Alias | `github-seungsuk-training` |
| Remote | `git@github-seungsuk-training:seungsuk-training/janggu-practice-lab.git` |
| Branch | `main` |
| Git 작성자 | `Seungsuk Ryoo` |
| Git Email | `seungsuk.training@gmail.com` |

VS Code가 설치되어 있다면 새 창으로 엽니다.

```bash
code --new-window .
```

## 2. SSH Private Key 보안

- `*.pub` Public Key만 GitHub에 등록합니다.
- Private Key를 Git, README, 메신저, 일반 Cloud Storage 또는 AI 작업 보고서에 노출하지 않습니다.
- Private Key 내용을 Terminal 출력, Screenshot 또는 화면 공유에 노출하지 않습니다.
- 임시 PC·EC2마다 새 Key를 만들고, 새 환경에는 기존 Private Key를 복사하기보다 새 Public Key를 등록합니다.
- 백업이 꼭 필요하면 암호화된 Password Manager 또는 암호화된 Offline 저장소만 사용합니다.
- 가능한 경우 Passphrase를 설정합니다.

## 3. 임시 PC·EC2 폐기

폐기 전에 Public Key Fingerprint로 삭제 대상을 식별합니다.

```bash
ssh-keygen -lf ~/.ssh/id_ed25519_seungsuk_training.pub
```

1. GitHub의 `Settings → SSH and GPG keys`에서 해당 환경의 Key 등록을 해제합니다.
2. 같은 Key를 사용하는 다른 Repository나 작업이 없는지 확인합니다.
3. PC를 계속 사용할 경우 `~/.ssh/config`에서 해당 Host Block을 제거합니다.
4. PC를 계속 사용할 경우에만 확인 Prompt가 있는 명령으로 Local Key Pair를 삭제합니다.

```bash
rm -i ~/.ssh/id_ed25519_seungsuk_training
rm -i ~/.ssh/id_ed25519_seungsuk_training.pub
```

EC2 자체를 폐기한다면 인스턴스 종료 전에 GitHub 등록 Key부터 삭제합니다. 실제 삭제 전 파일 경로와 Fingerprint를 확인하고 다른 Alias가 사용하는 Key는 삭제하지 않습니다.

## 4. 문제 해결

### `Permission denied (publickey)`

Alias에 적용되는 공개 가능한 설정만 확인합니다.

```bash
ssh -G github-seungsuk-training \
  | grep -E '^(user|hostname|identityfile|identitiesonly) '
ssh -vT git@github-seungsuk-training
```

다음을 점검합니다.

- `IdentityFile`이 생성한 Private Key 경로와 일치하는가?
- 대응 Public Key를 `seungsuk-training` GitHub 계정에 등록했는가?
- `~/.ssh`는 `700`, Private Key와 `config`는 `600` 권한인가?
- 인증 결과에 표시된 GitHub 계정이 의도한 계정인가?

`ssh -vT` 출력은 공유 전에 사용자명과 Local 경로 등 민감할 수 있는 정보를 검토합니다.

### `Repository not found`

- 인증된 계정이 `seungsuk-training/janggu-practice-lab`에 접근할 수 있는가?
- Remote의 Alias, Owner와 Repository 이름이 정확한가?
- SSH가 다른 GitHub 계정의 Key를 선택하지 않았는가?

```bash
git remote -v
ssh -T git@github-seungsuk-training
```

## 5. 새 환경 확인 Checklist

Repository를 Clone한 실제 경로에서 실행합니다. 아래 경로는 현재 EC2의 경로이며 다른 PC에서는 달라질 수 있습니다.

```bash
cd /home/ubuntu/janggu-practice-lab

git remote -v
git branch --show-current
git config --local --get user.name
git config --local --get user.email
ssh -T git@github-seungsuk-training
git status
```

## 6. Commit Email 공개 참고

Git Commit Email은 Repository History에 포함될 수 있습니다. 현재는 `seungsuk.training@gmail.com`을 사용합니다. 공개를 원하지 않으면 GitHub의 `noreply` Email을 검토한 뒤 새 Commit 전에 Repository-local 설정을 변경합니다.
