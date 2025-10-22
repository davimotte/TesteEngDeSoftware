# Backend de Login e Cadastro (Django)

## Passos
1. Crie e ative um virtualenv.
2. Instale dependências: `pip install -r requirements.txt`
3. Aplique migrações: `python manage.py migrate`
4. Crie superusuário: `python manage.py createsuperuser`
5. Rode o servidor: `python manage.py runserver`
6. Acesse:
   - `/entrar/` (login)
   - `/registrar/` (cadastro)
   - `/cadastro/pacientes/` (endpoint de teste em JSON)
   - `/admin/` (admin)

## Observações
- Usuário customizado em `contas.Usuario` (AUTH_USER_MODEL).
- Idioma e timezone configurados para pt-BR / America/Bahia.
- Banco padrão: SQLite. Altere `DATABASES` em `sistema/settings.py` para PostgreSQL quando necessário.
