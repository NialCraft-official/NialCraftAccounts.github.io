import tkinter as tk, random as rn, math as m, os, zipfile, subprocess as sp, sys
class G:
 def __init__(s, r):
  s.r = r; r.attributes("-fullscreen", True); s.cur = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cursor.cur").replace('\\', '/')
  try: r.config(cursor=f"@{s.cur}")
  except: pass
  s.st, s.mt, s.pts, s.jnts, s.m_r = "MENU", "default", [], [], os.path.join(os.path.dirname(os.path.abspath(__file__)), "Mods")
  s.df = {"name": "Стандарт", "gravity_mult": 1.0, "damping": 0.99, "bone_color": "#e6e6e6", "joint_color": "#c83232", "bone_width": 3}; s.cfg = s.df.copy(); s.ml, s.sl, s.lx, s.ly = [], None, 0, 0
  if not os.path.exists(s.m_r): os.makedirs(s.m_r)
  s.ld(); s.am()
  s.mf = tk.Frame(r, bg="#141419"); s.mf.pack(fill=tk.BOTH, expand=True)
  r.bind("<F11>", lambda e: r.attributes("-fullscreen", not r.attributes("-fullscreen"))); r.bind("<f>", s.th); r.bind("<F>", s.th); s.sm()
  r.bind("<Button-3>", s.cm); r.protocol("WM_DELETE_WINDOW", s.ql)
 def ld(s):
  if not os.path.exists(s.m_r): return
  s.ml.clear()
  for file in [f for f in os.listdir(s.m_r) if f.endswith(".zip")]:
   try:
    with zipfile.ZipFile(os.path.join(s.m_r, file), 'r') as ar:
     cf = next((x for x in ar.namelist() if x.endswith("config.txt")), None)
     if cf:
      with ar.open(cf) as f:
       mc = s.df.copy(); mc["file"], mc["active"] = file, False
       for line in f.read().decode("utf-8").splitlines():
        if "=" in line:
         k, v = [x.strip() for x in line.split("=", 1)]
         if k in mc: mc[k] = float(v) if k in ["gravity_mult", "damping"] else (int(v) if k == "bone_width" else v)
       s.ml.append(mc)
   except: pass
 def am(s):
  s.cfg = s.df.copy()
  for mc in s.ml:
   if mc.get("active"):
    for k in s.cfg: s.cfg[k] = mc[k]
    break
 def ql(s):
  if os.path.exists("launcher.py"): sp.Popen([sys.executable, "launcher.py"])
  s.r.destroy()
 def cm(s, e):
  if s.st != "MENU": return
  mm = tk.Menu(s.r, tearoff=0, bg="#19191e", fg="white", activebackground="#235a23", bd=1)
  mm.add_command(label=" Mods ", command=s.mw); mm.add_command(label=" Open Folder ", command=lambda: os.startfile(s.m_r))
  try: mm.config(cursor=f"@{s.cur}")
  except: pass
  mm.post(e.x_root, e.y_root)
 def sl_m(s, lbl, mc):
  if s.sl:
   if s.sl.winfo_exists(): s.sl.config(bg="#0f0f12", fg="#e6e6e6")
  s.sl = lbl; lbl.config(bg="#232328", fg="#ff7700")
 def os(s, mc):
  tw = tk.Toplevel(s.r); tw.title(mc["name"]); tw.geometry("300x200"); tw.config(bg="#19191e"); tw.resizable(False, False); tw.transient(s.r); tw.grab_set()
  try: tw.config(cursor=f"@{s.cur}")
  except: pass
  tk.Label(tw, text=f"Статус: {'АКТИВЕН' if mc['active'] else 'ОТКЛЮЧЕН'}", font=("Arial", 12, "bold"), fg="#00ff33" if mc['active'] else "#ca4b4b", bg="#19191e").pack(pady=20)
  def tg(act):
   if act:
    for m in s.ml: m["active"] = False
   mc["active"] = act; s.am(); tw.destroy(); s.mw()
  b1 = tk.Button(tw, text="ВКЛЮЧИТЬ", bg="#235a23", fg="white", width=12, command=lambda: tg(True)); b1.pack(pady=5)
  b2 = tk.Button(tw, text="ОТКЛЮЧИТЬ", bg="#641e1e", fg="white", width=12, command=lambda: tg(False)); b2.pack(pady=5)
  try: b1.config(cursor=f"@{s.cur}"); b2.config(cursor=f"@{s.cur}")
  except: pass
 def mw(s):
  s.cf(); s.st = "MODS_VIEW"; s.mf.grid_columnconfigure(0, weight=1); s.mf.grid_rowconfigure(0, weight=1)
  mc = tk.Frame(s.mf, bg="#141419"); mc.grid(row=0, column=0, sticky="nsew")
  tk.Label(mc, text="МОДЫ", font=("Arial", 24, "bold"), fg="#ff7700", bg="#141419").pack(pady=40)
  lf = tk.Frame(mc, bg="#0f0f12", bd=1, relief="solid"); lf.pack(pady=10, fill=tk.BOTH, expand=True, padx=200)
  if not s.ml: tk.Label(lf, text="Пусто", font=("Arial", 14), fg="#ca4b4b", bg="#0f0f12").pack(pady=50)
  else:
   for m_d in s.ml:
    st = " [АКТ]" if m_d["active"] else " [ОТКЛ]"
    l = tk.Label(lf, text=f"-> {m_d['name']}{st}", font=("Arial", 14), fg="#00ff33" if m_d["active"] else "#e6e6e6", bg="#0f0f12", anchor="w", padx=20, pady=5); l.pack(fill=tk.X)
    try: l.config(cursor=f"@{s.cur}")
    except: pass
    l.bind("<Button-1>", lambda e, lbl=l, data=m_d: s.sl_m(lbl, data))
    l.bind("<Double-Button-1>", lambda e, data=m_d: s.os(data))
  bb = tk.Button(mc, text="<- НАЗАД", font=("Arial", 12), fg="white", bg="#3c3c41", width=10, command=s.sm); bb.pack(pady=20)
  try: bb.config(cursor=f"@{s.cur}")
  except: pass
 def cf(s):
  for w in s.mf.winfo_children(): w.destroy()
 def th(s, e):
  if s.st == "GAME": s.st = "MENU"; s.sm()
 def spawn_ragdoll(s, e):
  if s.st != "GAME": return
  x, y = e.x, e.y; i = len(s.pts)
  s.pts.extend([[x, y-60, x, y-60, 10], [x, y-40, x, y-40, 4], [x, y-10, x, y-10, 5], [x, y+20, x, y+20, 5], [x-25, y-35, x-25, y-35, 4], [x-45, y-35, x-45, y-35, 4], [x-65, y-35, x-65, y-35, 4], [x+25, y-35, x+25, y-35, 4], [x+45, y-35, x+45, y-35, 4], [x+65, y-35, x+65, y-35, 4], [x-15, y+25, x-15, y+25, 4], [x-15, y+60, x-15, y+60, 4], [x-15, y+95, x-15, y+95, 4], [x+15, y+25, x+15, y+25, 4], [x+15, y+60, x+15, y+60, 4], [x+15, y+95, x+15, y+95, 4]])
  j = lambda p1, p2, l: s.jnts.append([i + p1, i + p2, l])
  j(0,1,20); j(1,2,30); j(2,3,30); j(1,4,25); j(4,5,20); j(5,6,20); j(1,7,25); j(7,8,20); j(8,9,20); j(3,10,15); j(10,11,35); j(11,12,35); j(3,13,15); j(13,14,35); j(14,15,35); j(0,2,50); j(4,7,50); j(10,13,30); j(2,10,45); j(2,13,45)
 def mm(s, e):
  s.lx, s.ly = e.x, e.y
 def update_physics(s):
  if s.st != "GAME": return
  g, d, fy = 0.5 * s.cfg["gravity_mult"], s.cfg["damping"], 850
  if s.mt == "water": g, d = 0.1 * s.cfg["gravity_mult"], s.cfg["damping"] * 0.86
  elif s.mt == "mountains": g = 0.8 * s.cfg["gravity_mult"]
  elif s.mt == "cave": g = 0.3 * s.cfg["gravity_mult"]
  for p in s.pts:
   vx, vy = (p-p)*d, (p-p)*d; p, p = p, p; p += vx; p += vy + g
   if p > fy - p: p = fy - p; p = p + vy * 0.4
  for _ in range(6):
   for j in s.jnts:
    p1, p2 = s.pts[j], s.pts[j]; dx, dy = p2 - p1, p2 - p1; dist = m.hypot(dx, dy) or 0.1; diff = j - dist; ox, oy = dx * (diff / dist) / 2, dy * (diff / dist) / 2; p1 -= ox; p1 -= oy; p2 += ox; p2 += oy
  s.dc.delete("dynamic"); tr = 130 + rn.randint(-4, 4) if s.mt == "cave" else 130
  for j in s.jnts:
   if s.mt == "cave":
    if m.hypot(s.pts[j] - s.lx, s.pts[j] - s.ly) > tr: continue
   s.dc.create_line(s.pts[j], s.pts[j], s.pts[j], s.pts[j], fill=s.cfg["bone_color"], width=s.cfg["bone_width"], tags="dynamic")
  for p in s.pts:
   if s.mt == "cave":
    if m.hypot(p - s.lx, p - s.ly) > tr: continue
   s.dc.create_oval(p-p, p-p, p+p, p+p, fill=s.cfg["joint_color"], outline="", tags="dynamic")
  if s.mt == "cave":
   s.dc.create_oval(s.lx-tr, s.ly-tr, s.lx+tr, s.ly+tr, outline="#000000", width=2000, tags="dynamic")
   for ex, ey in [(200, 400), (1200, 300), (700, 600)]:
    if m.hypot(ex - s.lx, ey - s.ly) > tr: s.dc.create_oval(ex, ey, ex+6, ey+6, fill="#ff0000", outline="", tags="dynamic"); s.dc.create_oval(ex+15, ey, ex+21, ey+6, fill="#ff0000", outline="", tags="dynamic")
  s.r.after(16, s.update_physics)
 def sg(s, target):
  s.cf(); s.st, s.mt, s.pts, s.jnts = "GAME", target, [], []
  s.mf.grid_columnconfigure(0, weight=1); s.mf.grid_rowconfigure(0, weight=1)
  s.dc = tk.Canvas(s.mf, bg="#000000" if target == "cave" else "#0f0f12", bd=0, highlightthickness=0)
  try: s.dc.config(cursor=f"@{s.cur}")
  except: pass
  s.dc.grid(row=0, column=0, sticky="nsew"); s.r.update(); w = s.mf.winfo_width()
  if target == "cave": s.dc.create_text(w // 2, 40, text="ВЫ УПАЛИ В ПЕЩЕРУ МИРА NIALCRAFT", fill="#ff7700", font=("Arial", 16, "bold"))
  else: s.dc.create_text(w // 2, 40, text=f"LIVE TEST CHAMBER [{target.upper()}]", fill="#c83232", font=("Arial", 14, "bold")); s.dc.create_line(0, 850, w, 850, fill="#64646e", width=8)
  s.dc.bind("<Button-1>", s.spawn_ragdoll); s.dc.bind("<Motion>", s.mm); s.update_physics()
 def sm(s):
  s.cf(); s.st = "MENU"; s.mf.grid_columnconfigure((0, 1), weight=1); s.mf.grid_rowconfigure(0, weight=1)
  lp = tk.Frame(s.mf, bg="#141419"); lp.grid(row=0, column=0, sticky="nsew")
  tk.Label(lp, text="RAGDOLL LABORATORY", font=("Arial", 36, "bold"), fg="#e6e6e6", bg="#141419").pack(pady=(150, 50))
  b1 = tk.Button(lp, text="ИГРАТЬ", font=("Arial", 20, "bold"), fg="white", bg="#235a23", width=18, command=s.sms); b1.pack(pady=20)
  b2 = tk.Button(lp, text="ВЫХОД", font=("Arial", 20, "bold"), fg="white", bg="#641e1e", width=18, command=s.ql); b2.pack(pady=20)
  try: b1.config(cursor=f"@{s.cur}"); b2.config(cursor=f"@{s.cur}")
  except: pass
  rp = tk.Frame(s.mf, bg="#0f0f12"); rp.grid(row=0, column=1, sticky="nsew")
  s.dc = tk.Canvas(rp, bg="#0f0f12", bd=0, highlightthickness=0); s.dc.pack(fill=tk.BOTH, expand=True)
  try: s.dc.config(cursor=f"@{s.cur}")
  except: pass
  s.r.update(); w = rp.winfo_width(); s.dc.create_text(w // 2, 40, text="LIVE TEST CHAMBER SIMULATOR", fill="#c83232", font=("Arial", 14, "bold")); s.dc.create_line(0, 850, w, 850, fill="#64646e", width=8)
 def sms(s):
  s.cf(); s.st = "MAP_SELECT"; s.mf.grid_columnconfigure(0, weight=1); s.mf.grid_rowconfigure(0, weight=1)
  cc = tk.Frame(s.mf, bg="#19191e"); cc.grid(row=0, column=0, sticky="nsew")
  tk.Label(cc, text="ВЫБЕРИТЕ КАРТУ", font=("Arial", 28, "bold"), fg="white", bg="#19191e").pack(pady=100)
  bf = tk.Frame(cc, bg="#19191e"); bf.pack(pady=20)
  for mt, mn, mc in [("default", "ДЕФОЛТ", "#32323c"), ("mountains", "С ГОРАМИ", "#46464b"), ("water", "С ВОДОЙ", "#23415a"), ("cave", "ПЕЩЕРА", "#151515")]:
   btn = tk.Button(bf, text=mn, font=("Arial", 18, "bold"), fg="white", bg=mc, width=12, height=6, command=lambda t=mt: s.sg(t)); btn.pack(side=tk.LEFT, padx=15)
   try: btn.config(cursor=f"@{s.cur}")
   except: pass
  bb = tk.Button(cc, text="<- НАЗАД", font=("Arial", 14), fg="#ca4b4b", bg="#3c3c41", width=12, command=s.sm); bb.pack(pady=80)
  try: bb.config(cursor=f"@{s.cur}")
  except: pass
if __name__ == "__main__":
 root = tk.Tk(); app = G(root); root.mainloop()
