import tkinter as tk, subprocess as sp, webbrowser as wb, os, sys, urllib.parse, json, base64, tkinter.messagebox as mb, tkinter.simpledialog as sd
class L:
 def __init__(s, r):
  s.r = r; r.title("NialCraft Labs Hub"); r.attributes("-fullscreen", True)
  s.cur = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cursor.cur").replace('\\', '/')
  try: r.config(cursor=f"@{s.cur}")
  except: pass
  s.user, s.av_colors = "Войти в профиль", None; s.st = "MENU"; s.mf = tk.Frame(r, bg="#141419"); s.mf.pack(fill=tk.BOTH, expand=True)
  s.mf.grid_columnconfigure(0, weight=0); s.mf.grid_columnconfigure(1, weight=1); s.mf.grid_rowconfigure(0, weight=1); s.sm()
 def cf(s):
  for w in s.rf.winfo_children(): w.destroy()
 def sb(s):
  s.lf = tk.Frame(s.mf, bg="#111115", width=250); s.lf.grid(row=0, column=0, sticky="nsew"); s.lf.pack_propagate(False)
  # Отрисовка пиксельного аватара из NIAL API в лаунчере
  if s.av_colors:
   av_c = tk.Canvas(s.lf, width=64, height=64, bg="#111115", bd=0, highlightthickness=0); av_c.pack(pady=(20, 5))
   for x in range(4):
    for y in range(8):
     if s.av_colors[x * 8 + y]:
      av_c.create_rectangle(x*8, y*8, x*8+8, y*8+8, fill="#ff3300", outline="")
      av_c.create_rectangle((7-x)*8, y*8, (7-x)*8+8, y*8+8, fill="#ff3300", outline="")
  b = lambda t, c, fg="white", bg="#111115": tk.Button(s.lf, text=t, font=("Arial", 12, "bold"), fg=fg, bg=bg, bd=0, activebackground="#191923", activeforeground="white", height=2, command=c).pack(fill=tk.X, pady=5, padx=10)
  b(s.user.upper(), s.sw_p, fg="#00ff33" if s.user != "Войти в профиль" else "#ca4b4b"); b("ГЛАВНАЯ", s.sm); b("ВЕРСИИ И ИГРЫ", s.sw_v); b("О ПРОЕКТЕ NIALCRAFT", s.sw_a)
  tk.Frame(s.lf, bg="#64646e", height=1).pack(fill=tk.X, pady=20, padx=15)
  b("ВЫХОД", s.r.quit, fg="#ca4b4b", bg="#1a1115")
  tk.Frame(s.mf, bg="#232328", width=2).grid(row=0, column=0, sticky="nse")
 def sm(s):
  s.st = "MENU"; s.rf = tk.Frame(s.mf, bg="#0f0f12"); s.rf.grid(row=0, column=1, sticky="nsew"); s.sb()
  tk.Label(s.rf, text="NIALCRAFT LABS", font=("Arial", 46, "bold"), fg="#e6e6e6", bg="#0f0f12", justify=tk.LEFT).pack(pady=(80, 10), padx=80, anchor="w")
  tk.Label(s.rf, text="ОФИЦИАЛЬНЫЙ ЧЕЙНДЖЛОГ v1.2.0:", font=("Arial", 14, "bold"), fg="#ff7700", bg="#0f0f12").pack(padx=80, anchor="w", pady=(30, 10))
  ch = tk.Frame(s.rf, bg="#141419", bd=1, relief="solid"); ch.pack(fill=tk.BOTH, expand=True, padx=80, pady=(0, 40))
  log = ["• [ФИЗИКА] Исправлен баг со спавном пиплов на ЛКМ.", "• [ПАСХАЛКА] Добавлен динамический свет факела и красные глаза в ПЕЩЕРЕ.", "• [МОДЫ] Добавлен продвинутый менеджер модов с окном переключения статусов.", "• [NIAL API] Подключен суверенный веб-протокол регистрации аккаунтов и пиксельных аватаров."]
  for line in log: tk.Label(ch, text=line, font=("Arial", 12), fg="#b4b4be", bg="#141419", anchor="w").pack(fill=tk.X, padx=20, pady=10)
  tk.Button(s.rf, text="ЗАПУСТИТЬ ЛАБОРАТОРИЮ", font=("Arial", 16, "bold"), fg="white", bg="#235a23", width=26, height=2, bd=0, command=s.sg).pack(pady=(0, 40))
 def sw_p(s):
  s.cf(); s.st = "PROFILE"
  tk.Label(s.rf, text="АВТОНОМНЫЙ ПРОФИЛЬ NIAL API", font=("Arial", 28, "bold"), fg="#e6e6e6", bg="#0f0f12").pack(pady=40)
  tk.Label(s.rf, text=f"Аккаунт: {s.user}", font=("Arial", 16), fg="#00ff33" if s.user != "Войти в профиль" else "#ca4b4b", bg="#0f0f12").pack(pady=10)
  def enter_nial_url():
   url = sd.askstring("NIAL API v3.0", "Вставьте скопированную ссылку с вашего сайта авторизации:", parent=s.r)
   if not url: return
   try:
    parsed = urllib.parse.urlparse(url); q = urllib.parse.parse_qs(parsed.query)
    if "nial_hash" in q:
     h_data = q["nial_hash"][0].replace("NIAL_PACKET_", "")
     dec = json.loads(base64.b64decode(h_data).decode("utf-8"))
     s.user = dec["n"]
     if dec.get("av"): s.av_colors = json.loads(base64.b64decode(dec["av"]).decode("utf-8"))
     s.sm(); mb.showinfo("NIAL API", f"Аккаунт успешно создан!\nДобро пожаловать в сеть, {s.user}!")
    elif "nial_token" in q:
     s.user = f"TOKEN: {q['nial_token'][0].upper()}"; s.av_colors = None; s.sm()
    else: mb.showerror("NIAL API Error", "Неверный формат ссылки. Пакет данных NIAL не обнаружен.")
   except Exception as e: mb.showerror("NIAL API Error", f"Критический сбой дешифрации пакета: {e}")
  btn = tk.Button(s.rf, text="СИНХРОНИЗИРОВАТЬ ССЫЛКУ NIAL API", font=("Arial", 14, "bold"), fg="white", bg="#ff3300", width=35, height=2, bd=0, command=enter_nial_url); btn.pack(pady=20)
  try: btn.config(cursor=f"@{s.cur}")
  except: pass
  btn_reg = tk.Button(s.rf, text="Впервые на NIAL? Создайте бесплатную учетную запись", font=("Arial", 11, "underline"), fg="#b4b4be", bg="#0f0f12", bd=0, activebackground="#0f0f12", activeforeground="#ffffff", command=lambda: wb.open("https://github.io"))
  btn_reg.pack(pady=10)
  try: btn_reg.config(cursor=f"@{s.cur}")
  except: pass
 def run_version(s, v):
  if "5.0" in v: s.sg()
  else: mb.showinfo("NialCraft Engine", f"Архивная версия {v} успешно распакована. Движок переключен.")
 def sw_v(s):
  s.cf(); s.st = "VERSIONS"
  tk.Label(s.rf, text="СПИСОК ВЕРСИЙ И ДРУГИЕ ИГРЫ", font=("Arial", 24, "bold"), fg="#e6e6e6", bg="#0f0f12").pack(pady=(30, 50))
  f = tk.Frame(s.rf, bg="#141419", bd=1, relief="solid"); f.pack(fill=tk.BOTH, expand=True, padx=80, pady=10)
  vs = ["Alpha 1.0", "Alpha 1.1", "Beta 1.0", "Beta 1.1", "Beta 1.2", "Beta 1.3", "Release 1.0", "Release 2.0", "Release 3.0", "Release 4.0", "Release 5.0 (Текущая)"]
  for v in vs:
   col = "#00ff33" if "5.0" in v else "#b4b4be"
   btn = tk.Button(f, text=f"  ✔ NialCraft Engine — {v}", font=("Arial", 11, "bold"), fg=col, bg="#141419", bd=0, activebackground="#191923", activeforeground=col, anchor="w", command=lambda ver=v: s.run_version(ver)); btn.pack(fill=tk.X, padx=10, pady=2)
   try: btn.config(cursor=f"@{s.cur}")
   except: pass
  bf = tk.Frame(s.rf, bg="#0f0f12"); bf.pack(fill=tk.X, padx=80, pady=20)
  b1 = tk.Button(bf, text="МОЙ ДВИЖОК", font=("Arial", 12, "bold"), fg="white", bg="#ff7700", width=22, height=1, bd=0, command=lambda: wb.open("https://github.io"))
  b2 = tk.Button(bf, text="СПИСОК МОИХ ИГР", font=("Arial", 12, "bold"), fg="white", bg="#32323c", width=22, height=1, bd=0, command=lambda: wb.open("https://github.com"))
  try: b1.config(cursor=f"@{s.cur}"); b2.config(cursor=f"@{s.cur}")
  except: pass
  b1.pack(side=tk.LEFT, padx=20); b2.pack(side=tk.LEFT, padx=20)
 def sw_a(s):
  s.cf(); s.st = "ABOUT"
  tk.Label(s.rf, text="СПЕЦИФИКАЦИЯ ПРОЕКТА И ROADMAP", font=("Arial", 22, "bold"), fg="#e6e6e6", bg="#0f0f12").pack(pady=(30, 10))
  info_frame = tk.Frame(s.rf, bg="#141419", bd=1, relief="solid"); info_frame.pack(fill=tk.BOTH, expand=True, padx=80, pady=10)
  tk.Label(info_frame, text="[ЯДРО ДВИЖКА NIALCRAFT 2D]", font=("Arial", 12, "bold"), fg="#ff7700", bg="#141419", anchor="w").pack(fill=tk.X, padx=20, pady=(15, 5))
  tk.Label(info_frame, text="• Архитектура: Оптимизированный мультиплеер на неблокирующих сокетах select.\n• Лимиты: Поддержка до 50 игроков одновременно с синхронизацией.\n• Файловая структура: Клиент main.py, Сервер server.py, Консоль RUN_SERVER.bat", font=("Arial", 11), fg="#b4b4be", bg="#141419", justify=tk.LEFT, anchor="w").pack(fill=tk.X, padx=20, pady=5)
  tk.Label(info_frame, text="[ТЕКУЩИЙ ROADMAP ПРОЕКТА]", font=("Arial", 12, "bold"), fg="#ff7700", bg="#141419", anchor="w").pack(fill=tk.X, padx=20, pady=(15, 5))
  roadmap = ["[x] Бинарный сетевой протокол на 50 слотов.", "[x] Автоматический резолв буквенных доменов облачных VPS.", "[-] Интеграция динамической подгрузки рабочих листов с GitHub Pages.", "[-] Синхронизация разрушения и установки блоков между игроками.", "[-] Добавление глобального чата."]
  for r_line in roadmap:
   col = "#00ff33" if "[x]" in r_line else "#64646e"
   tk.Label(info_frame, text=f"  {r_line}", font=("Arial", 11), fg=col, bg="#141419", anchor="w").pack(fill=tk.X, padx=20, pady=3)
  btn_git = tk.Button(s.rf, text="ОТКРЫТЬ РЕПОЗИТОРИЙ НА GITHUB", font=("Arial", 12, "bold"), fg="white", bg="#235a23", width=32, height=2, bd=0, command=lambda: wb.open("https://github.com/NialCraft.github.io/blob/main/README.md"))
  btn_git.pack(pady=20)
  try: btn_git.config(cursor=f"@{s.cur}")
  except: pass
 def sg(s):
  if os.path.exists("1.py"): sp.Popen([sys.executable, "1.py"]); s.r.destroy()
if __name__ == "__main__":
 root = tk.Tk(); app = L(root); root.mainloop()
