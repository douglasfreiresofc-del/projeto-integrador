from datetime import datetime
import tkinter as tk
from tkinter import messagebox

atividades = []
FUNDO, VERDE, BORDA = "#2d323b", "#cce8d6", "#9bc9ad"
CINZA, PRETO, BOLD_FG = "#f3f4f6", "#111827", "#0b2416"
F_TIT, F_SEC, F_BOLD, F_TXT, F_MIN = ("Segoe UI", 14, "bold"), ("Segoe UI", 10, "bold"), ("Segoe UI", 10, "bold"), ("Segoe UI", 10), ("Segoe UI", 9)


def analisar_prazo(data_txt, concluida):
    if concluida or not data_txt or data_txt == "Não informada":
        return ("Concluída" if concluida else "Pendente"), "", "normal"
    try:
        dias = (datetime.strptime(data_txt, "%d/%m/%Y").date() - datetime.now().date()).days
        if dias < 0:
            return "Pendente", f"PRAZO VENCIDO há {abs(dias)} dia(s)!", "critico"
        if dias == 0:
            return "Pendente", "ENTREGA É HOJE!", "critico"
        if dias <= 3:
            return "Pendente", f"PRAZO ACABANDO: faltam {dias} dia(s)!", "aviso"
        return "Pendente", f"Dentro do prazo ({dias} dias restantes)", "ok"
    except ValueError:
        return "Pendente", "Data inválida — use DD/MM/AAAA", "aviso"


def set_texto(caixa, texto, cor=PRETO):
    caixa.config(state="normal", fg=cor)
    caixa.delete("1.0", tk.END)
    caixa.insert(tk.END, texto)
    caixa.config(state="disabled")


def atualizar_tela(nome):
    lbl_hoje.config(text=f"Hoje: {datetime.now().date().strftime('%d/%m/%Y')}")
    alertas, nivel_geral = [], "ok"
    for a in atividades:
        _, msg, niv = analisar_prazo(a["data"], a["concluida"])
        if niv in ("critico", "aviso"):
            alertas.append(f"• {a['materia']} — {a['atividade']} ({a['data']}): {msg}")
            if niv == "critico" or (niv == "aviso" and nivel_geral != "critico"):
                nivel_geral = niv
    cor_alerta = "#b91c1c" if nivel_geral == "critico" else ("#b45309" if nivel_geral == "aviso" else PRETO)
    set_texto(txt_alertas, "\n".join(alertas) if alertas else "Tudo em dia — nenhuma atividade vencida, para hoje ou nos próximos 3 dias.", cor_alerta)

    linhas = [f"Estudante: {nome or 'Não informado'}   |   Total de atividades: {len(atividades)}", "─" * 68, ""]
    if not atividades:
        linhas.append("Nenhuma atividade cadastrada ainda.")
    for a in atividades:
        st, msg, _ = analisar_prazo(a["data"], a["concluida"])
        linhas.append(f"▸ {a['materia']} — {a['atividade']}\n  Entrega: {a['data']} às {a['hora']}  |  Status: {st}{f'  [{msg}]' if msg else ''}\n  Obs: {a['obs']}\n")
    set_texto(txt_resumo, "\n".join(linhas), PRETO)


def adicionar():
    materia, ativ = entry_materia.get().strip(), entry_atividade.get().strip()
    if not materia or not ativ:
        return messagebox.showwarning("Atenção", "Preencha Matéria e Atividade / Projeto.")
    atividades.append({
        "materia": materia, "atividade": ativ,
        "data": entry_data.get().strip() or "Não informada",
        "hora": entry_hora.get().strip() or "Não informado",
        "obs": text_obs.get("1.0", tk.END).strip() or "Sem observações",
        "concluida": var_concluida.get(),
    })
    for c in (entry_materia, entry_atividade, entry_data, entry_hora):
        c.delete(0, tk.END)
    text_obs.delete("1.0", tk.END)
    var_concluida.set(False)
    atualizar_tela(entry_nome.get().strip())


