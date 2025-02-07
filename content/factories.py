import factory
from models import Content, Rate
from user.factories import UserFactory

class ContentFactory(factory.django.DjangoModelFactory):
    """Factory for creating content."""
    class Meta:
        model = Content

    title = factory.Faker('sentence')
    text = factory.Faker('paragraph')
    user = factory.SubFactory(UserFactory)

class RateFactory(factory.django.DjangoModelFactory):
    """Factory for creating ratings."""
    class Meta:
        model = Rate

    score = factory.Iterator([1, 2, 3, 4, 5])
    post = factory.SubFactory(ContentFactory)
    user = factory.SubFactory(UserFactory)
