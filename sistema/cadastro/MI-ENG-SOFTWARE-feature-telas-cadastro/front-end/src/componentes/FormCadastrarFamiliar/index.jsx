// Este é o arquivo "Página" (index.jsx)
// O main.jsx chama este arquivo.

// Caminho Corrigido:
// De 'src/pages/CadastrarFamiliar/' (onde estamos)
// Subimos 1 nível para 'src/pages/' (../)
// Subimos 1 nível para 'src/' (../../)
// Entramos em 'src/components/' (../../components/)
// Entramos em 'src/components/forms/' (../../components/forms/)
// Pegamos o arquivo: ../../components/forms/FormCadastrarFamiliar
import { FormCadastrarFamiliar } from '../../components/forms/FormCadastrarFamiliar';

// Caminho Corrigido:
// Importa o CSS que está na mesma pasta
import './CadastrarFamiliar.css'; 


// Este é o componente "Página" que o seu main.jsx está importando
export function CadastrarFamiliar() {
  
  return (
    <div className="cadastrar-familiar-pagina">
      
      <main className="pagina-conteudo">
        <h1>Cadastro de Familiar</h1>
        <p>Preencha os dados abaixo para criar uma nova conta.</p>
        
        {/* A Página agora renderiza o Formulário que nós corrigimos */}
        <FormCadastrarFamiliar />

      </main>

    </div>
  );
}