import os
import shutil
import platform
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    else:  # Linux and other Unix-like OS
        subprocess.run(["xdg-open", path])

def create_document(output_folder):
    pass
    # create PDF

    # create E-Book

def create_latex_head(photo_path, title, output_folder):
    pass

def create_latex_backbone(output_folder="./output"):
    # ================
    # >>> main doc <<<
    # ================
    main_doc = r"""
    % Load + Define document
    \documentclass[fontsize=11pt,paper=a5,pagesize=auto]{scrbook}

    % Settings
    \include{preambel}

    % Start Document
    \begin{document}

        % Title Page
        \include{titlepage}

        % Add Photo Pages
        \include{photos}

    \end{document}



    """
    with open(os.path.join(output_folder, "main.tex"), "w") as f:
        f.write(main_doc)

    # ====================
    # >>> preambel doc <<<
    # ====================
    preambel_doc = r"""
    % Set margins
    \usepackage[
        a5paper,
        top=2cm,
        bottom=2cm,
        left=2cm,
        right=2cm
    ]{geometry}

    % Font encoding & Font Style
    \usepackage[T1]{fontenc}
    \usepackage{lmodern}
    \usepackage{helvet}
    \renewcommand{\familydefault}{\sfdefault}

    % Dummy Texts
    \usepackage[german]{babel}  % required from blindtext
    \usepackage{blindtext}

    % Better text justification
    \usepackage{microtype}

    % Turn-Off additional space after a sentence
    \frenchspacing

    % Make hpyer links and references and table-of-content clickable
    \usepackage[
        colorlinks=true,
        linkcolor=black,      % for table-of-content & ref
        urlcolor=blue,       % for URL links
        citecolor=blue       % for \cite
    ]{hyperref}

    % For Images
    \usepackage{float}
    \usepackage{graphicx}
    \usepackage{placeins}
    \usepackage{tikz}
    \usetikzlibrary{shadows}"""
    with open(os.path.join(output_folder, "preambel.tex"), "w") as f:
        f.write(preambel_doc)

def create_or_clean_output_folder(output_folder="./output"):
    os.makedirs(output_folder, exist_ok=True)

    shutil.rmtree(output_folder)


def main(photo_path, title, output_folder="./output"):
    create_or_clean_output_folder(output_folder)
    create_latex_backbone(output_folder)
    create_latex_head(photo_path, title, output_folder)
    create_document(output_folder)
    open_folder(output_folder)

def gui():
    def start_button_event(name:str, photo_path:str, output_var, root):
        try:
            main(photo_path=photo_path, title=name)
            output = "Successfull generated your Latex / PDF / Ebook"
        except Exception as e:
            output = f"Error occured: {e}"
        output_var.set(f"Output:\n{output}")
        update_size(root)

    def update_size(root):
        root.minsize(0, 0)
        width = root.winfo_width()
        height = root.winfo_height()
        root.geometry('')
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        root.geometry(f"{width}x{height}")

    root = tk.Tk()
    root.title("Auto Photo Album Creator")
    root.geometry("600x400")
    # root.minsize(400, 200)

    main_window = ttk.Frame(root)
    main_window.pack(expand=True, fill='both')

    # make gui title
    header = ttk.Label(
        main_window,
        text="Automatic Photo Album Generator\n📷 -> 📖",
        font=("Segoe UI", 16, "bold"),
        anchor="center",
        justify="center",
        padding=10
    )
    header.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10, 20))

    # get title
    input_label = ttk.Label(main_window, text="Title:")
    input_label.grid(row=1, column=1, sticky="nswe", pady=10, padx=20)

    user_input = tk.StringVar()
    input_entry = ttk.Entry(main_window, textvariable=user_input)
    user_input.set("My awesome photo album")
    input_entry.grid(row=1, column=2, sticky="we", pady=10, padx=20)

    # search photo folder
    def enable_button():
        run_button["state"] = "normal"

    selected_directory = tk.StringVar()
    
    def browse_directory():
        path = filedialog.askdirectory()
        if path:
            selected_directory.set(path)
            enable_button()

    browse_button = ttk.Button(main_window, text="Browse Directory", command=browse_directory)
    browse_button.grid(row=2, column=1, columnspan=1, pady=10)

    directory_display = ttk.Label(main_window, textvariable=selected_directory)
    directory_display.grid(row=2, column=2, columnspan=1, pady=5)

    # run button and output label
    output_var = tk.StringVar()
    output_var.set("Output:")
    output_label = ttk.Label(main_window, textvariable=output_var, borderwidth=2)
    output_label.grid(row=4, rowspan=2, column=1, columnspan=2, sticky="nswe", pady=10, padx=20)

    run_button = ttk.Button(main_window, text="Run", command=lambda: start_button_event(user_input.get(), selected_directory.get(), output_var, root), takefocus=0)
    run_button.grid(row=3, column=1, columnspan=2, sticky="nswe", ipady=10, padx=20)
    run_button["state"] = "disabled"

    # set weights for resizable
    for i in range(6):
        main_window.grid_rowconfigure(i, weight=1)
    for i in range(4):
        main_window.grid_columnconfigure(i, weight=1)

    update_size(root)
    root.geometry("600x400")
    root.mainloop()



if __name__ == "__main__":
    gui()
    # main()

