# Choose The GYM
---

## 목차
1. [프로젝트 소개](#1.-프로젝트-소개)
2. [프로젝트 목표](#2.-프로젝트-목표)
3. [기술 스택](#3.-기술-스택)
4. [프로젝트 구조](#4.-프로젝트-구조)
5. [DBModel](#5.-model)
6. [페이지UI](#6.-페이지-ui)
7. [실행화면](#7.-실행화면)

## To Do List
1. ~~게시글 만들기~~(기본적인 수정, 삭제기능)
2. ~~댓글 CRUD~~
3. ~~유저와 프로필~~
4. ~~프로필 수정, 비밀번호 변경~~
5. ~~검색기능 추가~~
6. ~~조회수 기능~~ (기본적인 기능만)
7. 게시글 시간순 정렬
8. ~~프로필 이미지~~
9. ~~css~~
10. 좋아요 구현

## 1. 프로젝트 소개
- 유저는 헬스장게시판에 직접 댓글을 달 수 있습니다.
- 헬스장 주인은 태그를 달면서 관련된 태그로 고객이 검색 가능합니다.
- 회원가입 할 때 address를 추가함으로써 주소기반으로 검색 가능합니다.



## 2. 프로젝트 목표
- 헬스장 소개 어떤 헬스 기구가 있고 편의시설 무엇이 있는지 유저들이 볼 수 있는 플랫폼을 제공
- 헬스장 주인은 게시글을 통해 헬스장 홍보도 가능합니다. 

## 3. 기술 스택

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/Html-E34F26?style=for-the-badge&logo=html5&logoColor=white">


## 4. 프로젝트 구조
- myapp - 프로젝트명
- blog - 앱명
- user - 앱명
- static - css/img/icon 등
```
📦myapp
┣ 📂app
┃ ┣ 📂__pycache__
┣ 📂blog
┃ ┣ 📂migrations
┃ ┃ ┣ 📂__pycache__
┃ ┣ 📂templates
┃ ┃ ┗ 📂blog
┃ ┣ 📂__pycache__
┣ 📂media
┃ ┣ 📂blog
┃ ┣ 📂django-summernote
┃ ┃ ┗ 📂2023-07-20
┃ ┗ 📂user
┣ 📂static
┃ ┣ 📂assets
┃ ┃
┃ ┗  📂css
┣ 📂staticfiles
┃ ┣ 📂admin
┃ ┃ ┣ 📂css
┃ ┃ ┃ ┣ 📂vendor
┃ ┃ ┃ ┃ ┗ 📂select2
┃ ┃ ┣ 📂img
┃ ┃ ┃ ┗  📂gis
┃ ┃ ┗ 📂js
┃ ┃ ┃ ┣ 📂admin
┃ ┃ ┃ ┣ 📂vendor
┃ ┃ ┃ ┃ ┣ 📂jquery
┃ ┃ ┃ ┃ ┣ 📂select2
┃ ┃ ┃ ┃ ┃ ┗ 📂i18n
┃ ┃ ┃ ┃ ┃
┃ ┃ ┗ ┗ ┗ 📂xregexp 
┃ ┣ 📂assets
┃ ┣ 📂css
┃ ┗ 📂summernote
┃ ┃ ┣ 📂font
┃ ┃ ┗  📂lang
┣ 📂templates
┣ 📂user
┃ ┣ 📂migrations
┃ ┃ ┣ 📂__pycache__
┃ ┣ 📂templates
┃ ┃ ┗ 📂user
┃ ┣ 📂__pycache__
┃ ┗ 📂Scripts
┣ 📜db.sqlite3
┣ 📜manage.py
┗ 📜requirements.txt
```
---
## 5. Model
<img src="../readme/model.png" >

## 6. 페이지 UI
- user-profile

<img src="../readme/user_register.png" style="width:300px; height:400px;">
<img src="../readme/user_login.png" style="width:300px; height:400px;">
<img src="../readme/user_password.png" style="width:300px; height:400px;">
<img src="../readme/useredit.png" style="width:300px; height:400px;">
<img src="../readme/userprofile.png" style="width:300px; height:400px;">

- blog-post

<img src="../readme/blog.png" style="width:300px; height:400px;">
<img src="../readme/bloglist.png" style="width:300px; height:400px;">
<img src="../readme/post.png" style="width:300px; height:400px;">

- Markdown으로 변경할 예정입니다.

## 7. 실행화면 
- user-profile

<img src="../readme/join.gif">
<img src="../readme/login.gif">
<img src="../readme/profile.gif">
<img src="../readme/editprofile.gif">

- blog-post

<img src="../readme/post.gif">
<img src="../readme/postdetail.gif.gif">
<img src="../readme/reviewtag.gif">

## 8. 느낀점

### 제일 큰 고비를 준 이미지 업로드
- 개발 과정 1차 고비
    1. 기본적인 이미지 업로드를 위해 models.ImageField 사용
        - 이미지가 올라가지 않는다. 
    2. 단순히 model만 설정해줄게 아니라 settings 설정 필요한걸 알게됨
        - 이미지가 업로드는 되었지만 화면으로 띄우기가 안됨.
        - static과 media에 대해서 다시 공부
    3. request.FILES 추가
        - request.POST 외에도 FILES를 추가해줘야 하는걸 알게됨.
        - 하지만 또 안됐다.
    4. html에서도 enctype="multipart/form-data" 추가가 필요한걸 공부함. 
- 1차 느낀점
    - print문을 찍으면서 어떤 값을 받아오고 object며 querySet이며 어떤 값을 갖는지 알게됨
    - 내 생각이고 코드가 깔끔하지 않지만 if의 중요성?을 알게되었다. 
```python
context = {
            'form':form,
            'imgform':imgform,
            # 'user':user_profile
        }
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.image:
            context['profile_img'] = user_profile.image.url
```
---
- 개발 과정 2차 고비(다중 이미지)
    1. imageField가 아니라 fileField를 사용하면 될까 생각
        - 될꺼 같지만 하지 않았다.
    2. 여러가지 fild를 사용해봤지만 되지 않음.
        - 그래서 생각난게 toast UI 사용 
        - 시간 부족으로 하지 못했다. 
    3. 그래서 summernote로 일단락
- 2차 느낀점
    - 시간제한이 있을 때는 뼈대를 만들고 살을 붙히는걸 몸소 느꼈다. 
    - 아직 주니어라 그런지 코드가 돌고 돈다? 이런느낌을 받았다.
    - 벌써부터 기대된다. 고수의 코딩...

--- 

### 데이터베이스 설계의 중요성
- model 설계에서 시간을 꽤 쏟은거 같다. 바꿨다가 지웠다가. 
- 설계또는 생각이 잘못되어 select 쿼리가 잘 되지 않았다. 
```python
queryset = Post.objects.filter(address__icontains=q | tags__name__icontains=q)
```
- 단순히 | 사용해 둘중 하나가 들어오면 post를 보내줘야겠다. 라고 생각했다.
    - 게시글은 하난데 검색하면 2개가 검색되는 신기한 광경이 눈 앞에 나타나고 말았다. 
    - 해결과정 if와 elif로 카테고리의 값을 get으로 받았고 input으로 받은 값만 전달해주어 정확한 값을 받게 하였다. 
```python
category = request.GET.get('category')
        q = request.GET.get('q')
        
        if not q:  # 검색어가 없는 경우
            queryset = Post.objects.all()  # 모든 게시물
        else:
            # 선택한 카테고리에 따라 필터링
            if category == 'address':
                queryset = Post.objects.filter(address__icontains=q)
            elif category == 'tag':
                queryset = Post.objects.filter(tags__name__icontains=q)
            elif category == 'content':
                queryset = Post.objects.filter(content__icontains=q)
            else:
                queryset = Post.objects.none()
```
---
### 마무리
생각보다 우여곡절한 코드가 많았지만 대표적으로 일단 생각나는건 위에밖에 없다. 다른 작은 에러들은 생각보다 금방 해결되었고, 위에 서술한 내용들이 꽤 오래 시간을 잡아먹어서 기억에 남는거 같다.

백엔드 개발자는 js, css 등 frontend 언어또한 능숙해야 한다는걸 다시한번 느꼈습니다. 

다음은 DRF를 해볼거 같은데 이것 또한 배워야할게 있어 행복하다! 
더 성장할 수 있는 개발자가 되는게 목표입니다. 


