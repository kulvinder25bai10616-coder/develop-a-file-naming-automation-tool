import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path
import shutil

class FileNamingAutomationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("File Naming Automation Tool")
        self.root.geometry("800x600")
        
        
        self.selected_files = []
        self.preview_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Select Files", command=self.select_files).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="Select Folder", command=self.select_folder).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Clear Selection", command=self.clear_selection).grid(row=0, column=2, padx=5)
        
        
        self.file_listbox = tk.Listbox(file_frame, height=6, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        
        naming_frame = ttk.LabelFrame(main_frame, text="Naming Options", padding="5")
        naming_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        
        ttk.Label(naming_frame, text="Base Name:").grid(row=0, column=0, sticky=tk.W)
        self.base_name = tk.StringVar(value="document")
        ttk.Entry(naming_frame, textvariable=self.base_name).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        
        ttk.Label(naming_frame, text="Numbering:").grid(row=1, column=0, sticky=tk.W)
        self.numbering_type = tk.StringVar(value="sequential")
        numbering_frame = ttk.Frame(naming_frame)
        numbering_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Radiobutton(numbering_frame, text="Sequential", variable=self.numbering_type, value="sequential").pack(side=tk.LEFT)
        ttk.Radiobutton(numbering_frame, text="Keep Original", variable=self.numbering_type, value="keep_original").pack(side=tk.LEFT)
        
        
        ttk.Label(naming_frame, text="Start Number:").grid(row=2, column=0, sticky=tk.W)
        self.start_number = tk.StringVar(value="1")
        ttk.Entry(naming_frame, textvariable=self.start_number, width=10).grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        
        ttk.Label(naming_frame, text="Number Padding:").grid(row=3, column=0, sticky=tk.W)
        self.number_padding = tk.StringVar(value="0")
        ttk.Entry(naming_frame, textvariable=self.number_padding, width=10).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
    
        self.add_timestamp = tk.BooleanVar()
        ttk.Checkbutton(naming_frame, text="Add Timestamp", variable=self.add_timestamp).grid(row=4, column=0, columnspan=2, sticky=tk.W)
        
        
        ttk.Label(naming_frame, text="Timestamp Format:").grid(row=5, column=0, sticky=tk.W)
        self.timestamp_format = tk.StringVar(value="%Y%m%d_%H%M%S")
        ttk.Entry(naming_frame, textvariable=self.timestamp_format).grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        
        ttk.Label(naming_frame, text="Case:").grid(row=6, column=0, sticky=tk.W)
        self.case_type = tk.StringVar(value="keep")
        case_frame = ttk.Frame(naming_frame)
        case_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Radiobutton(case_frame, text="Keep Original", variable=self.case_type, value="keep").pack(side=tk.LEFT)
        ttk.Radiobutton(case_frame, text="Lowercase", variable=self.case_type, value="lower").pack(side=tk.LEFT)
        ttk.Radiobutton(case_frame, text="Uppercase", variable=self.case_type, value="upper").pack(side=tk.LEFT)
        ttk.Radiobutton(case_frame, text="Title Case", variable=self.case_type, value="title").pack(side=tk.LEFT)
        
        
        self.replace_spaces = tk.BooleanVar(value=True)
        ttk.Checkbutton(naming_frame, text="Replace spaces with underscores", variable=self.replace_spaces).grid(row=7, column=0, columnspan=2, sticky=tk.W)
        
        
        self.remove_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(naming_frame, text="Remove special characters", variable=self.remove_special).grid(row=8, column=0, columnspan=2, sticky=tk.W)
        
         
        ttk.Label(naming_frame, text="Operation:").grid(row=9, column=0, sticky=tk.W)
        self.operation_type = tk.StringVar(value="rename")
        op_frame = ttk.Frame(naming_frame)
        op_frame.grid(row=9, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Radiobutton(op_frame, text="Rename Files", variable=self.operation_type, value="rename").pack(side=tk.LEFT)
        ttk.Radiobutton(op_frame, text="Copy Files", variable=self.operation_type, value="copy").pack(side=tk.LEFT)
        
        
        ttk.Label(naming_frame, text="Output Folder:").grid(row=10, column=0, sticky=tk.W)
        self.output_folder = tk.StringVar()
        ttk.Entry(naming_frame, textvariable=self.output_folder).grid(row=10, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Button(naming_frame, text="Browse", command=self.select_output_folder).grid(row=10, column=2, padx=(5, 0))
        
    
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        
        columns = ("original", "new_name")
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, show="headings", height=8)
        self.preview_tree.heading("original", text="Original Name")
        self.preview_tree.heading("new_name", text="New Name")
        self.preview_tree.column("original", width=300)
        self.preview_tree.column("new_name", width=300)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate Preview", command=self.generate_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Execute Renaming", command=self.execute_renaming).pack(side=tk.LEFT, padx=5)
        
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        file_frame.columnconfigure(1, weight=1)
        naming_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
    
    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files to rename")
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder containing files")
        if folder:
            
            files = [os.path.join(folder, f) for f in os.listdir(folder) 
                    if os.path.isfile(os.path.join(folder, f))]
            self.selected_files.extend(files)
            self.update_file_list()
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder for copies")
        if folder:
            self.output_folder.set(folder)
    
    def clear_selection(self):
        self.selected_files.clear()
        self.update_file_list()
        self.preview_tree.delete(*self.preview_tree.get_children())
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))
    
    def sanitize_filename(self, name):
        """Remove or replace problematic characters from filename"""
        if self.remove_special.get():
            
            name = re.sub(r'[^\w\s\.\-]', '', name)
        
        if self.replace_spaces.get():
            name = name.replace(' ', '_')
        
        
        if self.case_type.get() == "lower":
            name = name.lower()
        elif self.case_type.get() == "upper":
            name = name.upper()
        elif self.case_type.get() == "title":
            name = name.title()
        
        return name
    
    def generate_preview(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected!")
            return
        
        try:
            start_num = int(self.start_number.get())
            padding = int(self.number_padding.get())
        except ValueError:
            messagebox.showerror("Error", "Start number and padding must be integers!")
            return
        
        self.preview_tree.delete(*self.preview_tree.get_children())
        self.preview_data = []
        
        for i, file_path in enumerate(self.selected_files):
            original_name = os.path.basename(file_path)
            original_stem = Path(file_path).stem
            original_suffix = Path(file_path).suffix
            
            
            new_name = self.base_name.get()
            
            
            if self.numbering_type.get() == "sequential":
                number = start_num + i
                if padding > 0:
                    number_str = f"{number:0{padding}d}"
                else:
                    number_str = str(number)
                new_name += f"_{number_str}"
            else:
                # Try to extract numbers from original filename
                numbers = re.findall(r'\d+', original_stem)
                if numbers:
                    new_name += f"_{numbers[0]}"
            
            
            if self.add_timestamp.get():
                try:
                    timestamp = datetime.now().strftime(self.timestamp_format.get())
                    new_name += f"_{timestamp}"
                except:
                    messagebox.showerror("Error", "Invalid timestamp format!")
                    return
            
            
            new_name += original_suffix
            
            
            new_name = self.sanitize_filename(new_name)
            
            self.preview_data.append((file_path, new_name))
            self.preview_tree.insert("", tk.END, values=(original_name, new_name))
    
    def execute_renaming(self):
        if not self.preview_data:
            messagebox.showwarning("Warning", "Please generate preview first!")
            return
        
        operation = self.operation_type.get()
        
        if operation == "copy" and not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder for copy operation!")
            return
        
        try:
            success_count = 0
            failed_files = []
            
            for original_path, new_name in self.preview_data:
                try:
                    if operation == "rename":
                        
                        directory = os.path.dirname(original_path)
                        new_path = os.path.join(directory, new_name)
                        
                        
                        if os.path.exists(new_path):
                            response = messagebox.askyesno(
                                "File exists", 
                                f"File {new_name} already exists. Overwrite?"
                            )
                            if not response:
                                failed_files.append((original_path, "File exists"))
                                continue
                        
                        os.rename(original_path, new_path)
                        success_count += 1
                    
                    else:  
                        output_dir = self.output_folder.get()
                        new_path = os.path.join(output_dir, new_name)
                        
                        
                        os.makedirs(output_dir, exist_ok=True)
                        
                        
                        if os.path.exists(new_path):
                            response = messagebox.askyesno(
                                "File exists", 
                                f"File {new_name} already exists. Overwrite?"
                            )
                            if not response:
                                failed_files.append((original_path, "File exists"))
                                continue
                        
                        shutil.copy2(original_path, new_path)
                        success_count += 1
                        
                except Exception as e:
                    failed_files.append((original_path, str(e)))
            
            
            if failed_files:
                failed_list = "\n".join([f"{os.path.basename(f[0])}: {f[1]}" for f in failed_files])
                messagebox.showinfo(
                    "Operation Complete", 
                    f"Successfully processed {success_count} files.\n\n"
                    f"Failed files:\n{failed_list}"
                )
            else:
                messagebox.showinfo("Success", f"All {success_count} files processed successfully!")
            
        
            if operation == "rename":
                self.selected_files = [new_path for _, new_path in self.preview_data]
                self.update_file_list()
                self.preview_tree.delete(*self.preview_tree.get_children())
                self.preview_data = []
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

def main():
    root = tk.Tk()
    app = FileNamingAutomationTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()