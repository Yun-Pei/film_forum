import random
from faker import Faker
from member.models import Movies, MovieComments,User

fake = Faker()

movies_ids = Movies.objects.all().values_list("mid", flat=True)

users = User.objects.all()

test_comments_count = 10000

for _ in range(test_comments_count):
    user = random.choice(users)
    movie_id = random.choice(movies_ids)

    if not MovieComments.objects.filter(uid=user, mid_id=movie_id).exists():
        movie = Movies.objects.get(mid=movie_id)

        comment = MovieComments.objects.create(
            uid=user,
            mid=movie,
            content=fake.paragraph(),
            score=random.randint(1, 10),
            time=fake.date_time_this_year(before_now=True, after_now=False)
        )

        comment.save()