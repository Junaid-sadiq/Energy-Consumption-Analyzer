import tkinter as tk
from view.view import View
from model.model import Model
from controller.controller import Controller

if __name__ == "__main__":
    model = Model()
    view = View(model, None)
    controller = Controller(model, view)
    view.set_controller(controller, model)
    view.mainloop()