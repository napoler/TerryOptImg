# FR-008: Comprehensive Settings Page

> **Version**: 1.0
> **Status**: Proposed
> **Priority**: Medium

## 1. Overview
Add a dedicated Settings Page to the TerryOptImg application to allow users to configure comprehensive application settings, including defaults for optimization, appearance, and system behaviors.

## 2. User Stories
- **US-001**: As a user, I want to open a settings window so that I can configure the application without cluttering the main interface.
- **US-002**: As a user, I want to set default values for Quality and Concurrency so that I don't have to change them every time I launch the app.
- **US-003**: As a user, I want to adjust the UI scaling manually in case the automatic detection is incorrect.
- **US-004**: As a user, I want to choose the application language (English/Chinese).

## 3. Functional Requirements

### 3.1 Settings Dialog
- **FR-008-001**: A modal dialog window titled "Settings".
- **FR-008-002**: The dialog shall be accessible via a "Settings" button on the main interface.
- **FR-008-003**: The dialog shall have categorized settings (e.g., General, Optimization, Appearance).

### 3.2 Configuration Categories
- **FR-008-004**: **General**:
    - Language Selection (English, Chinese).
    - Check for Updates (Toggle).
- **FR-008-005**: **Optimization Defaults**:
    - Default Quality (Slider/Spinbox).
    - Default Workers (Spinbox).
    - Default Format (Dropdown).
- **FR-008-006**: **Appearance**:
    - UI Scale Factor (Entry/Slider, 0.5x to 3.0x).
    - Theme (Light/Dark - Optional/Future).

### 3.3 Persistence
- **FR-008-007**: Settings shall be saved to `config.json` immediately upon confirmation or closing.
- **FR-008-008**: The application shall load these settings on startup.

## 4. Technical Constraints
- Must use `tkinter` / `ttk`.
- Must be compatible with existing `config.json` structure (or migrate gracefully).
- UI Scaling changes might require a restart to take full effect (user should be notified).

## 5. Acceptance Criteria
- [ ] Settings button opens the dialog.
- [ ] Changes in Settings (e.g., Default Quality) are reflected when the app is restarted or when the user resets the main UI.
- [ ] Config file is updated correctly.
