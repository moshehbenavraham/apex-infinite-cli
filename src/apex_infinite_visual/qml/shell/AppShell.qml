import QtQuick
import QtQuick.Layouts
import "../effects"

Item {
    id: shell

    property var bridge

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 10

        CommandSurface {
            bridge: shell.bridge
            Layout.fillWidth: true
            onSettingsRequested: settingsDrawer.open()
        }

        FirstRunBanner {
            bridge: shell.bridge
            Layout.fillWidth: true
            onDoctorRequested: settingsDrawer.open()
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 10

            StatusRail {
                bridge: shell.bridge
                Layout.preferredWidth: 240
                Layout.fillHeight: true
            }

            RunConsole {
                bridge: shell.bridge
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            ColumnLayout {
                Layout.fillWidth: false
                Layout.preferredWidth: 250
                Layout.minimumWidth: 220
                Layout.maximumWidth: 280
                Layout.fillHeight: true
                spacing: 10

                SpecMap {
                    bridge: shell.bridge
                    Layout.fillWidth: true
                }

                SignalPanel {
                    bridge: shell.bridge
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }
            }
        }
    }

    EffectSurface {
        anchors.fill: parent
        bridge: shell.bridge
        z: 10
    }

    SettingsDrawer {
        id: settingsDrawer
        bridge: shell.bridge
    }
}
