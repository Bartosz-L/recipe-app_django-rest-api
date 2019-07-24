from rest_framework.generics import CreateAPIView
from user.serializers import UserSerializer
# Create your views here.


class CreateUserView(CreateAPIView):
    # create a new user in the system
    serializer_class = UserSerializer
