Nutrismart - Sistema de Gestão Nutricional - Guia Completo

📌 Por Que Usar o Nutrismart?  
1. Controle Nutricional Simplificado: Registre refeições, calcule calorias e monitore sua dieta sem complicação.  
2. Dietas Personalizadas: Receba recomendações de alimentos baseadas no seu plano alimentar (Low Carb, Cetogênica, Hiperproteica, Bulking).  
3. Acompanhamento em Tempo Real: Veja seu progresso diário com relatórios de calorias e ranking dos alimentos mais consumidos.  
4. Segurança: Recuperação de senha via perguntas de segurança e dados protegidos.  
5. Suporte Integrado: Tire dúvidas diretamente com administradores do sistema.  

🚀 Passo a Passo para Usar  

1️⃣ Primeiro Acesso  
- Execute o sistema: python main.py (Ou python interface.py para a versão gráfica)  
- Cadastre-se:  
  - Escolha "Cadastrar usuário" no menu  
  - Preencha e-mail, senha, peso, altura, sexo (M/F)  
  - Selecione uma dieta e uma pergunta de segurança  
- Login: Use seu e-mail e senha cadastrados  

2️⃣ Menu do Usuário  
- Registrar Refeição: Digite o nome do alimento e a quantidade (em gramas) - o sistema calcula as calorias  
- Ver Alimentos Recomendados: Receba 4 sugestões baseadas na sua dieta  
- Encerrar o Dia: Veja resumo das calorias consumidas vs. sua meta diária  
- Editar Perfil: Atualize peso, altura ou dieta para recalcular necessidades  
- Suporte: Envie mensagens aos administradores ou veja respostas  

3️⃣ Para Administradores (Senha: admin123)  
- Cadastrar/Alimentos: Adicione novos alimentos com nome e calorias por 100g  
- Ver Usuários: Acesse dados de todos os usuários cadastrados  
- Responder Suporte: Visualize e responda mensagens dos usuários  

💡 Dicas Rápidas  
- Atualize seu peso para cálculos precisos  
- Use o ranking para identificar alimentos mais consumidos  
- Lembretes alertam sobre hidratação e refeições não registradas  

⚠️ Solução de Problemas  
- E-mail já cadastrado: Use recuperação de senha ou cadastre outro e-mail  
- Alimento não encontrado: Peça ao administrador para cadastrá-lo  
- Erro no login: Verifique se CAPS LOCK está ativado  

📌 Por Dentro do Sistema  
- Banco de Dados: Tudo salvo automaticamente no SQLite (nutricao.db)  
- Segurança: Senhas armazenadas de forma direta (em projeto real use criptografia)  
- Offline: Funciona sem internet após instalado  

PROJETO NUTRISMART BY SAULO EDUARDO

BIBLIOTECAS: sqlite3 re datetime random tkinter

FUNÇÕES:
RF000 - CRUD

RF001 - Cadastro de Usuário (Aréa pra cadastro de novos usuários e de login, pede informações como email,senha,altura,peso,sexo e pede pro usuário selecionar qual dieta ele irá querer seguir)

RF002 - Menu interativo usuário e administrador(menu personalizado contando com funções pro usuário e pro administrador onde o usuário pode inserir suas refeições diárias e acompanhar sua interface, o administrador por si só pode acompanhar seus usuários e seus dados e inserir ou excluir alimentos nas listas)

RF003 - Seletor de dieta (Baseado na vontade do usuário, ele irá selecionar um dos tipos de dieta fornecidos pelo aplicativo como sua dieta pessoal para bater a meta (atualização mensal de dados cadastrais), a dieta é escolhida no cadastro)

RF004 - Banco de alimentos (Será feito um registro de refeições válidas em cada dieta, caso o usuario queira adicionar uma refeição que não consta nos registros, irá aparecer uma mensagem de erro pedindo pra que ele peça ao administrador para adicionar tal alimento)

RF005 - Registro de refeições (haverá um histórico que registra as refeições diarias do usuario e a quantidade de cada porção comparada com a recomendada para seguir a dieta)

RF006 - Refeições personalizadas pra cada dieta (Cada dieta escolhida pelo usuário terá suas refeições especificas recomendadas para dar seguimento a dieta corretamente, baseada em recomendações de nutricionistas)

RF007 - Suporte usuário/administrador (Área pra contato direto entre o administrador do programa e o usuario, onde eles podem se comunicar, o usuario pode mandar duvidas e o administrador pode olhar e responde-las, depois o usuario pode ver a resposta)

RF008 - Feedbacks ( Feedbacks diarios,semanais e mensais que variarão de acordo com o compromisso do usuário com a dieta,caso ele esteja seguindo a dieta recomendada ele terá um feedback positivo,caso não esteja, terá um feedback negativo notificando o que faltou na sua dieta)

RF009 - Ranking de alimentos mais consumidos(Opção onde o usuario pode ver os alimentos que ele mais consome na sua dieta em forma de ranking)

RF010- Sugestão de alimentos pro usuario(De acordo com a necessidade do usuario e sua dieta selecionada, o sistema recomenda alguns alimentos que ele pode integrar na sua dieta)

RF011- Notificações personalizadas(Lembretes pro usuario beber agua, e tomar cuidado com coisas da sua dieta)

RF012- CRUD da interface

RF013- Interface gráfica

RF014 - Melhoria nos tratamentos de erro dentro da interface grafica

RF015 - Interligação funções da interface e do terminal
