from tkinter import *
from tkinter import ttk, messagebox
from generation import ImaGen as Generator, ListModels
import threading
import time


class GenerationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ImaGen UI")
    
        self.gen = Generator()
        self.modelslist = ListModels()
        self.model_var = StringVar()
        self.model_var.set(self.modelslist[0])
        self.prompt_var = StringVar()
        self.api_key_var = StringVar()
        self.generations_var = StringVar()
        self.progress_var = DoubleVar()
        self.remaining_time_var = StringVar()
##        self.width_mul_var = StringVar()
##        self.height_mul_var = StringVar()
        
        

        self.create_widgets()

    def create_widgets(self):
        # Model selection
        Label(self.root, text="Select Model:").grid(row=0, column=0, pady=10)
        models_dropdown = OptionMenu(self.root, self.model_var, *self.modelslist)
        models_dropdown.grid(row=0, column=1, pady=10)

        # Prompt input
        Label(self.root, text="Type a prompt:").grid(row=1, column=0, pady=10)
        prompt_entry = Entry(self.root, textvariable=self.prompt_var)
        prompt_entry.grid(row=1, column=1, pady=10)

        # API Key input
        Label(self.root, text="API Key (optional):").grid(row=2, column=0, pady=10)
        api_key_entry = Entry(self.root, textvariable=self.api_key_var)
        api_key_entry.grid(row=2, column=1, pady=10)

        # Number of generations input
        Label(self.root, text="Number of Generations (optional):").grid(row=3, column=0, pady=10)
        generations_entry = Entry(self.root, textvariable=self.generations_var)
        generations_entry.grid(row=3, column=1, pady=10)

##        # Width multiplier input
##        Label(self.root, text="width multiplier (x64):").grid(row=0, column=2, pady=10)
##        width_mul_entry = Entry(self.root, textvariable=self.width_mul_var)
##        width_mul_entry.grid(row=0, column=3, pady=10)
##
##        # Height multiplier input
##        Label(self.root, text="height multiplier (x64):").grid(row=1, column=2, pady=10)
##        height_mul_entry = Entry(self.root, textvariable=self.height_mul_var)
##        height_mul_entry.grid(row=1, column=3, pady=10)
        

        # Start generation button
        generate_button = Button(self.root, text="Generate", command=self.start_generation)
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Progress bar
        progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        progress_bar.grid(row=5, column=0, columnspan=2, pady=10)

        # Remaining time label
        remaining_time_label = Label(self.root, text="Remaining Time:")
        remaining_time_label.grid(row=6, column=0, pady=5)
        remaining_time_display = Label(self.root, textvariable=self.remaining_time_var)
        remaining_time_display.grid(row=6, column=1, pady=5)

    def start_generation(self):
        model = self.model_var.get()
        prompt = self.prompt_var.get()
        api_key = self.api_key_var.get()
        
        try:
            generations = int(self.generations_var.get())
        except ValueError:
            # Handle the case where the input is not a valid integer
            messagebox.showerror("Error", "Please enter a valid positive integer for the number of generations.")
            return
        if generations <= 0:
            messagebox.showerror("Error", "Number of generations must be a positive integer.")
            return

        def generate_and_update_progress():
            if api_key:
                self.gen.generate(prompt=prompt, models=[model], api_key=api_key, n=generations)
            else:
                self.gen.generate(prompt=prompt, models=[model], n=generations)

            status = self.gen.status()
            total_time = 0

            # Find the first non-zero wait_time
            while status["wait_time"] == 0:
                status = self.gen.status()

            total_time = status["wait_time"]

            while not status["done"]:
                status = self.gen.status()
                progress = 100 - (status["wait_time"] / total_time) * 100
                self.progress_var.set(progress)

                remaining_time = status["wait_time"]
                self.remaining_time_var.set(f"{remaining_time:.2f} seconds")

                self.root.update_idletasks()
                time.sleep(0.4)

            self.gen.extract_done("highplainimage")
            messagebox.showinfo("Generation Complete", "Done!")

        threading.Thread(target=generate_and_update_progress).start()


if __name__ == "__main__":
    root = Tk()
    app = GenerationUI(root)
    root.mainloop()
