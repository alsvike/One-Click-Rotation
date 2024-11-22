import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, 
    QDialog, QMessageBox, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import keyboard

# Predefined list of valid keys
VALID_KEYS = {
    'Letter Keys': [chr(i) for i in range(ord('a'), ord('z') + 1)],
    'Number Keys': [str(i) for i in range(10)] + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    'Function Keys': [f'f{i}' for i in range(1, 13)],
    'Special Keys': ['space', 'tab', 'shift', 'ctrl', 'alt', 'enter', 'backspace', 
                    'delete', 'insert', 'home', 'end', 'pageup', 'pagedown', 
                    'up', 'down', 'left', 'right', 'esc'],
    'Other Keys': ['½', '¾', '`', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/']
}

def is_valid_key(key):
    """Validate if a key is supported by the keyboard library"""
    all_valid_keys = []
    for category in VALID_KEYS.values():
        all_valid_keys.extend(category)
    return key.lower() in [k.lower() for k in all_valid_keys]

class KeyListener(QThread):
    key_pressed = pyqtSignal(str)
    
    def __init__(self, trigger_key):
        super().__init__()
        self.trigger_key = trigger_key
        self.running = True
        
    def run(self):
        try:
            while self.running:
                keyboard.wait(self.trigger_key)
                if self.running:  # Check again to prevent emit after stopping
                    self.key_pressed.emit(self.trigger_key)
        except Exception as e:
            print(f"Error in key listener: {str(e)}")
    
    def stop(self):
        self.running = False
        keyboard.press_and_release('esc')  # Break the wait() loop

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Configuration")
        self.setMinimumWidth(500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Name input
        name_label = QLabel("Configuration Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Example: My Rotation")
        
        # Trigger key selector
        trigger_label = QLabel("Macro Trigger Key:")
        self.trigger_combo = QComboBox()
        self.populate_key_dropdown(self.trigger_combo)
        
        # Sequence input with key selector
        sequence_label = QLabel("Action Sequence:")
        self.sequence_layout = QVBoxLayout()
        self.sequence_widgets = []
        self.add_sequence_key()  # Add first key by default
        
        # Add/Remove sequence key buttons
        sequence_buttons = QHBoxLayout()
        add_key_btn = QPushButton("Add Key")
        add_key_btn.clicked.connect(self.add_sequence_key)
        remove_key_btn = QPushButton("Remove Key")
        remove_key_btn.clicked.connect(self.remove_sequence_key)
        sequence_buttons.addWidget(add_key_btn)
        sequence_buttons.addWidget(remove_key_btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        # Add widgets to layouts
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(trigger_label)
        layout.addWidget(self.trigger_combo)
        layout.addWidget(sequence_label)
        layout.addLayout(self.sequence_layout)
        layout.addLayout(sequence_buttons)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def populate_key_dropdown(self, combo):
        for category, keys in VALID_KEYS.items():
            combo.addItem(f"--- {category} ---")
            for key in sorted(keys):
                combo.addItem(key)
    
    def add_sequence_key(self):
        key_combo = QComboBox()
        self.populate_key_dropdown(key_combo)
        self.sequence_widgets.append(key_combo)
        self.sequence_layout.addWidget(key_combo)
    
    def remove_sequence_key(self):
        if len(self.sequence_widgets) > 1:  # Always keep at least one key
            widget = self.sequence_widgets.pop()
            widget.deleteLater()
    
    def get_config(self):
        sequence = [widget.currentText() for widget in self.sequence_widgets 
                   if not widget.currentText().startswith('---')]
        return {
            'name': self.name_input.text(),
            'sequence': sequence,
            'trigger': self.trigger_combo.currentText()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("One-Click Rotation")
        self.setMinimumSize(800, 600)
        self.configs = []
        self.current_sequence = []
        self.sequence_index = 0
        self.key_listener = None
        self.is_rotation_active = False
        self.setup_ui()
        self.load_configs()
        
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Left panel (configurations)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Config list
        self.config_list = QListWidget()
        self.config_list.itemSelectionChanged.connect(self.on_config_selected)
        
        # Buttons
        create_btn = QPushButton("Create Config")
        create_btn.clicked.connect(self.create_config)
        delete_btn = QPushButton("Delete Config")
        delete_btn.clicked.connect(self.delete_config)
        
        left_layout.addWidget(QLabel("Configurations:"))
        left_layout.addWidget(self.config_list)
        left_layout.addWidget(create_btn)
        left_layout.addWidget(delete_btn)
        
        # Right panel (console and controls)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: monospace;
            }
        """)
        
        # Control buttons
        self.start_btn = QPushButton("Start Rotation")
        self.start_btn.clicked.connect(self.toggle_rotation)
        self.start_btn.setEnabled(False)
        
        right_layout.addWidget(QLabel("Console Output:"))
        right_layout.addWidget(self.console)
        right_layout.addWidget(self.start_btn)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")
    
    def create_config(self):
        dialog = ConfigDialog(self)
        if dialog.exec_():
            config = dialog.get_config()
            if not config['name'] or not config['sequence'] or not config['trigger']:
                QMessageBox.warning(self, "Error", "All fields are required!")
                return
            
            # Validate all keys
            invalid_keys = []
            for key in config['sequence']:
                if not is_valid_key(key):
                    invalid_keys.append(key)
            
            if invalid_keys:
                QMessageBox.warning(self, "Error", 
                    f"The following keys are not valid: {', '.join(invalid_keys)}")
                return
            
            self.configs.append(config)
            self.config_list.addItem(config['name'])
            self.save_configs()
            self.log_message(f"Created new configuration: {config['name']}")
    
    def delete_config(self):
        current_row = self.config_list.currentRow()
        if current_row >= 0:
            config_name = self.configs[current_row]['name']
            self.configs.pop(current_row)
            self.config_list.takeItem(current_row)
            self.save_configs()
            self.log_message(f"Deleted configuration: {config_name}")
    
    def save_configs(self):
        try:
            with open('configs.json', 'w') as f:
                json.dump(self.configs, f)
        except Exception as e:
            self.log_message(f"Error saving configs: {str(e)}")
    
    def load_configs(self):
        try:
            with open('configs.json', 'r') as f:
                self.configs = json.load(f)
                for config in self.configs:
                    self.config_list.addItem(config['name'])
        except FileNotFoundError:
            self.log_message("No saved configurations found")
        except Exception as e:
            self.log_message(f"Error loading configs: {str(e)}")
    
    def on_config_selected(self):
        self.start_btn.setEnabled(True)
        if self.key_listener and self.key_listener.isRunning():
            self.toggle_rotation()
    
    def toggle_rotation(self):
        if not self.is_rotation_active:
            current_row = self.config_list.currentRow()
            if current_row >= 0:
                config = self.configs[current_row]
                self.current_sequence = config['sequence']
                self.sequence_index = 0  # Reset index when starting
                
                try:
                    self.key_listener = KeyListener(config['trigger'].lower())
                    self.key_listener.key_pressed.connect(self.execute_next_action)
                    self.key_listener.start()
                    
                    self.is_rotation_active = True
                    self.start_btn.setText("Stop Rotation")
                    self.log_message(f"Started rotation: {config['name']}")
                except Exception as e:
                    self.log_message(f"Error starting rotation: {str(e)}")
                    QMessageBox.warning(self, "Error", 
                        f"Failed to start rotation: {str(e)}")
        else:
            if self.key_listener:
                self.key_listener.stop()
                self.key_listener.wait()
                self.key_listener = None
            self.is_rotation_active = False
            self.start_btn.setText("Start Rotation")
            self.log_message("Stopped rotation")
    
    def execute_next_action(self):
        if not self.current_sequence:
            return
            
        try:
            key = self.current_sequence[self.sequence_index]
            keyboard.press_and_release(key)
            self.log_message(f"Executed key: {key}")
            
            self.sequence_index = (self.sequence_index + 1) % len(self.current_sequence)
        except Exception as e:
            self.log_message(f"Error executing key: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()