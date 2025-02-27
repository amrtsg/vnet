import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
import config as cfg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Global variables for GUI elements
root = None
train_label = None
val_label = None
canvas_train = None
canvas_val = None
canvas_val_img = None

# Create a Figure instance for training loss
fig_train = Figure(figsize=(5, 4), dpi=100)
loss_history_train = {"steps": [], "d_loss": [], "g_loss": []}
ax_train = fig_train.add_subplot(111)
x_train = []  # To store x-values (step numbers)
y_train = []  # To store y-values (losses)

# Create a Figure instance for validation loss
fig_val = Figure(figsize=(5, 4), dpi=100)
loss_history_val = {"steps": [], "total_loss": []}
ax_val = fig_val.add_subplot(111)
x_val = []  # To store x-values (step numbers)
y_val = []  # To store y-values (losses)

# Create a Figure instance for images
fig_image2 = Figure(figsize=(5, 4), dpi=100)
ax_image2 = fig_image2.add_subplot(111)


def initialize_gui_elements():
    global train_label, val_label, canvas_train, canvas_val, canvas_val_img
    
    # Initialize GUI elements
    train_label = ttk.Label(root, text="", font=("Helvetica", 12))
    train_label.grid(row=0, column=0, columnspan=2, padx=40)

    val_label = ttk.Label(root, text="", font=("Helvetica", 12))
    val_label.grid(row=0, column=2, columnspan=2, padx=40)

    # Create a FigureCanvasTkAgg object using the Figure for training loss
    if cfg.USE_GRAPHS:
        canvas_train = FigureCanvasTkAgg(fig_train, master=root)
        canvas_train.get_tk_widget().grid(row=1, column=0, columnspan=2)
        if cfg.USE_VAL:
            # Create a FigureCanvasTkAgg object using the Figure for validation loss
            canvas_val = FigureCanvasTkAgg(fig_val, master=root)
            canvas_val.get_tk_widget().grid(row=1, column=2, columnspan=2)
            canvas_val_img = FigureCanvasTkAgg(fig_image2, master=root)
            canvas_val_img.get_tk_widget().grid(row=1, column=4, columnspan=2)


def update_train_plot(curr_epoch, step, d_loss, g_loss):
    global train_label
    if train_label:
        train_label.config(text=f"Epoch {int(curr_epoch)}: "\
                                f"Step {step}: "\
                                f"Discriminator: {d_loss:.2f} "\
                                f"Generator: {g_loss:.2f}")
        if cfg.USE_GRAPHS and canvas_train:
            loss_history_train["steps"].append(step)
            loss_history_train["d_loss"].append(d_loss)
            loss_history_train["g_loss"].append(g_loss)
            # Clear the previous graph
            ax_train.clear()
            # Update x and y for the graph
            x_train.append(step)
            y_train.append(d_loss)  # You can choose which loss to plot
            ax_train.plot(loss_history_train["steps"], loss_history_train["d_loss"], label='Discriminator Loss', color='blue')
            ax_train.plot(loss_history_train["steps"], loss_history_train["g_loss"], label='Generator Loss', color='red')
            ax_train.set_xlabel('Step')
            ax_train.set_ylabel('Loss')
            ax_train.legend()
            # Redraw the canvas
            canvas_train.draw()


def update_val_plot(curr_epoch, step, val_loss, img):
    global val_label
    if val_label:
        val_label.config(text=f"VAL Epoch {int(curr_epoch)}: "\
                              f"VAL Step {step}: "\
                              f"VAL Loss: {val_loss[0]:.2f} ")
        if cfg.USE_GRAPHS and canvas_val:
            loss_history_val["steps"].append(step)
            loss_history_val["total_loss"].append(val_loss[0])
            # Clear the previous graph
            ax_val.clear()
            # Update x and y for the graph
            x_val.append(step)
            y_val.append(val_loss[0])  # You can choose which loss to plot
            ax_val.plot(loss_history_val["steps"], loss_history_val["total_loss"], label='Validation Loss', color='green')
            ax_val.set_xlabel('Step')
            ax_val.set_ylabel('Loss')
            ax_val.legend()
            ax_image2.imshow(img[0])
            ax_image2.axis('off')
            # Redraw the canvas
            canvas_val.draw()
            canvas_val_img.draw()


def start_gui():
    global root
    root = tk.Tk()
    root.title("Training Progress")
    
    initialize_gui_elements()

    root.mainloop()


def init_gui():
    # Create a thread for the GUI
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()