# 🚀 Minerador Automático de Minecraft 🤖⛏️

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)
![Minecraft](https://img.shields.io/badge/Minecraft-Bedrock%20Edition-red)

Um bot inteligente que automatiza a mineração no Minecraft Bedrock Edition utilizando visão computacional e movimentação otimizada em espiral.

---

## ✨ Funcionalidades

- **Detecção Inteligente de Minérios**  
  ![Detecção](https://img.shields.io/badge/Detecção-Diamante%20|%20Ferro%20|%20Ouro-yellow.svg)  
  Identifica automaticamente diamante, ferro, ouro e outros minérios usando OpenCV.

- **Gerenciamento de Picaretas**  
  ![Picaretas](https://img.shields.io/badge/Gerenciamento-Troca%20Automática%20de%20Picaretas-orange.svg)  
  Troca para outra picareta quando a atual está prestes a quebrar.

- **Sistema de Segurança** *(opcional)*  
  ![Segurança](https://img.shields.io/badge/Segurança-Detecção%20de%20Perigos-red.svg)  
  Evita lava, buracos e outros perigos no ambiente (pode ser desativado).

- **Mapeamento 3D e Navegação**  
  ![Mapeamento](https://img.shields.io/badge/Navegação-Padrão%20Espiral-blue.svg)  
  Cobre grandes áreas com eficiência em movimento espiral descendente.

---

## 📥 Instalação

Clone o repositório:

```bash
git git@github.com:CodexMelo/Bot-de-Minera-o-Autom-tica-no-Minecraft-Bedrock.git
cd Bot-de-Minera-o-Autom-tica-no-Minecraft-Bedrock
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Requisitos:

- Python 3.8+
- Minecraft Bedrock Edition
- Bibliotecas Python:
  ```
  opencv-python
  numpy
  mss
  keyboard
  pyautogui
  pydirectinput
  pillow
  ```

---

## ⚙️ Configuração

1. **Organização da Hotbar:**
   ```
   Slot 1: Picareta de Diamante
   Slot 2: Picareta de Ferro
   Slot 3: Picareta de Pedra
   Slot 4: Picareta de Madeira
   ```

2. **Configurações no `config.py`:**

```python
# Parâmetros de mineração
DIAMETRO = 100      # Diâmetro da espiral
PROFUNDIDADE = 5    # Quantidade de camadas
TECLA_INICIAR = 'c' # Tecla para começar
TECLA_PARAR = 'v'   # Tecla de emergência

# Cores dos minérios (BGR)
MINERIOS = {
    'diamante': {'min': (200, 150, 50), 'max': (255, 200, 100)},
    'ferro': {'min': (60, 80, 120), 'max': (100, 120, 180)},
}
```

---

## 🎮 Como Usar

Execute:

```bash
python main.py
```

Controles:

- Posicione o personagem na parede inicial.
- Pressione `TECLA_INICIAR` (`c` por padrão) para começar.
- Pressione `TECLA_PARAR` (`v` por padrão) para interromper.

---

## ⚡ Recursos Avançados

Exemplo de padrão de varredura em espiral:

```python
PADRAO_ESPIRAL = [
    (0, 0), (0, 30), (30, 30), (30, 0),
    (30, -30), (0, -30), (-30, -30), (-30, 0), (-30, 30),
    (0, 60), (45, 45), (60, 0), (45, -45),
    (0, -60), (-45, -45), (-60, 0), (-45, 45)
]
```

---

## 📊 Desempenho

| Configuração de FOV | Precisão | Área Coberta |
|:-------------------:|:--------:|:------------:|
| 60-70               | ⭐⭐⭐⭐    | ⭐⭐          |
| 80-90               | ⭐⭐⭐     | ⭐⭐⭐        |
| 100+                | ⭐⭐      | ⭐⭐⭐⭐      |

**Recomendação:**  
Utilizar FOV entre **80 e 90** para melhor equilíbrio entre precisão e alcance.

---

## 🤝 Como Contribuir

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b feature/NovaFuncionalidade`).
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Push para sua branch (`git push origin feature/NovaFuncionalidade`).
5. Abra um Pull Request!

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Consulte o arquivo `LICENSE` para mais informações.

---

## 📧 Contato

Projeto desenvolvido por **CODEX MELO**.  
GitHub: [https://github.com/CodexMelo/Bot-de-Minera-o-Autom-tica-no-Minecraft-Bedrock#](https://github.com/CodexMelo/Bot-de-Minera-o-Autom-tica-no-Minecraft-Bedrock#)
