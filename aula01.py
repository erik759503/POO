# ANTES: Violação de múltiplos princípios
class BibliotecaManager:
    """
    PROBLEMAS EVIDENTES:
    - Viola SRP: uma classe fazendo tudo
    - Alto acoplamento: mudanças afetam toda a classe
    - Baixa coesão: métodos com responsabilidades diferentes
    - Viola OCP: adicionar novos tipos requer modificar a classe
    - Código duplicado (viola DRY)
    - Complexidade desnecessária (viola KISS)
    """
    
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []
    
    def cadastrar_livro(self, titulo, autor, isbn):
        # Validação misturada com lógica de negócio
        if not titulo or len(titulo) < 2:
            print("Título inválido!")
            return False
        
        # Lógica de persistência misturada
        novo_livro = {
            'id': len(self.livros) + 1,
            'titulo': titulo,
            'autor': autor,
            'isbn': isbn,
            'disponivel': True
        }
        self.livros.append(novo_livro)
        
        # Formatação de saída misturada
        print(f"Livro '{titulo}' cadastrado com sucesso!")
        return True
    
    def emprestar_livro(self, livro_id, usuario_id):
        # Busca de livro com lógica duplicada
        livro = None
        for l in self.livros:
            if l['id'] == livro_id:
                livro = l
                break
        
        if not livro:
            print("Livro não encontrado!")
            return False
        
        # Busca de usuário com lógica duplicada
        usuario = None
        for u in self.usuarios:
            if u['id'] == usuario_id:
                usuario = u
                break
        
        if not usuario:
            print("Usuário não encontrado!")
            return False
        
        # Validação de disponibilidade
        if not livro['disponivel']:
            print("Livro não disponível!")
            return False
        
        # Cálculo de data de devolução hardcoded
        from datetime import datetime, timedelta
        data_emprestimo = datetime.now()
        data_devolucao = data_emprestimo + timedelta(days=14)
        
        # Criação do empréstimo
        emprestimo = {
            'id': len(self.emprestimos) + 1,
            'livro_id': livro_id,
            'usuario_id': usuario_id,
            'data_emprestimo': data_emprestimo,
            'data_devolucao': data_devolucao,
            'devolvido': False
        }
        
        self.emprestimos.append(emprestimo)
        livro['disponivel'] = False
        
        print(f"Empréstimo realizado! Devolução: {data_devolucao.strftime('%d/%m/%Y')}")
        return True
    
    def calcular_multa(self, emprestimo_id):
        # Busca com lógica duplicada novamente
        emprestimo = None
        for e in self.emprestimos:
            if e['id'] == emprestimo_id:
                emprestimo = e
                break
        
        if not emprestimo or emprestimo['devolvido']:
            return 0
        
        # Cálculo de multa hardcoded
        from datetime import datetime
        data_atual = datetime.now()
        if data_atual > emprestimo['data_devolucao']:
            dias_atraso = (data_atual - emprestimo['data_devolucao']).days
            multa = dias_atraso * 2.0  # R$ 2,00 por dia
            return multa
        
        return 0
    
    def gerar_relatorio(self):
        # Formatação misturada com lógica de negócio
        print("=== RELATÓRIO DE EMPRÉSTIMOS ===")
        for emp in self.emprestimos:
            livro = None
            for l in self.livros:
                if l['id'] == emp['livro_id']:
                    livro = l
                    break
            
            usuario = None
            for u in self.usuarios:
                if u['id'] == emp['usuario_id']:
                    usuario = u
                    break
            
            status = "Devolvido" if emp['devolvido'] else "Em andamento"
            multa = self.calcular_multa(emp['id'])
            
            print(f"Livro: {livro['titulo'] if livro else 'N/A'}")
            print(f"Usuário: {usuario['nome'] if usuario else 'N/A'}")
            print(f"Status: {status}")
            print(f"Multa: R$ {multa:.2f}")
            print("-" * 30)