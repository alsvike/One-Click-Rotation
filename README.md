# One-Click Rotation for Gamers

## Overview

**One-Click Rotation** is a gaming tool designed for players looking to streamline their gameplay with custom key rotations. Whether you’re managing skill combos in an MMO, executing complex macros in RPGs, or automating repetitive key sequences, this tool provides a simple, effective way to enhance your gaming experience.

With an intuitive interface and full control over key configurations, you can optimize your gaming performance by executing a sequence of keypresses with a single trigger key. Stay focused on gameplay while the tool handles the heavy lifting for you!

## Features

- **Custom Key Rotations**: Create tailored keypress sequences for specific in-game actions or combos.
- **Trigger Keys**: Assign a single key to start and control your custom rotation.
- **Key Validation**: Ensures all configured keys are compatible with the tool.
- **Console Feedback**: Get real-time logs of key actions for easy debugging and monitoring during gameplay.
- **Save and Manage Configurations**: Quickly switch between setups for different games or characters.
- **Dark Gaming Theme**: The sleek interface is designed to match your gaming setup.

## Requirements

- **Platform**: Compatible with Windows.
- **Python Version**: Python 3.x.
- **Libraries**: PyQt5, keyboard.

## Installation

1. Clone the repository to your gaming PC:

   ```bash
   git clone https://github.com/username/One-Click-Rotation.git
   ```

2. Install required libraries:

   ```bash
   pip install pyqt5 keyboard
   ```

3. Launch the tool:

   ```bash
   python main.py
   ```

## How to Use

### Setting Up a Rotation

1. **Create a New Config**:
   - Click **Create Config**.
   - Enter a name (e.g., "Mage Combo").
   - Select a trigger key (e.g., `F2`) (Key that will act as the one button to press)
   - Add keys to the action sequence (e.g., `1`, `2`, `3` for skill rotation).
   - Save your configuration.

2. **Start a Rotation**:
   - Select your configuration from the list.
   - Press **Start Rotation** to activate the macro.
   - Use the trigger key to cycle through your configured actions in-game.

3. **Stop a Rotation**:
   - Press **Stop Rotation** to halt the macro.

### Pro Tips

- Create separate configs for different characters or game scenarios.
- Use keys that won’t conflict with normal gameplay for your trigger and actions.
- Pair the tool with window-specific processes (planned feature) to make macros game-specific.

## Screenshots

![Main Window](./assets/main_window.png)
![Create Config Window](./assets/create_config_window.png)

## Planned Features

#### Game Profiles
- Allow users to create profiles for specific games.
- Each profile could store multiple configurations tailored to different characters, game modes, or scenarios.

#### Dynamic Rotation Adjustments
- Enable users to modify key rotations mid-game without stopping the tool.
  - Add/remove keys on-the-fly.
  - Rearrange the sequence order dynamically.

#### Mouse Movement and Clicks
- Support mouse actions, such as:
  - Simulated mouse movements for aiming or repositioning.
  - Left/right/middle mouse clicks as part of a sequence.

#### Combo Keys
- Support for combinations like `Shift+1` or `Ctrl+Q` for advanced macro setups.

#### Multi-Key Triggers
- Allow multiple keys to act as a trigger (e.g., pressing `Shift+F1` starts a rotation).

#### ~Ability to Edit Configurations~
~- Modify existing configurations for flexibility.~ $${\color{green}ADDED!}$$ Check out the new version!

#### Support for Mouse Buttons
- Use mouse buttons as triggers or action keys for advanced gameplay setups.

#### Window-Specific Macros
- Link macros to specific games, ensuring they only run when the game is active.

#### Visual Key Mapping
- Include a graphical interface to drag-and-drop keys into a sequence or map actions to keys visually.

#### Sound Alerts
- Play sounds when:
  - A macro starts or stops.
  - An error occurs (e.g., invalid key).

#### Backup and Import/Export
- Enable exporting configurations as files for sharing or backups.

#### Error Handling and Logs
- Add more robust error handling with detailed logs to troubleshoot issues when a macro doesn’t execute as expected.


## Known Bugs

- The application may temporarily freeze when stopping a macro during gameplay. Restart if needed.

## Example Use Cases

- **MMORPG**: Automate skill rotations to maximize DPS.
- **MOBA**: Quickly execute combos for heroes with complex keybinds.
- **RPG**: Chain potion usage and ability triggers for tough battles.
- **Sandbox Games**: Automate repetitive building or crafting actions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
