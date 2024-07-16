from celery import shared_task

from posts.services import generate_comment_answer
from posts.models import Comment


@shared_task
def answer_comment(comment_id, post_title, post_content, comment_content):
    answer = generate_comment_answer(post_title, post_content, comment_content)
    answer_to_comment = Comment.objects.filter(id=comment_id).select_related('post').get()
    Comment.objects.create(
        user_id=answer_to_comment.post.user_id,
        post_id=answer_to_comment.post_id,
        answer_to_id=answer_to_comment.id,
        content=answer,
        auto_generated=True
    )
