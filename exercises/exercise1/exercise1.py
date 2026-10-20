import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Übung eins zum Kennenlernen von Pytorch und Berechnungsgraphen

    ## Aufgabe 1
    1. Funktion auswählen: y(x)=2sin(x)+sin(7x+3)
    2. Plotten
    3. Beispieldaten vorbereiten
    """)
    return


@app.cell
def _():
    import numpy as np
    import numpy.typing as npt
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.model_selection import train_test_split

    # Definitionsbereich
    x = np.linspace(-2 * np.pi, 2 * np.pi, 2000)

    # Funktion: y(x) = 2*sin(x) + sin(7x + 3)

    def f(x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    	return 2 * np.sin(x) + np.sin(7 * x + 3)

    y = f(x)

    # Zufällte x-Punkte und zugehörige Funktionswerte
    N = 300
    rng = np.random.default_rng(seed=43)
    x_train = np.sort(rng.uniform(-2 * np.pi, 2 * np.pi, N))
    y_train = f(x_train)

    df_samples = pd.DataFrame({"x": x_train, "y": y_train})

    # Plot
    plt.figure(figsize=(10, 4))
    # Plot Funktion
    plt.plot(x, y, color="tab:blue", linewidth=1.5, label=r"$y(x)=2\sin(x)+\sin(7x+3)$")

    # Plot Punkte
    plt.scatter(x_train, y_train, color="red", zorder=3, label="zufällige Punkte")
    plt.vlines(
    	x_train,
    	ymin=y.min() - 0.2,
    	ymax=y_train,
    	colors="red",
    	linestyles="dotted",
    	alpha=0.5,
    )

    # Achsen etwas hübscher machen
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)

    # x-Achse in Vielfachen von π beschriften
    plt.xticks(
    	[-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi],
    	[r"$-2\pi$", r"$-\pi$", r"$0$", r"$\pi$", r"$2\pi$"],
    )

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Wellige Funktion")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return x_train, y_train


@app.cell
def _():
    from graphviz import Digraph

    # ---------- Graph anlegen ----------
    g = Digraph(name="ComputationGraph", format="png")

    # Globale Attribute
    g.attr(rankdir="TB", newrank="true", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="13", color="black", penwidth="1.4")
    g.attr("edge", color="black", arrowsize="0.8", penwidth="1.2")
    g.attr(labelloc="t", fontsize="14")
    g.attr(label="Berechnungsgraph:   y = 2\u00b7sin(x) + sin(7x + 3)")

    # ---------- Stil-Helfer ----------
    VAR_STYLE = dict(
    	shape="ellipse", style="filled", fillcolor="#fff2cc", fontitalic="true"
    )
    PAR_STYLE = dict(shape="ellipse", style="filled,dashed", fillcolor="#f4cccc")
    OP_STYLE = dict(shape="box", style="rounded,filled", fillcolor="#cfe2f3")

    # ---------- Knoten ----------
    g.node("x", **VAR_STYLE)
    g.node("y", **VAR_STYLE)

    g.node("p2", label="2", **PAR_STYLE)
    g.node("p7", label="7", **PAR_STYLE)
    g.node("p3", label="3", **PAR_STYLE)

    g.node("sinL", label="sin", **OP_STYLE)
    g.node("mulL", label="*", **OP_STYLE)
    g.node("mulR", label="*", **OP_STYLE)
    g.node("addR", label="+", **OP_STYLE)
    g.node("sinR", label="sin", **OP_STYLE)
    g.node("addM", label="+", **OP_STYLE)

    # ---------- Kanten (Datenfluss) ----------
    g.edge("x", "sinL")
    g.edge("x", "mulR")
    g.edge("sinL", "mulL")
    g.edge("p2", "mulL")
    g.edge("mulR", "addR")
    g.edge("p7", "mulR")
    g.edge("addR", "sinR")
    g.edge("p3", "addR")
    g.edge("mulL", "addM")
    g.edge("sinR", "addM")
    g.edge("addM", "y")

    # ---------- Horizontale Ebenen (Rang-Gruppen) ----------
    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("x",):
    		s.node(n)

    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("sinL", "mulR"):
    		s.node(n)

    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("mulL", "addR"):
    		s.node(n)

    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("sinR",):
    		s.node(n)

    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("addM",):
    		s.node(n)

    with g.subgraph() as s:
    	s.attr(rank="same")
    	for n in ("y",):
    		s.node(n)

    # ---------- Rendern ----------
    g  # zeigt das Bild inline in Jupyter
    return


@app.cell
def _(x_train, y_train):
    import torch
    import torch.nn as nn
    from torchviz import make_dot



    torch.manual_seed(43)   # reproduzierbare Zufallsinitialisierung

    # ---------- Ground Truth (nur zur Datengenerierung) ----------
    TRUE_A, TRUE_B, TRUE_C = 2.0, 7.0, 3.0

    def true_function(x: torch.Tensor) -> torch.Tensor:
    	# Funktion: y(x) = 2*sin(x) + sin(7x + 3)
        return TRUE_A * torch.sin(x) + torch.sin(TRUE_B * x + TRUE_C)

    # ---------- Trainingsdaten ----------
    x_train_t = torch.tensor(data=x_train, dtype=torch.float64)
    y_train_t = torch.tensor(data=y_train, dtype=torch.float64)

    # ---------- Modell mit zufälliger Initialisierung ----------
    init_width = 2
    class WavyFunction(nn.Module):
        def __init__(self):
            super().__init__()
            # Weite Gleichverteilung, damit b=7 überhaupt erreichbar ist
            self.a = nn.Parameter(torch.empty((), dtype=torch.float64).uniform_(TRUE_A - init_width,  TRUE_A + init_width))
            self.b = nn.Parameter(torch.empty((), dtype=torch.float64).uniform_(TRUE_B - init_width,  TRUE_B + init_width))
            self.c = nn.Parameter(torch.empty((), dtype=torch.float64).uniform_(TRUE_C - init_width,  TRUE_C + init_width))

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.a * torch.sin(x) + torch.sin(self.b * x + self.c)


    model = WavyFunction()
    print(f"Init:  a={model.a.item():+.4f}  b={model.b.item():+.4f}  c={model.c.item():+.4f}")

    # ---------- Training ----------
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    n_epochs = 3000

    for epoch in range(n_epochs + 1):
        optimizer.zero_grad()
        y_pred = model(x_train_t)
        loss = ((y_pred - y_train_t) ** 2).mean()
        loss.backward()
        optimizer.step()

        if epoch % 500 == 0:
            print(f"epoch {epoch:4d}  loss={loss.item():.3e}  "
                  f"a={model.a.item():+.4f}  b={model.b.item():+.4f}  c={model.c.item():+.4f}")

    print(f"\nGelernt:  a={model.a.item():+.4f}  b={model.b.item():+.4f}  c={model.c.item():+.4f}")
    print(f"Wahr:     a={TRUE_A:+.4f}  b={TRUE_B:+.4f}  c={TRUE_C:+.4f}")

    # ---------- Berechnungsgraph mit torchviz ----------
    # Skalarer Eingang (wie im Original-Beispiel), damit der Graph kompakt bleibt
    x1 = torch.tensor(1.0, requires_grad=True, dtype=torch.float64)
    y1 = model(x1)

    dot = make_dot(
        y1,
        params=dict(model.named_parameters()),   # a, b, c als benannte Blätter
        show_attrs=True,
        show_saved=True,
    )
    dot
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
