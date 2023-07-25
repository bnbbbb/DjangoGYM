function handleLikeButtonClick(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const postId = form.getAttribute('data-post-id');
    const likeButton = document.getElementById('like-button');
    const likeCount = document.getElementById('like-count');

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': form.elements.csrfmiddlewaretoken.value,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    })
    .then(response => response.json())
    .then(data => {
        // 좋아요 버튼 텍스트와 클래스를 변경합니다.
        likeButton.classList.toggle('btn-likeliked', data.liked);

        // 좋아요 수를 업데이트합니다.
        likeCount.textContent = data.like_count + '명이 게시물을 좋아합니다.';
    })
    .catch(error => console.error('Error:', error));
}

// 좋아요 버튼에 클릭 이벤트를 추가합니다.
const likeForm = document.getElementById('like-form');
if (likeForm) {
    likeForm.addEventListener('submit', handleLikeButtonClick);
}
