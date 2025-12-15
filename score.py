import os

SCORES_FILE = "scores.txt"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    entries = []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                name, score = line.strip().split(";")
                entries.append((name, int(score)))
            except:
                pass
    # ordenar por pontuação (maior primeiro)
    entries.sort(key=lambda x: x[1], reverse=True)
    return entries


def save_score(player_name, score):
    entries = load_scores()
    updated = False

    # se já existe o nome → atualiza score apenas se for maior
    for i, (name, s) in enumerate(entries):
        if name == player_name:
            if score > s:
                entries[i] = (name, score)
            updated = True
            break

    # se o nome ainda não existe → adiciona
    if not updated:
        entries.append((player_name, score))

    # ordenar novamente
    entries.sort(key=lambda x: x[1], reverse=True)

    # salvar
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        for name, s in entries:
            f.write(f"{name};{s}\n")
