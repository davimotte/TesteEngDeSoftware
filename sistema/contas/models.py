from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo', 'admClinica')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPOS = (
        ('admClinica', 'Administrador da Clínica'),
        ('clinica', 'Clínica'),
        ('terapeuta', 'Terapeuta'),
        ('familiar', 'Familiar'),
    )
    
    email = models.EmailField('e-mail', unique=True)
    first_name = models.CharField('nome', max_length=150, blank=True)
    last_name = models.CharField('sobrenome', max_length=150, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='familiar')  # Corrigido para 20
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    telefone = models.CharField(max_length=15, blank=True)  # Adicionado do diagrama
    data_cadastro = models.DateTimeField(default=timezone.now)  # Adicionado do diagrama
    ativo = models.BooleanField(default=True)  # Adicionado do diagrama

    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def __str__(self):
        return f"{self.email} ({self.get_tipo_display()})"

    def clean(self):
        if self.cpf and not self.validar_cpf():
            raise ValidationError({'cpf': 'CPF inválido'})

    def validar_cpf(self):
        # Implementar validação de CPF
        return True


class Endereco(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='endereco')
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    complemento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
    
class Clinica(Usuario):
    usuario_ptr = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="contas_clinica",
        primary_key=True,
    )
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "clínica"
        verbose_name_plural = "clínicas"

    def adicionar_terapeuta(self, terapeuta):
        """Adiciona terapeuta à clínica"""
        pass

    def remover_terapeuta(self, terapeuta):
        """Remove terapeuta da clínica"""
        pass

class AdministradorClinica(Usuario):
    usuario_ptr = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="contas_administrador_clinica",  # Corrigido: related_name único
        primary_key=True,
    )
    cnpj_clinica = models.CharField(max_length=18, null=True, blank=True)  # Renomeado para evitar conflito
    cargo = models.CharField(max_length=100, blank=True)  # Adicionado do diagrama

    class Meta:
        verbose_name = "administrador da clínica"
        verbose_name_plural = "administradores da clínica"

    def cadastrar_terapeuta(self, terapeuta_data):
        """Cadastra novo terapeuta"""
        pass

    def inativar_terapeuta(self, terapeuta):
        """Inativa terapeuta"""
        pass

class Terapeuta(Usuario):
    usuario_ptr = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="contas_terapeuta",
        primary_key=True,
    )
    crp = models.CharField(max_length=20, unique=True, null=True, blank=True)
    especialidade = models.CharField(max_length=100, blank=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.SET_NULL, null=True, blank=True, related_name='terapeutas')

    class Meta:
        verbose_name = "terapeuta"
        verbose_name_plural = "terapeutas"

    def criar_plano_terapeutico(self, paciente, dados_plano):
        """Cria plano terapêutico para paciente"""
        pass

    def visualizar_planos(self):
        """Visualiza todos os planos do terapeuta"""
        return PlanoTerapeutico.objects.filter(terapeuta=self)

class Familiar(Usuario):
    usuario_ptr = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name="contas_familiar",
        primary_key=True,
    )
    parentesco = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "familiar"
        verbose_name_plural = "familiares"

    def registrar_comentario(self, paciente, texto):
        """Registra comentário como feedback"""
        return Feedback.objects.create(
            autor=self,
            paciente=paciente,
            texto=texto,
            tipo_feedback='comentario'
        )

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='paciente')
    data_nascimento = models.DateField()
    neurodivergencia = models.CharField(max_length=100)
    responsaveis = models.ManyToManyField(Familiar, related_name='pacientes_responsaveis', blank=True)
    terapeutas = models.ManyToManyField(Terapeuta, related_name='pacientes_terapeutas', blank=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, related_name='pacientes_vinculados') 

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    def get_plano_terapeutico_ativo(self):
        return self.planos_terapeuticos.filter(ativo=True).first()

    def get_familiares_vinculados(self):
        return self.responsaveis.all()

    def get_terapeutas_responsaveis(self):
        return self.terapeutas.all()

class PlanoTerapeutico(models.Model):
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='planos_terapeuticos')
    titulo = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=True)

    def notificar_atualizacao(self):
        """Notifica sobre atualização do plano"""
        pass

    def desativar_plano(self):
        """Desativa o plano terapêutico"""
        self.ativo = False
        self.save()

class SessaoTerapia(models.Model):
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='sessoes')
    data = models.DateTimeField()
    duracao = models.IntegerField(help_text="Duração em minutos")
    observacao = models.TextField(blank=True)

    def registrar_observacao(self, observacao):
        self.observacao = observacao
        self.save()

class Feedback(models.Model):
    TIPO_FEEDBACK = (
        ('comentario', 'Comentário'),
        ('progresso', 'Relato de Progresso'),
        ('ajuste', 'Sugestão de Ajuste'),
    )
    
    autor = models.ForeignKey(Familiar, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_feedback = models.CharField(max_length=20, choices=TIPO_FEEDBACK)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    resposta = models.TextField(blank=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    terapeuta_resposta = models.ForeignKey(Terapeuta, on_delete=models.SET_NULL, null=True, blank=True)

class Documento(models.Model):
    nome_arquivo = models.CharField(max_length=255)
    caminho_arquivo = models.FileField(upload_to='documentos/')
    tipo = models.CharField(max_length=50)
    tamanho_arquivo = models.IntegerField()
    data_upload = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    def validar_documento(self):
        """Valida tipo e tamanho do documento"""
        tipos_permitidos = ['pdf', 'doc', 'docx', 'jpg', 'png']
        tamanho_maximo = 10 * 1024 * 1024  # 10MB
        
        return (self.tipo in tipos_permitidos and 
                self.tamanho_arquivo <= tamanho_maximo)

class RegistroDiario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='diario')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto_mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    anexos = models.ManyToManyField(Documento, blank=True)

    def adicionar_anexo(self, documento):
        self.anexos.add(documento)

class Checklist(models.Model):
    titulo = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Terapeuta, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='checklists')

    def adicionar_item(self, descricao):
        return ItemChecklist.objects.create(checklist=self, descricao=descricão)

class ItemChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=200)
    concluido = models.BooleanField(default=False)

    def marcar_como_concluido(self):
        self.concluido = True
        self.save()

    def marcar_como_pendente(self):
        self.concluido = False
        self.save()