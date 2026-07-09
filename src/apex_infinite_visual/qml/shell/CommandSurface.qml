import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls"

Rectangle {
    id: strip

    property var bridge
    signal settingsRequested()

    implicitHeight: layout.implicitHeight + 24
    radius: 4
    color: bridge.panelColor
    border.color: bridge.borderColor
    border.width: 1

    ColumnLayout {
        id: layout
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: "APEX INFINITE HYPERTERMINAL"
                color: bridge.accentColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(16 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.4
            }

            Rectangle {
                width: 8
                height: 8
                radius: 4
                color: bridge.runHealth === "failed"
                    ? bridge.errorColor
                    : bridge.running ? bridge.accentColor : bridge.mutedColor

                SequentialAnimation on opacity {
                    running: bridge.running
                    loops: Animation.Infinite
                    NumberAnimation { to: 0.3; duration: 600 }
                    NumberAnimation { to: 1.0; duration: 600 }
                }
            }

            Item { Layout.fillWidth: true }

            Text {
                text: bridge.autonomySummary
                color: bridge.dryRun ? bridge.mutedColor : bridge.warningColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(11 * bridge.fontScale)
                elide: Text.ElideRight
                Layout.maximumWidth: strip.width * 0.45
            }

            ApexButton {
                bridge: strip.bridge
                text: "Visual"
                onClicked: strip.settingsRequested()
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            TextField {
                id: projectField
                text: bridge.projectPath
                enabled: !bridge.running
                selectByMouse: true
                color: bridge.textColor
                placeholderText: "Project path"
                placeholderTextColor: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                background: Rectangle {
                    color: bridge.cellColor
                    border.color: projectField.activeFocus
                        ? bridge.accentColor : bridge.borderColor
                    border.width: 1
                    radius: 3
                }
                Layout.fillWidth: true
                Accessible.name: "Project path"
                onEditingFinished: bridge.setProjectPath(text)
            }

            TextField {
                id: commandField
                text: bridge.startCommand
                enabled: !bridge.running
                selectByMouse: true
                color: bridge.textColor
                placeholderText: "Start command"
                placeholderTextColor: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                background: Rectangle {
                    color: bridge.cellColor
                    border.color: commandField.activeFocus
                        ? bridge.accentColor : bridge.borderColor
                    border.width: 1
                    radius: 3
                }
                Layout.preferredWidth: 190
                Accessible.name: "Start command"
                onEditingFinished: bridge.setStartCommand(text)
            }

            ApexSegmentedControl {
                bridge: strip.bridge
                model: ["dry-run", "live"]
                currentValue: bridge.dryRun ? "dry-run" : "live"
                enabled: !bridge.running
                onSelected: function(value) { bridge.setDryRun(value === "dry-run") }
            }

            RowLayout {
                spacing: 4

                Text {
                    text: "MAX"
                    color: bridge.mutedColor
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(10 * bridge.fontScale)
                    font.letterSpacing: 1.2
                }

                SpinBox {
                    id: iterBox
                    from: 1
                    to: 50
                    value: bridge.maxIterations
                    enabled: !bridge.running
                    font.family: bridge.fontFamily
                    font.pixelSize: Math.round(12 * bridge.fontScale)
                    Accessible.name: "Max iterations"
                    onValueModified: bridge.setMaxIterations(value)
                }
            }

            ApexButton {
                bridge: strip.bridge
                text: bridge.running ? "Running" : "Start"
                primary: true
                enabled: !bridge.running
                Accessible.name: "Start run"
                onClicked: bridge.startRun()
            }

            ApexButton {
                bridge: strip.bridge
                text: "Stop"
                danger: true
                enabled: bridge.running
                Accessible.name: "Stop run"
                onClicked: bridge.stopRun()
            }

            ApexButton {
                bridge: strip.bridge
                text: "Doctor"
                enabled: !bridge.running
                Accessible.name: "Run doctor"
                onClicked: bridge.runDoctor()
            }
        }
    }
}
