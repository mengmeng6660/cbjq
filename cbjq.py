import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QDialog, QSpinBox)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt

blocks = [
    [[
        [1, 1],
        [1, 1]
    ]],
    [[
        [2, 2, 2, 2]
    ], [
        [2],
        [2],
        [2],
        [2]
    ]],
    [[
        [3, 3, 0],
        [0, 3, 3]
    ], [
        [0, 3],
        [3, 3],
        [3, 0]
    ]],
    [[
        [0, 4, 4],
        [4, 4, 0]
    ], [
        [4, 0],
        [4, 4],
        [0, 4]
    ]],
    [[
        [5, 0, 0],
        [5, 5, 5]
    ], [
        [5, 5],
        [5, 0],
        [5, 0]
    ], [
        [5, 5, 5],
        [0, 0, 5]
    ], [
        [0, 5],
        [0, 5],
        [5, 5]
    ]],
    [[
        [0, 6, 6],
        [6, 6, 6]
    ], [
        [6, 6],
        [0, 6],
        [0, 6]
    ], [
        [6, 6, 6],
        [6, 0, 0]
    ], [
        [6, 0],
        [6, 0],
        [6, 6]
    ]],
    [[
        [0, 7, 0],
        [7, 7, 7]
    ], [
        [7, 7, 7],
        [0, 7, 0]
    ], [
        [7, 0],
        [7, 7],
        [7, 0]
    ], [
        [0, 7],
        [7, 7],
        [0, 7]
    ]],
    [[
        [0, 8, 0],
        [8, 8, 8],
        [0, 8, 0]
    ]],
    [[
        [9]
    ]],
    [[
        [10, 10]
    ], [
        [10],
        [10]
    ]],
    [[
        [11, 11],
        [11, 0],
    ], [
        [11, 11],
        [0, 11],
    ], [
        [0, 11],
        [11, 11],
    ], [
        [11, 0],
        [11, 11],
    ]],
]

def canPlaceBlock(a, x, y, b, d, offset):
    y -= offset
    if y < 0:
        return False
    pat = blocks[b][d]
    for i in range(len(pat)):
        for j in range(len(pat[0])):
            if pat[i][j] and (x + i >= len(a) or y + j >= len(a[0]) or a[x + i][y + j] != -1):
                return False
    return True

def placeBlock(a, x, y, b, d, v, offset):
    y -= offset
    pat = blocks[b][d]
    for i in range(len(pat)):
        for j in range(len(pat[0])):
            if pat[i][j]:
                a[x + i][y + j] = v

def dfs(a, l, p, res):
    if p == len(a) * len(a[0]):
        x = [row[:] for row in a]
        res.append(x)
        if len(res) >= 1000:
            return True
        return False
    x = p // len(a[0])
    y = p % len(a[0])
    if a[x][y] != -1:
        return dfs(a, l, p + 1, res)
    for b in range(len(blocks)):
        if not l[b]:
            continue
        for d in range(len(blocks[b])):
            offset = 0
            while not blocks[b][d][0][offset]:
                offset += 1
            if not canPlaceBlock(a, x, y, b, d, offset):
                continue
            placeBlock(a, x, y, b, d, b + 1, offset)
            l[b] -= 1
            if dfs(a, l, p + 1, res):
                return True
            l[b] += 1
            placeBlock(a, x, y, b, d, -1, offset)
    return False

def solve(arr, num, strategy):
    res = []
    m, n = len(arr), len(arr[0])
    a = [row[:] for row in arr]
    l = num[:]
    dfs(a, l, 0, res)
    if strategy == 'small_first':
        res.sort(key=lambda x: (len(set(sum(x, []))), min(sum(x, []))))
    elif strategy == 'large_first':
        res.sort(key=lambda x: (-len(set(sum(x, []))), -max(sum(x, []))))

    return res


