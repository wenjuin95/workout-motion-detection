from tkinter import Tk
from model.workout_model import WorkoutModel
from view.main_view import MainView
from controller.main_controller import MainController


def main():
    root = Tk()

    model = WorkoutModel()
    view = MainView(root)
    controller = MainController(model, view)
    root.mainloop()


if __name__ == "__main__":
    main()
