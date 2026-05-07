from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class Login(View):
    """
    Class Based View para autenticação de usuários
    """
    def get(self, request):
        contexto = {}
        return render(request, 'autenticacao.html', contexto)

    def post(self, request):
        # Pegando os dados do formulário de login
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        # Autenticando o usuário
        user = authenticate(request, username=usuario, password=senha)

        # Verificando as credenciais de autenticação fornecidas
        if user is not None:

            # Verifica se o usuário ainda está ativo no sistema
            if user.is_active:
                login(request, user)
                return redirect("/veiculo")
            else:
                return render(request, 'autenticacao.html', {'mensagem': 'Usuário inativo'})
        else:
            return render(request, 'autenticacao.html', {'mensagem': 'Usuário ou senha inválidos'})
        
class Logout(View):
    """
    Class Based View para logout de usuários
    """
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
        
class LoginAPI(ObtainAuthToken):
    """
    Class Based View para autenticação de usuários por meio de API REST
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context= {
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key
        })
