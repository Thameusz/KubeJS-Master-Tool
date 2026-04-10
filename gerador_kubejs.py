import tkinter as tk
from tkinter import ttk, messagebox

# --- CONFIGURAÇÕES DE ESTILO ---
BG_COLOR = "#1e1e1e"
SECONDARY_BG = "#2d2d2d"
FG_COLOR = "#e0e0e0"
ACCENT_GREEN = "#43a047"
ACCENT_ORANGE = "#f39c12"
ACCENT_BLUE = "#1e88e5"
ACCENT_PURPLE = "#8e24aa"
ACCENT_RED = "#e53935"
FONT_BOLD = ("Segoe UI", 10, "bold")

def copy_to_clipboard(txt):
    root.clipboard_clear()
    root.clipboard_append(txt)
    messagebox.showinfo("KubeJS", "Código copiado com sucesso!")

def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

def create_styled_entry(parent, width=30):
    return tk.Entry(parent, width=width, bg=SECONDARY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")

def create_title(text, color):
    tk.Label(content_frame, text=text, bg=BG_COLOR, fg=color, font=FONT_BOLD).pack(pady=15)

# --- FUNÇÕES DAS TELAS ---

def show_shaped():
    clear_frame()
    create_title("RECEITA SHAPED (BANCADA)", ACCENT_GREEN)
    grid = [[" " for _ in range(3)] for _ in range(3)]
    
    header = tk.Frame(content_frame, bg=BG_COLOR); header.pack(pady=5)
    tk.Label(header, text="Output:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
    out_e = create_styled_entry(header, 25); out_e.pack(side="left", padx=5)
    tk.Label(header, text="Qtd:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
    qty_e = create_styled_entry(header, 5); qty_e.insert(0, "1"); qty_e.pack(side="left")

    g_frame = tk.Frame(content_frame, bg=SECONDARY_BG, padx=10, pady=10); g_frame.pack(pady=10)
    buttons = [[None for _ in range(3)] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            def toggle(row=r, col=c):
                opts = [" ", "A", "B", "C", "D"]
                val = opts[(opts.index(grid[row][col]) + 1) % 5]
                grid[row][col] = val
                buttons[row][col].config(text=val)
            b = tk.Button(g_frame, text=" ", width=4, height=2, bg=BG_COLOR, fg=FG_COLOR, font=FONT_BOLD, relief="flat", command=toggle)
            b.grid(row=r, column=c, padx=2, pady=2)
            buttons[r][c] = b

    m_frame = tk.Frame(content_frame, bg=BG_COLOR); m_frame.pack()
    entries = {}
    for i, char in enumerate(["A", "B", "C", "D"]):
        f = tk.Frame(m_frame, bg=BG_COLOR); f.grid(row=i//2, column=i%2, padx=10, pady=5)
        tk.Label(f, text=f"{char}:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        entries[char] = create_styled_entry(f, 15); entries[char].pack(side="left", padx=2)

    def generate():
        rows = [f"'{grid[r][0]}{grid[r][1]}{grid[r][2]}'" for r in range(3)]
        items = [f"{k}: '{v.get()}'" for k, v in entries.items() if any(k in r for r in grid) and v.get()]
        copy_to_clipboard(f"  event.shaped(Item.of('{out_e.get()}', {qty_e.get()}), [{', '.join(rows)}], {{{', '.join(items)}}})")

    tk.Button(content_frame, text="GERAR SHAPED", bg=ACCENT_GREEN, fg="white", font=FONT_BOLD, width=25, command=generate).pack(pady=15)

def show_fornalha():
    clear_frame()
    create_title("RECEITA DE FORNALHA", ACCENT_ORANGE)
    f_in = tk.Frame(content_frame, bg=BG_COLOR); f_in.pack(pady=5)
    tk.Label(f_in, text="Input:", bg=BG_COLOR, fg=FG_COLOR, width=10).pack(side="left")
    in_e = create_styled_entry(f_in, 25); in_e.pack(side="left")
    f_out = tk.Frame(content_frame, bg=BG_COLOR); f_out.pack(pady=5)
    tk.Label(f_out, text="Output:", bg=BG_COLOR, fg=FG_COLOR, width=10).pack(side="left")
    out_e = create_styled_entry(f_out, 25); out_e.pack(side="left")
    tk.Button(content_frame, text="GERAR FORNALHA", bg=ACCENT_ORANGE, fg="white", font=FONT_BOLD, width=25, 
              command=lambda: copy_to_clipboard(f"  event.smelting('{out_e.get()}', '{in_e.get()}')")).pack(pady=20)

def show_mixer():
    clear_frame()
    create_title("RECEITA MIXER (CREATE)", ACCENT_PURPLE)
    
    out_f = tk.Frame(content_frame, bg=BG_COLOR); out_f.pack(pady=5)
    tk.Label(out_f, text="Output:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
    out_e = create_styled_entry(out_f, 25); out_e.pack(side="left", padx=5)

    ing_container = tk.Frame(content_frame, bg=BG_COLOR); ing_container.pack(fill="x", pady=5)
    ings = []

    def add_ing():
        f = tk.Frame(ing_container, bg=SECONDARY_BG, pady=2); f.pack(fill="x", pady=1)
        tag_v = tk.BooleanVar()
        tk.Checkbutton(f, text="#", variable=tag_v, bg=SECONDARY_BG, fg=ACCENT_PURPLE, selectcolor=BG_COLOR).pack(side="left")
        e = create_styled_entry(f, 30); e.pack(side="left", padx=5)
        tk.Button(f, text="X", bg=ACCENT_RED, fg="white", command=lambda: [f.destroy(), ings.remove(d)]).pack(side="right")
        d = {'e': e, 't': tag_v}
        ings.append(d)

    for _ in range(2): add_ing()
    tk.Button(content_frame, text="➕ Adicionar Ingrediente", bg=SECONDARY_BG, fg=FG_COLOR, command=add_ing).pack(pady=5)

    # --- RE-ADICIONADO: HEAT REQUIREMENT ---
    heat_f = tk.Frame(content_frame, bg=BG_COLOR); heat_f.pack(pady=10)
    tk.Label(heat_f, text="Requisito de Calor:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left", padx=5)
    heat_v = tk.StringVar(value="none")
    heat_cb = ttk.Combobox(heat_f, textvariable=heat_v, values=["none", "heated", "superheated"], state="readonly", width=15)
    heat_cb.pack(side="left")

    def generate():
        items = [f"'{'#' if i['t'].get() else ''}{i['e'].get()}'" for i in ings if i['e'].get()]
        heat_type = heat_v.get()
        heat_code = ""
        if heat_type == "heated": heat_code = ".heated()"
        elif heat_type == "superheated": heat_code = ".superheated()"
        
        copy_to_clipboard(f"  event.recipes.create.mixing('{out_e.get()}', [{', '.join(items)}]){heat_code}")
    
    tk.Button(content_frame, text="GERAR MIXER", bg=ACCENT_PURPLE, fg="white", font=FONT_BOLD, width=25, command=generate).pack(pady=15)

def show_crusher():
    clear_frame()
    create_title("CONFIGURAÇÃO CRUSHER (CREATE)", ACCENT_BLUE)
    
    f_in = tk.Frame(content_frame, bg=BG_COLOR); f_in.pack(pady=5)
    tag_v = tk.BooleanVar()
    tk.Checkbutton(f_in, text="#", variable=tag_v, bg=BG_COLOR, fg=ACCENT_BLUE, selectcolor=SECONDARY_BG).pack(side="left")
    in_e = create_styled_entry(f_in, 25); in_e.pack(side="left")

    f_p = tk.Frame(content_frame, bg=SECONDARY_BG, padx=10, pady=10); f_p.pack(fill="x", pady=5)
    tk.Label(f_p, text="Principal:", bg=SECONDARY_BG, fg=FG_COLOR).pack(side="left")
    out_p = create_styled_entry(f_p, 15); out_p.pack(side="left", padx=5)
    qty_p = create_styled_entry(f_p, 4); qty_p.insert(0, "1"); qty_p.pack(side="left")
    ch_p = create_styled_entry(f_p, 4); ch_p.insert(0, "1.0"); ch_p.pack(side="left", padx=5)

    sec_f = tk.Frame(content_frame, bg=BG_COLOR)
    tk.Label(sec_f, text="Secundário:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
    out_s = create_styled_entry(sec_f, 15); out_s.pack(side="left", padx=5)
    qty_s = create_styled_entry(sec_f, 4); qty_s.insert(0, "1"); qty_s.pack(side="left")
    ch_s = create_styled_entry(sec_f, 4); ch_s.insert(0, "0.5"); ch_s.pack(side="left", padx=5)

    def toggle_sec():
        if sec_f.winfo_viewable():
            sec_f.pack_forget()
            btn_sec.config(text="➕ Adicionar Secundário")
        else:
            sec_f.pack(fill="x", pady=5)
            btn_sec.config(text="➖ Remover Secundário")

    btn_sec = tk.Button(content_frame, text="➕ Adicionar Secundário", bg=SECONDARY_BG, fg=FG_COLOR, command=toggle_sec)
    btn_sec.pack(pady=5)

    def generate():
        inp = f"{'#' if tag_v.get() else ''}{in_e.get()}"
        res = [f"Item.of('{out_p.get()}', {qty_p.get()}).withChance({ch_p.get()})"]
        if sec_f.winfo_viewable() and out_s.get():
            res.append(f"Item.of('{out_s.get()}', {qty_s.get()}).withChance({ch_s.get()})")
        copy_to_clipboard(f"  event.recipes.create.crushing([{', '.join(res)}], '{inp}')")

    tk.Button(content_frame, text="GERAR CRUSHER", bg=ACCENT_BLUE, fg="white", font=FONT_BOLD, width=25, command=generate).pack(pady=15)

def show_deployer():
    clear_frame()
    create_title("RECEITA DEPLOYER", ACCENT_ORANGE)
    f1 = tk.Frame(content_frame, bg=BG_COLOR); f1.pack(pady=2)
    tk.Label(f1, text="Item Base:", bg=BG_COLOR, fg=FG_COLOR, width=12).pack(side="left")
    in_e = create_styled_entry(f1, 25); in_e.pack(side="left")
    f2 = tk.Frame(content_frame, bg=BG_COLOR); f2.pack(pady=2)
    tk.Label(f2, text="Ferramenta:", bg=BG_COLOR, fg=FG_COLOR, width=12).pack(side="left")
    tool_e = create_styled_entry(f2, 25); tool_e.pack(side="left")
    f3 = tk.Frame(content_frame, bg=BG_COLOR); f3.pack(pady=2)
    tk.Label(f3, text="Resultado:", bg=BG_COLOR, fg=FG_COLOR, width=12).pack(side="left")
    out_e = create_styled_entry(f3, 25); out_e.pack(side="left")
    tk.Button(content_frame, text="GERAR DEPLOYER", bg=ACCENT_ORANGE, fg="white", font=FONT_BOLD, width=25, 
              command=lambda: copy_to_clipboard(f"  event.recipes.create.deploying('{out_e.get()}', ['{in_e.get()}', '{tool_e.get()}'])")).pack(pady=20)

def show_sequenced():
    clear_frame()
    create_title("SEQUENCED ASSEMBLY", ACCENT_ORANGE)
    
    form_frame = tk.Frame(content_frame, bg=BG_COLOR)
    form_frame.pack(pady=5, fill="x")

    def add_form_row(label_text, default_val=""):
        row = tk.Frame(form_frame, bg=BG_COLOR)
        row.pack(fill="x", pady=3)
        lbl = tk.Label(row, text=label_text, bg=BG_COLOR, fg=FG_COLOR, width=18, anchor="w")
        lbl.pack(side="left")
        ent = create_styled_entry(row, 35)
        ent.insert(0, default_val)
        ent.pack(side="left", padx=5)
        return ent

    out_e = add_form_row("Output Final:")
    trans_e = add_form_row("Transitional:")
    in_e = add_form_row("Input Item:")
    loop_e = add_form_row("Quantidade Loops:", "5")

    fail_v = tk.BooleanVar()
    tk.Checkbutton(content_frame, text="Habilitar Chance de Falha?", variable=fail_v, bg=BG_COLOR, fg=ACCENT_ORANGE, 
                   command=lambda: fail_panel.pack(pady=10, fill="x") if fail_v.get() else fail_panel.pack_forget(), 
                   selectcolor=SECONDARY_BG, font=("Segoe UI", 9)).pack(pady=5)
    
    fail_panel = tk.Frame(content_frame, bg=SECONDARY_BG, padx=10, pady=10)
    
    row_ch = tk.Frame(fail_panel, bg=SECONDARY_BG); row_ch.pack(fill="x", pady=2)
    tk.Label(row_ch, text="Chance Sucesso:", bg=SECONDARY_BG, fg=FG_COLOR, width=15, anchor="w").pack(side="left")
    ch_e = create_styled_entry(row_ch, 10); ch_e.insert(0, "0.8"); ch_e.pack(side="left", padx=5)
    
    row_jk = tk.Frame(fail_panel, bg=SECONDARY_BG); row_jk.pack(fill="x", pady=2)
    tk.Label(row_jk, text="Item Falha:", bg=SECONDARY_BG, fg=FG_COLOR, width=15, anchor="w").pack(side="left")
    junk_e = create_styled_entry(row_jk, 30); junk_e.insert(0, "create:incomplete_precision_mechanism"); junk_e.pack(side="left", padx=5)

    tk.Label(content_frame, text="PASSOS DA SEQUÊNCIA:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 9, "bold")).pack(pady=(15, 5))
    steps_cont = tk.Frame(content_frame, bg=BG_COLOR); steps_cont.pack(fill="x")
    steps = []

    def add_s():
        f = tk.Frame(steps_cont, bg=SECONDARY_BG, pady=2)
        f.pack(fill="x", pady=2)
        v = tk.StringVar(value="Deploying")
        cb = ttk.Combobox(f, textvariable=v, values=["Deploying", "Pressing", "Filling", "Cutting (Saw)", "Energizing"], width=15, state="readonly")
        cb.pack(side="left", padx=5)
        e = create_styled_entry(f, 25)
        e.pack(side="left", padx=5)
        tk.Button(f, text="X", bg=ACCENT_RED, fg="white", relief="flat", command=lambda: [f.destroy(), steps.remove(d)]).pack(side="right", padx=5)
        d = {'t': v, 'i': e, 'f': f}; steps.append(d)
    
    for _ in range(2): add_s()
    tk.Button(content_frame, text="➕ Adicionar Passo", bg=SECONDARY_BG, fg=FG_COLOR, relief="flat", command=add_s).pack(pady=5)

    def generate():
        out_str = f"Item.of('{out_e.get()}').withChance({ch_e.get()}), '{junk_e.get()}'" if fail_v.get() else f"'{out_e.get()}'"
        step_code = []
        for s in steps:
            t, val, tr = s['t'].get(), s['i'].get(), trans_e.get()
            if t == "Deploying": step_code.append(f"event.recipes.create.deploying('{tr}', ['{tr}', '{val}'])")
            elif t == "Pressing": step_code.append(f"event.recipes.create.pressing('{tr}', '{tr}')")
            elif t == "Filling": step_code.append(f"event.recipes.create.filling('{tr}', ['{tr}', Fluid.of('{val}', 250)])")
            elif t == "Cutting (Saw)": step_code.append(f"event.recipes.create.cutting('{tr}', '{tr}')")
            elif t == "Energizing": step_code.append(f"event.recipes.create_new_age.energizing('{tr}', '{tr}', {val})")
        copy_to_clipboard(f"  event.recipes.create.sequenced_assembly([{out_str}], '{in_e.get()}', [{', '.join(step_code)}]).transitionalItem('{trans_e.get()}').loops({loop_e.get()})")

    tk.Button(content_frame, text="GERAR SEQUENCED ASSEMBLY", bg=ACCENT_ORANGE, fg="white", font=FONT_BOLD, width=30, command=generate).pack(pady=20)

def show_remove():
    clear_frame()
    create_title("REMOVER RECEITA", ACCENT_RED)
    tk.Label(content_frame, text="ID da Receita:", bg=BG_COLOR, fg=FG_COLOR).pack()
    id_e = create_styled_entry(content_frame, 40); id_e.pack(pady=10)
    tk.Button(content_frame, text="GERAR REMOÇÃO", bg=ACCENT_RED, fg="white", font=FONT_BOLD, width=25, 
              command=lambda: copy_to_clipboard(f"  event.remove({{ id: '{id_e.get()}' }})")).pack(pady=20)

# --- MAIN ---
root = tk.Tk(); root.title("KubeJS Tool"); root.geometry("750x850"); root.config(bg=BG_COLOR)
nav = tk.Frame(root, bg=SECONDARY_BG); nav.pack(side="top", fill="x")
menu = [("Shaped", show_shaped), ("Fornalha", show_fornalha), ("Mixer", show_mixer), ("Crusher", show_crusher), ("Deployer", show_deployer), ("Sequenced", show_sequenced), ("Remover", show_remove)]
for t, c in menu: tk.Button(nav, text=t, bg=SECONDARY_BG, fg=FG_COLOR, relief="flat", font=FONT_BOLD, padx=8, pady=10, command=c).pack(side="left")
content_frame = tk.Frame(root, bg=BG_COLOR, padx=30, pady=20); content_frame.pack(fill="both", expand=True)
show_shaped()
root.mainloop()