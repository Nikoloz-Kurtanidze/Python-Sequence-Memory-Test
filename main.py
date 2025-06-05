from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
import design, sys
from random import randint
import winsound

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = design.Ui_MainWindow()
ui.setupUi(MainWindow)


buttons = [ui.pushButton, ui.pushButton_2, ui.pushButton_3, ui.pushButton_4, ui.pushButton_5, ui.pushButton_6, ui.pushButton_7, ui.pushButton_8, ui.pushButton_9]
button_classes = []
timer = QTimer()

random_numbers = []
selected_numbers = []
show_index = 0
is_displaying = True

# ღილაკის კლასი
class Button:
    def __init__(self, QtButton, index):
        self.QtButton = QtButton
        self.index = index
        self.QtButton.clicked.connect(self.on_click)
    
    def on_click(self):
        global is_displaying, show_index, selected_numbers, random_numbers
        if not is_displaying: # როდესაც მიმდევრობის გამეორების დროა
            selected_numbers.append(self.index)
            if selected_numbers[-1] == random_numbers[len(selected_numbers) -1]:
                if len(selected_numbers) == len(random_numbers):
                    # თუ პასუხი სწორია და ბოლოა მიმდევრობიდან
                    is_displaying = True
                    show_index = 0
                    selected_numbers = []
                    random_numbers.append(randint(0, 8))
                    timer.singleShot(2000, show_sequence)

            else:
                # არასწორი პასუხის შემთხვევაში
                messageBox = QMessageBox()
                messageBox.setWindowTitle("წააგე")
                messageBox.setText(f"ქულა - {len(random_numbers) -1}")
                messageBox.finished.connect(app.quit)
                messageBox.exec_()

            self.animate()
    
    def animate(self):
        # ცვლის ღილაკის სტილს
        self.QtButton.setStyleSheet(self.QtButton.styleSheet() + "Background-color: white; border: 8px solid black")
        timer.singleShot(700, self.end_animation)
        
        if ui.checkBox.isChecked():
            winsound.PlaySound(f"sounds/{self.index}.wav", winsound.SND_ASYNC)

    def end_animation(self):
        # უბრუნებს იგივე სტილს
        self.QtButton.setStyleSheet(self.QtButton.styleSheet().replace("Background-color: white; border: 8px solid black", ""))


# ყოველი QPushButton-ისთვის ქმნის Button კლასს
for i, btn in enumerate(buttons):
    button_classes.append(Button(btn, i))


# ფუნქცია რომელიც იწყებს მიმდევრობის ჩვენებას
def show_sequence():
    global show_index, is_displaying
    button = button_classes[random_numbers[show_index]]
    button.animate()
    show_index += 1

    if show_index < len(random_numbers):
        # თუ არ არის ბოლომდე მისული იმეორებს
        timer.singleShot(1500, show_sequence)
    else:
        is_displaying = False


ui.checkBox.setChecked(True)

# დაწყებისთვის საჭირო კოდი
random_numbers.append(randint(0, 8))
timer.singleShot(2000, show_sequence)


MainWindow.show()
sys.exit(app.exec_())