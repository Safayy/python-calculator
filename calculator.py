import sys
from functools import partial
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton)

WINDOW_SIZE = 235

class Calculator(QWidget):
    def __init__(self) -> None:
        #Initialize window
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.setStyleSheet("background-color: #241c24;")
        
        #Initialize calculator
        self.expression = ""
        
        #Add layouts
        self.layout = QVBoxLayout(self)
        self.screen = QLineEdit()
        self.screen.setStyleSheet("background-color: white; height: 50px; font-size: 20px;")
        self.screen.setReadOnly(True)
        self.screen.setText(self.expression)
        self.layout_buttons = QGridLayout()
        
        self._createButtons()
        self.layout.addWidget(self.screen)
        self.layout.addLayout(self.layout_buttons)
        self.setLayout(self.layout)
        
        
    # def _create
    def _createButtons(self):
        #Button templates
        button_labels = [
            {"text": "0", "row": 3, "column":0},
            {"text": "1", "row": 2, "column":0},
            {"text": "2", "row": 2, "column":1},
            {"text": "3", "row": 2, "column":2},
            {"text": "4", "row": 1, "column":0},
            {"text": "5", "row": 1, "column":1},
            {"text": "6", "row": 1, "column":2},
            {"text": "7", "row": 0, "column":0},
            {"text": "8", "row": 0, "column":1},
            {"text": "9", "row": 0, "column":2},
            {"text": ".", "row": 3, "column":1},
            {"text": "÷", "row": 0, "column":3},
            {"text": "×", "row": 1, "column":3},
            {"text": "cls", "row": 3, "column":2},
            {"text": "+", "row": 2, "column":3},
            {"text": "=", "row": 3, "column":3}
        ]
        self.operators = ["×", "÷", "+", "-"]
        
        #Create buttons
        buttons = []
        for label in button_labels:
            button = QPushButton(label["text"])
            button.setStyleSheet("color: white; font-size: 15px;")
            button.clicked.connect(partial(self.manage_press, label["text"]))
            buttons.append(button)
            self.layout_buttons.addWidget(button, label["row"],label["column"])
        
    def manage_press(self, key_pressed:chr):
        if self.expression == "Invalid Expression":
            self.expression = ""
            
        if key_pressed == "=":
            self.compute()
            return
        
        if key_pressed == "cls":
            self.expression = ""
        elif key_pressed in self.operators:
            self.expression += " " + str(key_pressed) + " "
        else:
            self.expression += str(key_pressed)
        self.screen.setText(self.expression)
        
    def compute(self):
        terms = self.expression.split()
        answer = terms[0]
        #If start or end with operator, Error
        if terms[0] in self.operators or terms[-1] in self.operators:
            self.expression = "Invalid Expression"
        else:
            while(any(operator in terms for operator in self.operators)): #While operators remaining
                for term in terms:
                    if term in self.operators:
                        #Get operators and operands
                        index = terms.index(term)
                        operator_term = term
                        operand_1 = terms[index-1]
                        operand_2 = terms[index+1]
                        
                        #Calculate answer
                        if operator_term == "×":
                            answer = int(operand_1) * int(operand_2)
                        elif operator_term == "÷":
                            answer = int(operand_1) / int(operand_2)
                        elif operator_term == "+":
                            answer = int(operand_1) + int(operand_2)
                        elif operator_term == "-":
                            answer = int(operand_1) - int(operand_2)
                            
                        #Update terms
                        print(terms)
                        print(answer)
                        terms.pop(index)
                        terms.pop(index)
                        terms[index-1] = answer
                        print(terms)
        self.expression = str(answer)
        self.screen.setText(self.expression)
    
class Que:
    pass
  
if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator();
    calculator.show()
    sys.exit(app.exec())