class SolutionDisplay(QWidget):
    def __init__(self, solutions, parent=None):
        super().__init__(parent)
        self.solutions = solutions
        self.current_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('求解结果')
        self.layout = QVBoxLayout()
        self.solution_label = QLabel(f"结果数量: {len(self.solutions)}")
        self.layout.addWidget(self.solution_label)

        self.solution_area = QGridLayout()
        self.layout.addLayout(self.solution_area)

        self.buttons_layout = QHBoxLayout()
        prev_button = QPushButton("上一个")
        prev_button.clicked.connect(self.showPrevSolution)
        self.buttons_layout.addWidget(prev_button)

        next_button = QPushButton("下一个")
        next_button.clicked.connect(self.showNextSolution)
        self.buttons_layout.addWidget(next_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)
        self.resize(400, 300)
        self.showSolution(self.current_index)

    def showSolution(self, index):
        for i in reversed(range(self.solution_area.count())):
            self.solution_area.itemAt(i).widget().setParent(None)

        solution = self.solutions[index]
        for i, row in enumerate(solution):
            for j, value in enumerate(row):
                label = QLabel(str(value))
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(50, 50)
                label.setStyleSheet(f"background-color: {self.getColor(value)}; color: black;")
                self.solution_area.addWidget(label, i, j)

        self.solution_label.setText(f"结果数量: {len(self.solutions)} (当前是第 {index + 1} 个)")

    def showPrevSolution(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.showSolution(self.current_index)

    def showNextSolution(self):
        if self.current_index < len(self.solutions) - 1:
            self.current_index += 1
            self.showSolution(self.current_index)

    def getColor(self, value):
        colors = ["#ffffff", "#ffcccc", "#ccffcc", "#ccccff", "#ccffff", "#ffccff", "#ffffcc", "#ffcc99", "#ffccff", "#cc99ff", "#cc99cc",
                  "#cccccc"]
        return colors[value] if value > 0 else "#ffffff"


class BlockFillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('信源研析')
        self.grid_rows, self.grid_cols = self.getGridSize()
        self.blocks_counts = []
        self.grid_layout = QGridLayout()
        self.grid_buttons = []
        self.createGrid()
        self.createControls()
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addLayout(self.controls_layout)
        self.setLayout(main_layout)
        self.resize(6, 800)

    def getGridSize(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()
        row_spin = QSpinBox()
        row_spin.setRange(1, 20)
        row_spin.setValue(5)
        col_spin = QSpinBox()
        col_spin.setRange(1, 20)
        col_spin.setValue(5)
        layout.addWidget(QLabel("行数:"))
        layout.addWidget(row_spin)
        layout.addWidget(QLabel("列数:"))
        layout.addWidget(col_spin)
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            return row_spin.value(), col_spin.value()
        else:
            sys.exit()

    def createGrid(self):
        self.grid_layout.setHorizontalSpacing(5)
        self.grid_layout.setVerticalSpacing(5)
        for i in range(self.grid_rows):
            row = []
            for j in range(self.grid_cols):
                btn = QPushButton("")
                btn.setFixedSize(50, 50)
                btn.setStyleSheet("background-color: white; color: black; border: 1px solid;")
                btn.clicked.connect(lambda _, i=i, j=j: self.toggleCell(i, j))
                self.grid_layout.addWidget(btn, i, j)
                row.append(btn)
            self.grid_buttons.append(row)

    def toggleCell(self, i, j):
        current = self.grid_buttons[i][j].text()
        new_value = "" if current != "" else "X"
        self.grid_buttons[i][j].setText(new_value)
        self.grid_buttons[i][j].setStyleSheet("background-color: #ffcccc; color: black; border: 1px solid;" if new_value == "X" else "background-color: white; color: black; border: 1px solid;")

    def createControls(self):
        self.controls_layout = QVBoxLayout()
        self.controls_layout.addWidget(QLabel("方块数量"))
        for i in range(len(blocks)):
            block_layout = QHBoxLayout()
            block_preview = BlockPreview(blocks[i][0], bg_color=self.getColor(i))
            block_layout.addWidget(block_preview)
            block_label = QLabel(f"方块 {i + 1} 的数量:")
            block_layout.addWidget(block_label)
            block_count = QLineEdit()
            block_layout.addWidget(block_count)
            self.blocks_counts.append(block_count)
            self.controls_layout.addLayout(block_layout)

        clear_button = QPushButton("清除")
        clear_button.clicked.connect(self.clearInputs)
        self.controls_layout.addWidget(clear_button)

        solve_small_button = QPushButton("小编号优先")
        solve_small_button.clicked.connect(lambda: self.solvePuzzle('small_first'))
        self.controls_layout.addWidget(solve_small_button)

        solve_large_button = QPushButton("大编号优先")
        solve_large_button.clicked.connect(lambda: self.solvePuzzle('large_first'))
        self.controls_layout.addWidget(solve_large_button)

    def clearInputs(self):
        for count in self.blocks_counts:
            count.clear()

    def solvePuzzle(self, strategy):
        try:
            block_counts = []
            for count in self.blocks_counts:
                if count.text() == "":
                    block_counts.append(0)
                else:
                    block_counts.append(int(count.text()))
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
            return

        grid = [[-1 if self.grid_buttons[i][j].text() == "" else 0 for j in range(self.grid_cols)] for i in
                range(self.grid_rows)]
        solution = solve(grid, block_counts, strategy)
        if solution:
            self.solution_display = SolutionDisplay(solution)
            self.solution_display.show()
        else:
            QMessageBox.information(self, "解决方案", "没有解法.")

    def getColor(self, value):
        colors = ["#ffffff", "#ffcccc", "#ccffcc", "#ccccff", "#ccffff", "#ffccff", "#ffffcc", "#ffcc99", "#ffccff", "#cc99ff", "#cc99cc", "#cccccc"]
        return colors[value] if value > 0 else "#ffffff"


class BlockPreview(QWidget):
    def __init__(self, block, bg_color=None, parent=None):
        super().__init__(parent)
        self.block = block
        self.setFixedSize(50, 50)
        self.bg_color = bg_color

    def paintEvent(self, event):
        painter = QPainter(self)
        block_size = 10
        for i in range(len(self.block)):
            for j in range(len(self.block[0])):
                if self.block[i][j]:
                    painter.fillRect(j * block_size, i * block_size, block_size, block_size, QBrush(QColor(self.bg_color)))
                    painter.setPen(QPen(Qt.black, 1))
                    painter.drawRect(j * block_size, i * block_size, block_size, block_size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BlockFillingApp()
    ex.show()
    sys.exit(app.exec_())
