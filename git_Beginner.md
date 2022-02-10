# 초기설정
- 처음 한번만 설정
    1. 누가 커밋 기록을 남겻는지 볼수있도록 이름, 메일 주소만 다르게 하여 동일 하게 입력

        $ git config --global user.name "이름"
        $ git config __global user.email "메일 주소"
        깃허브 닉네임과 깃허브 아이디

    2. 작성자가 올바르게 설정됐는지 확인 가능

        $ git config --global -1
        Or
        $ git config --global --list


# Git 기본 명령어

![image-20220210114422256](git_Beginner.assets/image-20220210114422256.png)



- **Working Directory**(Working Tree)= 일반적인 작업이 일어나는 곳
- **Staging Area**(Index)= 커밋을 위한 파일 및 폴더가 추가되는 곳
- **Repository** = Staging Area에 있던 파일 및 폴더의 변경사항 (Commit)을 저장하는곳
- 위의 순서대로 버전 관리를 수행함

## git init

```

$ git init

```

- 현재 작업 중인 드렉토리를 Git으로 관리한다는 명령어
- .git이라는 숨김 폴더를 생성하고 터미널에서는 master이라고 표기됨
  - 이미 git저장소인 폴더에 또 git 저장소를 중첩하면 안됨
  - master가 있다면 init하면 안된다는 뜻
  - 터미널이 ~인지 확인하기



## git status



`$ git status`

- Working Directory와 Staging Area의 현재 상태를 알려줌
- 상시로 확인하면 마음이 편해짐



![파일의 라이프사이클](https://hphk.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F67719520-a1d8-4cbb-81dd-49dea429a7f4%2FUntitled.png?table=block&id=0e7118f6-1e80-4394-a0a3-56e395eced90&spaceId=daa2d103-3ecd-4519-8c30-4f55e74c7ef4&width=1600&userId=&cache=v2)





## git add



- 뒤에 파일 (a.txt), 폴더(폴더이름), 디렉토리에 속한 파일,폴더 전부(.)을 붙여서 사용함





## git commit



`$ git commit -m "커밋 메세지"`

- **커밋 메세지**는 현재 변경 사항들을 잘 나타낼 수 있도록 의미 있게 작성하는 것을 권장.



## git log



- 옵션
  - `--oneline` : 한 줄로 축약해서 보여줌.
  - `--graph` : 브랜치와 머지 내역을 그래프로 보여줌.
  - `--all` : 현재 브랜치를 포함한 모든 브랜치의 내역을 보여줌.
  - `--reverse` : 커밋 내역의 순서를 반대로 보여줌. (최신이 가장 아래)
  - `-p` : 파일의 변경 내용도 같이 보여줌.
  - `-2` : 원하는 갯수 만큼의 내역을 보여줌. (2 말고 임의의 숫자 사용 가능)





![git 명령어](https://hphk.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fc86c667a-616f-45b6-892e-15da6a3c494e%2FUntitled.png?table=block&id=07cb1049-19ba-49df-a26a-0eb77478eabf&spaceId=daa2d103-3ecd-4519-8c30-4f55e74c7ef4&width=1820&userId=&cache=v2)
