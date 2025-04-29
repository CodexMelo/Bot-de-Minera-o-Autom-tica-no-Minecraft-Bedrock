🛠️ Bot de Mineração Automática no Minecraft Bedrock
Este projeto é um bot inteligente para minerar automaticamente em espiral no Minecraft Bedrock Edition, utilizando:

Detecção de minérios

Mineração otimizada

Controle automático de ferramentas (picaretas)

Navegação e movimentação automáticas

📋 Funcionalidades
Mineração em Espiral: cava seguindo um padrão em espiral para máxima eficiência.

Detecção Inteligente de Minérios: prioriza minérios raros (diamante, esmeralda, ouro, etc.).

Seleção automática de picareta: troca de ferramenta conforme o minério detectado.

Controle da mira: após detectar e minerar, o bot sempre centraliza novamente a mira.

Mineração Adjacente: após andar, minera blocos ao redor (em cima, na frente e embaixo).

Pausa e Cancelamento: pode ser pausado pressionando uma tecla configurada.

⚙️ Requisitos
Python 3.10 ou superior

Bibliotecas Python:

pyautogui

pydirectinput

keyboard

opencv-python

numpy

Minecraft Bedrock (resolução fixa da tela para capturas corretas)

🚀 Como usar
Instale as dependências:

bash
Copiar
Editar
pip install pyautogui pydirectinput keyboard opencv-python numpy
Configure os parâmetros principais no seu script:

TECLA_PARAR (ex: "v")

TEMPO_QUEBRAR_BLOCO (tempo base para minerar)

DIAMETRO (largura da espiral)

Execute o bot com:

bash
Copiar
Editar
python bot_mineracao.py
Dentro do jogo:

Posicione-se no centro da área de mineração.

Comece o script.

O bot começará a minerar automaticamente!

🎯 Principais Funções

Função	Descrição
cavar_espiral()	Cava em espiral, detectando e minerando minérios prioritários.
verificar_minerio()	Detecta o minério que está na frente da mira usando visão computacional (YOLO/Template Matching).
minerar_adjacentes()	Minera blocos à frente, em cima e embaixo do jogador.
selecionar_picareta_por_tipo(tipo)	Troca automaticamente para a picareta correta.
📸 Imagens e Detecção
O bot usa captura de tela (pyautogui.screenshot) para identificar minérios no campo de visão.
Modelos de minérios (templates) devem estar em uma pasta do projeto, organizados por nome.

⚠️ Avisos
Resolução da Tela: o bot foi calibrado para resoluções específicas. Pode ser necessário ajustar se seu monitor for diferente.

Minecraft Configurações:

FOV padrão

Sensibilidade fixa

Sem shaders ou texturas que mudem aparência dos minérios

Uso Ético: este bot é para uso pessoal e estudo. Não utilize em servidores públicos sem permissão.

💻 Organização dos Arquivos
Copiar
Editar
bot_mineracao/
├── templates/
│   ├── diamante.png
│   ├── esmeralda.png
│   └── ...
├── bot_mineracao.py
├── README.md
└── requirements.txt
✨ Créditos
Desenvolvido com paixão por VMS DRAGON/ Codex Melo! ⛏️
Ideal para quem quer automatizar tarefas repetitivas e aprender sobre automação no Minecraft.
