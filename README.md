# Space Invaders Clone

Um jogo estilo *Space Invaders* clássico desenvolvido em Python utilizando a biblioteca **Pygame**. O projeto apresenta mecânicas completas de jogo, incluindo sistema de menus, dificuldade progressiva e persistência de pontuação (ranking).

##  Funcionalidades

* **Menu Interativo:** Navegação entre Iniciar Jogo e Placar de Líderes.
* **Sistema de High Scores:** As pontuações são salvas localmente em um arquivo de texto, mantendo um ranking dos melhores jogadores.
* **Dificuldade Progressiva:** O jogo se torna mais difícil a cada fase completada (inimigos mais rápidos e tiros mais frequentes).
* **Mecânicas de Combate:**
    * Barra de vida do jogador.
    * Sistema de colisão preciso (máscaras).
    * Animações de explosão.
* **Entrada de Nome:** O jogador pode digitar seu nome antes de começar para registrar no ranking.

##  Tecnologias Utilizadas

* **Python 3.12.3
* **Pygame** (Gerenciamento gráfico, áudio e input)

##  Estrutura do Projeto

O código foi modularizado para facilitar a manutenção e estudo:

* `main.py`: Arquivo principal, gerencia o loop do jogo e os estados (Menu, Jogo, Game Over).
* `player.py`: Classe da nave do jogador e controles.
* `aliens.py`: Gerenciamento dos inimigos e lógica de movimento em grupo.
* `bullets.py`: Classes para os projéteis (tanto do jogador quanto dos aliens).
* `explosion.py`: Animação de sprites para explosões.
* `score.py`: Lógica de leitura e escrita do arquivo de pontuações (`scores.txt`).
* `settings.py`: Configurações globais (resolução, cores, FPS).
* `utils.py`: Funções auxiliares para texto e carregamento de imagens.

##  Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/galactic-defender.git](https://github.com/seu-usuario/galactic-defender.git)
    cd galactic-defender
    ```

2.  **Crie um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install pygame
    ```

4.  **Execute o jogo:**
    ```bash
    python main.py
    ```

##  Controles

* **Setas (Esquerda/Direita):** Movem a nave.
* **Espaço:** Atira.
* **Mouse:** Navegação nos menus.

---
Desenvolvido para fins de estudo em Programação Orientada a Objetos e lógica de programação.
