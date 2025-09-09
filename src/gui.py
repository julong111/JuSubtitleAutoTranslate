#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2025/8/11
# @Author : julong@111.com
# @Description : JuSubTitleAutoTranslate的GUI界面

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import queue
import sys
from pathlib import Path
import configparser
import subprocess

from tkhtmlview import HTMLScrolledText
from model_utils import is_model_folder_complete, download_model

class TranslatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI自动翻译工具")
        self.config_file = Path(__file__).parent / "config.ini"
        self.config = configparser.ConfigParser()

        self.load_window_geometry()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Environment Status Check ---
        status_frame = ttk.LabelFrame(main_frame, text="环境状态检测", padding="10")
        status_frame.pack(fill=tk.X, pady=5)

        self.opus_status = tk.StringVar(value="检测中...")
        self.nllb_status = tk.StringVar(value="检测中...")

        ttk.Label(status_frame, text="OPUS 模型:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.opus_status).grid(row=0, column=1, sticky=tk.W, padx=5)
        self.download_opus_button = ttk.Button(status_frame, text="下载 OPUS 模型", command=lambda: self.start_download_thread('opus'))
        self.download_opus_button.grid(row=0, column=2, padx=10)

        ttk.Label(status_frame, text="NLLB 模型:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.nllb_status).grid(row=1, column=1, sticky=tk.W, padx=5)
        self.download_nllb_button = ttk.Button(status_frame, text="下载 NLLB 模型", command=lambda: self.start_download_thread('nllb'))
        self.download_nllb_button.grid(row=1, column=2, padx=10)

        help_button = ttk.Button(status_frame, text="模型下载帮助", command=self.show_help_window)
        help_button.grid(row=0, column=3, rowspan=2, padx=20)

        # --- Mode Selection ---
        mode_frame = ttk.LabelFrame(main_frame, text="翻译模式", padding="10")
        mode_frame.pack(fill=tk.X, pady=5)
        self.mode = tk.StringVar(value="single")
        ttk.Radiobutton(mode_frame, text="单文件翻译", variable=self.mode, value="single", command=self.toggle_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="文件夹批量翻译", variable=self.mode, value="batch", command=self.toggle_mode).pack(side=tk.LEFT, padx=5)

        # --- Path Selection ---
        path_frame = ttk.LabelFrame(main_frame, text="路径选择", padding="10")
        path_frame.pack(fill=tk.X, pady=5)

        self.input_path_label = ttk.Label(path_frame, text="输入文件:")
        self.input_path_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.input_path, width=60).grid(row=0, column=1, sticky=tk.EW)
        ttk.Button(path_frame, text="浏览...", command=self.browse_input).grid(row=0, column=2, padx=5)

        self.output_path_label = ttk.Label(path_frame, text="输出路径 (可选):")
        self.output_path_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.output_path, width=60).grid(row=1, column=1, sticky=tk.EW)
        ttk.Button(path_frame, text="浏览...", command=self.browse_output).grid(row=1, column=2, padx=5)
        path_frame.columnconfigure(1, weight=1)

        # --- Model Configuration ---
        model_frame = ttk.LabelFrame(main_frame, text="模型配置", padding="10")
        model_frame.pack(fill=tk.X, pady=5)

        ttk.Label(model_frame, text="翻译模型:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.model_type = tk.StringVar(value="opus")
        model_menu = ttk.OptionMenu(model_frame, self.model_type, "opus", "opus", "nllb", command=self.toggle_nllb_options)
        model_menu.grid(row=0, column=1, sticky=tk.W, padx=5)

        self.auto_download = tk.BooleanVar()
        ttk.Checkbutton(model_frame, text="自动下载模型", variable=self.auto_download).grid(row=0, column=2, padx=10)

        ttk.Label(model_frame, text="模型路径 (可选):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.model_path = tk.StringVar()
        ttk.Entry(model_frame, textvariable=self.model_path, width=60).grid(row=1, column=1, columnspan=2, sticky=tk.EW)
        model_frame.columnconfigure(1, weight=1)

        # --- NLLB Options ---
        self.nllb_frame = ttk.LabelFrame(main_frame, text="NLLB 模型选项", padding="10")

        ttk.Label(self.nllb_frame, text="源语言:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.source_lang = tk.StringVar(value="eng_Latn")
        ttk.Entry(self.nllb_frame, textvariable=self.source_lang).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(self.nllb_frame, text="目标语言:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.target_lang = tk.StringVar(value="zho_Hans")
        ttk.Entry(self.nllb_frame, textvariable=self.target_lang).grid(row=1, column=1, sticky=tk.W, padx=5)

        # --- Execution and Logging ---
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill=tk.X, pady=5)

        self.start_button = ttk.Button(action_frame, text="开始翻译", command=self.start_translation_thread)
        self.start_button.pack(pady=5)

        log_frame = ttk.LabelFrame(main_frame, text="日志输出", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15, state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.queue = queue.Queue()
        self.after(100, self.process_queue)

        self.toggle_mode()
        self.toggle_nllb_options()
        self.check_model_status()

    def load_window_geometry(self):
        self.config.read(self.config_file)
        if 'window' in self.config and 'geometry' in self.config['window']:
            self.geometry(self.config['window']['geometry'])
        else:
            # Center the window if no config is found
            window_width = 800
            window_height = 750
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)
            self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def save_window_geometry(self):
        if 'window' not in self.config:
            self.config['window'] = {}
        self.config['window']['geometry'] = self.geometry()
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def on_closing(self):
        self.save_window_geometry()
        self.destroy()

    def show_help_window(self):
        try:
            help_path = Path(__file__).parent / "help.html"
            if not help_path.exists():
                messagebox.showerror("错误", "帮助文件 'src/help.html' 未找到。")
                return

            # Create a new top-level window
            help_win = tk.Toplevel(self)
            help_win.title("模型下载帮助")
            help_win.geometry("800x600") # Adjusted size for better HTML view

            # Make the help window modal
            help_win.transient(self)
            help_win.grab_set()

            # Add the HTMLScrolledText widget
            html_view = HTMLScrolledText(help_win)
            html_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Read and set the HTML content
            with open(help_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            html_view.set_html(html_content)

            # Add a close button
            close_button = ttk.Button(help_win, text="关闭", command=help_win.destroy)
            close_button.pack(pady=10)

        except ImportError:
            messagebox.showerror("错误", "HTML渲染库 'tkhtmlview' 未找到。\n\n请通过 pip install tkhtmlview 命令安装后再试。")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开帮助文件: {e}")

    def check_model_status(self):
        project_root = Path(__file__).parent.parent
        models_dir = project_root / "models"

        # Define model paths and their essential files
        opus_base_path = models_dir / "models--Helsinki-NLP--opus-mt-en-zh"
        opus_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json", "source.spm", "target.spm"]
        
        if is_model_folder_complete(opus_base_path, opus_files):
            self.opus_status.set("✅ 已就绪")
        else:
            self.opus_status.set("❌ 未找到")

        nllb_base_path = models_dir / "models--facebook--nllb-200-distilled-600M"
        nllb_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json", "tokenizer.json"]
        
        if is_model_folder_complete(nllb_base_path, nllb_files):
            self.nllb_status.set("✅ 已就绪")
        else:
            self.nllb_status.set("❌ 未找到")

    def start_download_thread(self, model_type):
        self.start_button.config(state='disabled')
        self.download_opus_button.config(state='disabled')
        self.download_nllb_button.config(state='disabled')
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        thread = threading.Thread(target=self.run_download, args=(model_type,), daemon=True)
        thread.start()

    def run_download(self, model_type):
        try:
            # All download logic is now in model_utils.py
            download_model(model_type, self.queue)
        except Exception as e:
            self.queue.put(f"\n❌ 启动下载线程时发生意外错误: {e}\n")
        finally:
            # Schedule the UI updates to be run safely in the main thread
            self.after(100, self.restore_ui_after_download)

    def restore_ui_after_download(self):
        """Safely updates UI elements from the main thread after a download attempt."""
        self.check_model_status()
        self.start_button.config(state='normal')
        self.download_opus_button.config(state='normal')
        self.download_nllb_button.config(state='normal')

    def toggle_mode(self):
        mode = self.mode.get()
        if mode == "single":
            self.input_path_label.config(text="输入文件:")
            self.output_path_label.config(text="输出文件 (可选):")
        else: # batch
            self.input_path_label.config(text="输入文件夹:")
            self.output_path_label.config(text="输出文件夹 (可选):")
        self.input_path.set("")
        self.output_path.set("")

    def browse_input(self):
        mode = self.mode.get()
        if mode == "single":
            path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        else:
            path = filedialog.askdirectory()
        if path:
            self.input_path.set(path)

    def browse_output(self):
        mode = self.mode.get()
        if mode == "single":
            path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT files", "*.srt")])
        else:
            path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def toggle_nllb_options(self, *args):
        if self.model_type.get() == "nllb":
            self.nllb_frame.pack(fill=tk.X, pady=5, before=self.start_button.master)
        else:
            self.nllb_frame.pack_forget()

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def process_queue(self):
        try:
            message = self.queue.get_nowait()
            self.log(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def start_translation_thread(self):
        self.start_button.config(state='disabled')
        self.download_opus_button.config(state='disabled')
        self.download_nllb_button.config(state='disabled')
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        thread = threading.Thread(target=self.run_translation, daemon=True)
        thread.start()

    def run_translation(self):
        try:
            # Find the path to translate.py relative to the current script (gui.py)
            script_path = Path(__file__).parent / "translate.py"
            if not script_path.exists():
                self.queue.put(f"错误: 未找到翻译脚本 translate.py\n")
                return

            command = [sys.executable, str(script_path)]

            # Mode and paths
            if self.mode.get() == "single":
                if not self.input_path.get():
                    self.queue.put("错误: 请选择输入文件。\n")
                    return
                command.extend(["-i", self.input_path.get()])
                if self.output_path.get():
                    command.extend(["-o", self.output_path.get()])
            else: # batch
                if not self.input_path.get():
                    self.queue.put("错误: 请选择输入文件夹。\n")
                    return
                command.extend(["-di", self.input_path.get()])
                if self.output_path.get():
                    command.extend(["-do", self.output_path.get()])

            # Model options
            command.extend(["-m", self.model_type.get()])
            if self.model_path.get():
                command.extend(["--model_path", self.model_path.get()])
            if self.auto_download.get():
                command.append("--auto-download")

            # NLLB options
            if self.model_type.get() == "nllb":
                command.extend(["--source_lang", self.source_lang.get()])
                command.extend(["--target_lang", self.target_lang.get()])

            self.queue.put(f"执行命令: {' '.join(command)}\n\n")
            
            project_root = Path(__file__).parent.parent

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=project_root
            )

            for line in iter(process.stdout.readline, ' '):
                if not line:
                    break
                self.queue.put(line)
            
            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                self.queue.put("\n🎉 翻译任务成功完成!\n")
            else:
                self.queue.put(f"\n❌ 翻译任务失败，退出代码: {process.returncode}\n")

        except Exception as e:
            self.queue.put(f"\n❌ 启动翻译时发生意外错误: {e}\n")
        finally:
            self.start_button.config(state='normal')
            self.download_opus_button.config(state='normal')
            self.download_nllb_button.config(state='normal')

if __name__ == "__main__":
    app = TranslatorGUI()
    app.mainloop()
