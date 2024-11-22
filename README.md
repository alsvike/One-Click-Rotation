# One-Click Rotation

## Overview

The **One-Click Rotation** application allows users to configure and execute keypress macros. This tool is designed for automating repetitive tasks by triggering a sequence of keystrokes with a single button press. It features a graphical user interface (GUI) powered by PyQt5, where users can create, manage, and execute key rotation configurations with ease.

The application supports both basic and advanced key configuration and validation. Users can specify a macro's trigger key, define a sequence of actions, and instantly execute the sequence with a dedicated trigger key. The tool uses the **keyboard** library to simulate keypresses.

## Features

- **Create Custom Macros**: Users can define their keypress sequences and associate them with a specific trigger key.
- **Key Validation**: The app validates the sequence of keys to ensure they are compatible with the keyboard library.
- **Real-time Console**: Outputs keypress actions and status updates in real-time via a built-in console.
- **Start/Stop Rotation**: Users can start or stop the macro rotation at any time.
- **Configuration Management**: Save, load, and delete macros easily through a list interface.
- **Dark Theme**: The app comes with a custom dark theme for a better user experience.

## Requirements

- Python 3.x
- PyQt5
- keyboard
- A working keyboard and operating system

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/username/One-Click-Rotation.git
   ```

2. Install required libraries using pip:

   ```bash
   pip install pyqt5 keyboard
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Usage

### Creating a New Configuration

- Open the application and click on **Create Config**.
- Enter a name for your configuration.
- Select a trigger key (the key that will start your rotation).
- Define the action sequence by selecting keys for the macro.
- Click **Save** to save your configuration.

### Starting the Rotation

- Select a configuration from the list.
- Click **Start Rotation** to begin the sequence of keypresses.
- The application will simulate keypresses as defined in your sequence, and it will loop through the sequence until you stop it.

### Stopping the Rotation

- To stop the rotation, click **Stop Rotation**. The application will stop listening for the trigger key and halt the keypress sequence.

## Screenshots

![Main Window](./assets/main_window.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