def bloco(parent, pady=(0, 12), expand=False):
    cv = tk.Canvas(parent, bg=FUNDO, highlightthickness=0, bd=0)
    cv.pack(fill="both" if expand else "x", expand=expand, padx=18, pady=pady)
    inner = tk.Frame(cv, bg=VERDE)
    wid = cv.create_window(16, 14, anchor="nw", window=inner)

    def resize(e=None):
        w = max(cv.winfo_width(), 200)
        h = max(cv.winfo_height(), inner.winfo_reqheight() + 28, 160) if expand else max(inner.winfo_reqheight() + 28, 80)
        if not expand:
            cv.config(height=h)
        r = 22
        pts = [w - r, 2, w - 2, 2, w - 2, r, w - 2, h - r, w - 2, h - 2, w - r, h - 2, r, h - 2, 2, h - 2, 2, h - r, 2, r, 2, 2, r, 2]
        cv.delete("bg")
        cv.create_polygon(pts, smooth=True, fill=VERDE, outline=BORDA, width=2, tags="bg")
        cv.tag_lower("bg")
        cv.itemconfig(wid, width=max(w - 32, 160), **({"height": max(h - 28, 100)} if expand else {}))

    cv.bind("<Configure>", resize)
    inner.bind("<Configure>", resize)
    return inner


def lbl(parent, texto, fonte=F_BOLD):
    return tk.Label(parent, text=texto, font=fonte, bg=VERDE, fg=BOLD_FG)


def campo_entry(parent, row, texto, width=42):
    lbl(parent, texto).grid(row=row, column=0, sticky="w", pady=4, padx=(0, 10))
    e = tk.Entry(parent, width=width, font=F_TXT, bg=CINZA, fg=PRETO, insertbackground=PRETO, relief="flat")
    e.grid(row=row, column=1, sticky="w", pady=4)
    return e


def caixa_txt(parent, h, fonte=F_MIN, edit=False):
    t = tk.Text(parent, height=h, font=fonte, bg=CINZA, fg=PRETO, insertbackground=PRETO, relief="flat", bd=0, state="normal" if edit else "disabled")
    if not edit:
        t.pack(fill="both" if h >= 8 else "x", expand=h >= 8)
    return t


janela = tk.Tk()
janela.title("MY ORGANIZER")
janela.geometry("640x800")
janela.minsize(600, 740)
janela.configure(bg=FUNDO)

topo = tk.Frame(janela, bg=FUNDO)
topo.pack(fill="x", padx=18, pady=(14, 6))
tk.Label(topo, text="MY ORGANIZER", font=F_TIT, bg=FUNDO, fg="#e5e7eb").pack(side="left")
lbl_hoje = tk.Label(topo, text="", font=F_MIN, bg=FUNDO, fg="#cbd5e1")
lbl_hoje.pack(side="right", pady=4)

form = bloco(janela, pady=(4, 12))
entry_nome = campo_entry(form, 0, "Seu nome:")
entry_materia = campo_entry(form, 1, "Matéria:")
entry_atividade = campo_entry(form, 2, "Atividade / Projeto:")
entry_data = campo_entry(form, 3, "Data (DD/MM/AAAA):", width=20)
entry_hora = campo_entry(form, 4, "Horário:", width=20)

lbl(form, "Observação:").grid(row=5, column=0, sticky="nw", pady=4, padx=(0, 10))
text_obs = caixa_txt(form, h=2, fonte=F_TXT, edit=True)
text_obs.config(width=42)
text_obs.grid(row=5, column=1, sticky="w", pady=4)

var_concluida = tk.BooleanVar()
tk.Checkbutton(form, text="Atividade já foi concluída", variable=var_concluida, font=F_BOLD, bg=VERDE, fg=BOLD_FG, activebackground=VERDE, activeforeground=BOLD_FG, selectcolor=CINZA).grid(row=6, column=1, sticky="w", pady=(4, 8))

area_btn = tk.Frame(form, bg=VERDE)
area_btn.grid(row=7, column=0, columnspan=2, pady=(4, 2))
tk.Button(area_btn, text="Cadastrar Atividade", command=adicionar, bg=PRETO, fg="#22c55e", activebackground="#1f2937", activeforeground="#22c55e", font=F_BOLD, relief="flat", cursor="hand2", padx=26, pady=8).pack(anchor="center")

b_alertas = bloco(janela, pady=(0, 12))
lbl(b_alertas, "Alertas de Prazo", F_SEC).pack(anchor="w", pady=(0, 4))
txt_alertas = caixa_txt(b_alertas, h=3)

b_resumo = bloco(janela, pady=(0, 16), expand=True)
lbl(b_resumo, "Resumo das Atividades", F_SEC).pack(anchor="w", pady=(0, 4))
txt_resumo = caixa_txt(b_resumo, h=8)

atualizar_tela("")
janela.mainloop()