from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

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
