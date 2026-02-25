// Edit comment toggle
document.querySelectorAll('.edit-comment-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        document.querySelector(`.comment-text-${commentId}`).style.display = 'none';
        document.querySelector(`.comment-edit-form-${commentId}`).style.display = 'block';
        this.closest('.btn-group').style.display = 'none';
    });
});

document.querySelectorAll('.cancel-edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        document.querySelector(`.comment-text-${commentId}`).style.display = 'block';
        document.querySelector(`.comment-edit-form-${commentId}`).style.display = 'none';
        document.querySelector('.btn-group').style.display = 'flex';
    });
});
