import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: banner

    property var bridge
    property bool dismissed: false
    signal doctorRequested()

    visible: bridge.firstRunNeeded && !dismissed
    implicitHeight: visible ? column.implicitHeight + 24 : 0
    radius: 4
    color: Qt.alpha(bridge.warningColor, 0.08)
    border.color: bridge.warningColor
    border.width: 1

    ColumnLayout {
        id: column
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            Text {
                text: "FIRST RUN SETUP"
                color: bridge.warningColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 1.8
            }

            Text {
                text: "No shared CLI config was found. Configure a provider "
                    + "below, run Doctor, then start with the default dry run."
                color: bridge.textColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(11 * bridge.fontScale)
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }

            ApexButton {
                bridge: banner.bridge
                text: "Doctor"
                onClicked: {
                    bridge.runDoctor()
                    banner.doctorRequested()
                }
            }

            ApexButton {
                bridge: banner.bridge
                text: "Dismiss"
                onClicked: banner.dismissed = true
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ColumnLayout {
                spacing: 2

                Text {
                    text: "Provider"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(9 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                ComboBox {
                    id: setupProvider
                    model: bridge.setupProviders
                    font.family: bridge.fontFamily
                    Layout.preferredWidth: 130
                    Accessible.name: "Setup provider"
                }
            }

            ColumnLayout {
                spacing: 2
                Layout.fillWidth: true

                Text {
                    text: "Model (blank keeps the provider default)"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(9 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                TextField {
                    id: setupModel
                    placeholderText: "Model"
                    placeholderTextColor: bridge.mutedColor
                    color: bridge.textColor
                    font.family: bridge.fontFamily
                    background: Rectangle {
                        color: bridge.cellColor
                        border.color: setupModel.activeFocus
                            ? bridge.accentColor : bridge.borderColor
                        border.width: 1
                        radius: 3
                    }
                    Layout.fillWidth: true
                    Accessible.name: "Setup model"
                }
            }

            ColumnLayout {
                spacing: 2

                Text {
                    text: "Codex binary"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(9 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                TextField {
                    id: setupCodex
                    text: "codex"
                    placeholderText: "codex"
                    placeholderTextColor: bridge.mutedColor
                    color: bridge.textColor
                    font.family: bridge.fontFamily
                    background: Rectangle {
                        color: bridge.cellColor
                        border.color: setupCodex.activeFocus
                            ? bridge.accentColor : bridge.borderColor
                        border.width: 1
                        radius: 3
                    }
                    Layout.preferredWidth: 130
                    Accessible.name: "Setup Codex binary"
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ColumnLayout {
                spacing: 2
                Layout.fillWidth: true

                Text {
                    text: "Projects directory (optional)"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(9 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                TextField {
                    id: setupProjectsDir
                    placeholderText: "~/projects"
                    placeholderTextColor: bridge.mutedColor
                    color: bridge.textColor
                    font.family: bridge.fontFamily
                    background: Rectangle {
                        color: bridge.cellColor
                        border.color: setupProjectsDir.activeFocus
                            ? bridge.accentColor : bridge.borderColor
                        border.width: 1
                        radius: 3
                    }
                    Layout.fillWidth: true
                    Accessible.name: "Setup projects directory"
                }
            }

            ColumnLayout {
                spacing: 2
                Layout.fillWidth: true

                Text {
                    text: "Default target project (optional)"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(9 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                TextField {
                    id: setupDefaultProject
                    placeholderText: "Project path"
                    placeholderTextColor: bridge.mutedColor
                    color: bridge.textColor
                    font.family: bridge.fontFamily
                    background: Rectangle {
                        color: bridge.cellColor
                        border.color: setupDefaultProject.activeFocus
                            ? bridge.accentColor : bridge.borderColor
                        border.width: 1
                        radius: 3
                    }
                    Layout.fillWidth: true
                    Accessible.name: "Setup default project"
                }
            }
        }

        Text {
            text: bridge.autonomyWarning + " Current mode: "
                + bridge.autonomySummary + " Codex flags: "
                + bridge.codexFlagsText + "."
            color: bridge.warningColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ApexToggle {
                id: confirmWrite
                bridge: banner.bridge
                text: "I confirm writing the shared CLI config"
                checked: false
            }

            ApexButton {
                bridge: banner.bridge
                text: "Write shared config"
                primary: true
                enabled: confirmWrite.checked
                Accessible.name: "Write shared config"
                onClicked: bridge.writeSharedConfig(
                    setupProvider.currentText,
                    setupModel.text,
                    setupCodex.text,
                    setupProjectsDir.text,
                    setupDefaultProject.text,
                    "")
            }

            Item { Layout.fillWidth: true }
        }

        Text {
            visible: bridge.setupError.length > 0
            text: bridge.setupError
            color: bridge.errorColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }

        Text {
            visible: bridge.setupWrittenPath.length > 0
            text: "Shared config written to " + bridge.setupWrittenPath
                + ". A backup of any previous config was preserved. "
                + "Run Doctor, then start the default dry run."
            color: bridge.accentColor
            font.family: bridge.fontFamily
            font.pixelSize: Math.round(10 * bridge.fontScale)
            wrapMode: Text.Wrap
            Layout.fillWidth: true
        }
    }
}
