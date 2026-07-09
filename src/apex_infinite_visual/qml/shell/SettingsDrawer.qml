import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../controls"

Drawer {
    id: drawer

    property var bridge

    edge: Qt.RightEdge
    width: Math.min(400, parent ? parent.width * 0.45 : 400)
    height: parent ? parent.height : 600

    background: Rectangle {
        color: bridge.panelColor
        border.color: bridge.borderColor
        border.width: 1
    }

    Flickable {
        anchors.fill: parent
        anchors.margins: 14
        contentWidth: width
        contentHeight: column.implicitHeight + 20
        clip: true

        ColumnLayout {
            id: column
            width: parent.width
            spacing: 10

            Text {
                text: "VISUAL PROFILE"
                color: bridge.accentColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(13 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.0
            }

            Text {
                text: "Theme"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 1.4
            }

            ComboBox {
                model: bridge.themeNames
                currentIndex: bridge.themeNames.indexOf(bridge.themeName)
                font.family: bridge.fontFamily
                Layout.fillWidth: true
                Accessible.name: "Theme"
                onActivated: bridge.setTheme(currentText)
            }

            Text {
                text: "Rendering mode"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 1.4
            }

            ComboBox {
                model: bridge.renderingModes
                currentIndex: bridge.renderingModes.indexOf(bridge.renderingMode)
                font.family: bridge.fontFamily
                Layout.fillWidth: true
                Accessible.name: "Rendering mode"
                onActivated: bridge.setRenderingMode(currentText)
            }

            Text {
                text: "Quality tier (recommended: " + bridge.recommendedTier + ")"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
                font.letterSpacing: 1.4
            }

            ComboBox {
                model: bridge.qualityTiers
                currentIndex: bridge.qualityTiers.indexOf(bridge.qualityTier)
                font.family: bridge.fontFamily
                Layout.fillWidth: true
                Accessible.name: "Quality tier"
                onActivated: bridge.setQualityTier(currentText)
            }

            Text {
                text: "Intensity " + bridge.effectIntensity + "%"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
            }

            ApexSlider {
                bridge: drawer.bridge
                from: 0
                to: 100
                stepSize: 5
                value: bridge.effectIntensity
                enabled: !bridge.plainFallback
                Layout.fillWidth: true
                Accessible.name: "Effect intensity"
                onMoved: bridge.setEffectIntensity(Math.round(value))
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 14

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Reduced effects"
                    checked: bridge.reducedEffects
                    onToggled: function(value) { bridge.setReducedEffects(value) }
                }

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Plain fallback"
                    checked: bridge.plainFallback
                    onToggled: function(value) { bridge.setPlainFallback(value) }
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 2
                columnSpacing: 14
                rowSpacing: 8

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Glow"
                    checked: bridge.glowEnabled
                    enabled: !bridge.reducedEffects && !bridge.plainFallback
                    onToggled: function(value) {
                        bridge.setEffectEnabled("glow", value)
                    }
                }

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Scanlines"
                    checked: bridge.scanlinesEnabled
                    enabled: !bridge.reducedEffects && !bridge.plainFallback
                    onToggled: function(value) {
                        bridge.setEffectEnabled("scanlines", value)
                    }
                }

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Flicker"
                    checked: bridge.flickerEnabled
                    enabled: !bridge.reducedEffects && !bridge.plainFallback
                    onToggled: function(value) {
                        bridge.setEffectEnabled("flicker", value)
                    }
                }

                ApexToggle {
                    bridge: drawer.bridge
                    text: "Curvature"
                    checked: bridge.curvatureEnabled
                    enabled: !bridge.reducedEffects && !bridge.plainFallback
                    onToggled: function(value) {
                        bridge.setEffectEnabled("curvature", value)
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: bridge.borderColor
            }

            Text {
                text: "TYPE"
                color: bridge.accentColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.0
            }

            ComboBox {
                model: bridge.fontFamilies
                currentIndex: bridge.fontFamilies.indexOf(bridge.fontFamily)
                font.family: bridge.fontFamily
                Layout.fillWidth: true
                Accessible.name: "Font family"
                onActivated: bridge.setFontFamily(currentText)
            }

            Text {
                text: "Scale " + Math.round(bridge.fontScale * 100) + "%"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
            }

            ApexSlider {
                bridge: drawer.bridge
                from: 0.8
                to: 1.4
                stepSize: 0.05
                value: bridge.fontScale
                Layout.fillWidth: true
                Accessible.name: "Font scale"
                onMoved: bridge.setFontScale(value)
            }

            Text {
                text: "Line spacing " + Math.round(bridge.lineSpacing * 100) + "%"
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(10 * bridge.fontScale)
            }

            ApexSlider {
                bridge: drawer.bridge
                from: 0.9
                to: 1.6
                stepSize: 0.05
                value: bridge.lineSpacing
                Layout.fillWidth: true
                Accessible.name: "Line spacing"
                onMoved: bridge.setLineSpacing(value)
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: bridge.borderColor
            }

            Text {
                text: "PROFILES"
                color: bridge.accentColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.0
            }

            ComboBox {
                id: profileBox
                model: bridge.profileNames
                font.family: bridge.fontFamily
                Layout.fillWidth: true
                Accessible.name: "Profile"
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                ApexButton {
                    bridge: drawer.bridge
                    text: "Load"
                    enabled: profileBox.currentText.length > 0
                    onClicked: bridge.loadProfile(profileBox.currentText)
                }

                ApexButton {
                    bridge: drawer.bridge
                    text: "Delete"
                    danger: true
                    enabled: profileBox.currentText.length > 0
                    onClicked: bridge.deleteProfile(profileBox.currentText)
                }
            }

            TextField {
                id: newProfileName
                placeholderText: "New profile name"
                placeholderTextColor: bridge.mutedColor
                color: bridge.textColor
                font.family: bridge.fontFamily
                background: Rectangle {
                    color: bridge.cellColor
                    border.color: newProfileName.activeFocus
                        ? bridge.accentColor : bridge.borderColor
                    border.width: 1
                    radius: 3
                }
                Layout.fillWidth: true
                Accessible.name: "New profile name"
            }

            ApexButton {
                bridge: drawer.bridge
                text: "Save current as profile"
                primary: true
                enabled: newProfileName.text.trim().length > 0
                Layout.fillWidth: true
                onClicked: bridge.saveProfile(newProfileName.text.trim())
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                ApexButton {
                    bridge: drawer.bridge
                    text: "Duplicate"
                    enabled: profileBox.currentText.length > 0
                        && newProfileName.text.trim().length > 0
                    onClicked: bridge.duplicateProfile(
                        profileBox.currentText, newProfileName.text.trim())
                }

                ApexButton {
                    bridge: drawer.bridge
                    text: "Rename"
                    enabled: profileBox.currentText.length > 0
                        && newProfileName.text.trim().length > 0
                    onClicked: bridge.renameProfile(
                        profileBox.currentText, newProfileName.text.trim())
                }

                ApexButton {
                    bridge: drawer.bridge
                    text: "Reset built-in"
                    enabled: profileBox.currentText.length > 0
                    onClicked: bridge.resetProfile(profileBox.currentText)
                }
            }

            Text {
                text: "Duplicate and Rename use the name field above. Reset "
                    + "restores a built-in profile to its shipped values."
                color: bridge.mutedColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(9 * bridge.fontScale)
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }

            TextField {
                id: profileFilePath
                placeholderText: "Profile JSON path (import/export)"
                placeholderTextColor: bridge.mutedColor
                color: bridge.textColor
                font.family: bridge.fontFamily
                background: Rectangle {
                    color: bridge.cellColor
                    border.color: profileFilePath.activeFocus
                        ? bridge.accentColor : bridge.borderColor
                    border.width: 1
                    radius: 3
                }
                Layout.fillWidth: true
                Accessible.name: "Profile JSON path"
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                ApexButton {
                    bridge: drawer.bridge
                    text: "Import"
                    enabled: profileFilePath.text.trim().length > 0
                    onClicked: bridge.importProfile(profileFilePath.text.trim())
                }

                ApexButton {
                    bridge: drawer.bridge
                    text: "Export"
                    enabled: profileBox.currentText.length > 0
                        && profileFilePath.text.trim().length > 0
                    onClicked: bridge.exportProfile(
                        profileBox.currentText, profileFilePath.text.trim())
                }
            }

            Text {
                visible: bridge.profileError.length > 0
                text: bridge.profileError
                color: bridge.errorColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(11 * bridge.fontScale)
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: bridge.borderColor
            }

            Text {
                text: "DOCTOR"
                color: bridge.accentColor
                font.family: bridge.fontFamily
                font.pixelSize: Math.round(12 * bridge.fontScale)
                font.bold: true
                font.letterSpacing: 2.0
            }

            ApexButton {
                bridge: drawer.bridge
                text: "Run diagnostics"
                Layout.fillWidth: true
                onClicked: bridge.runDoctor()
            }

            Repeater {
                model: bridge.doctorRows

                Rectangle {
                    required property var modelData
                    Layout.fillWidth: true
                    implicitHeight: doctorRow.implicitHeight + 12
                    radius: 3
                    color: bridge.cellColor
                    border.color: modelData.status === "fail"
                        ? bridge.errorColor
                        : modelData.status === "warn"
                            ? bridge.warningColor : bridge.borderColor
                    border.width: 1

                    RowLayout {
                        id: doctorRow
                        anchors.fill: parent
                        anchors.margins: 6
                        spacing: 8

                        Text {
                            text: modelData.status.toUpperCase()
                            color: modelData.status === "fail"
                                ? bridge.errorColor
                                : modelData.status === "warn"
                                    ? bridge.warningColor : bridge.accentColor
                            font.family: bridge.fontFamily
                            font.pixelSize: Math.round(10 * bridge.fontScale)
                            font.bold: true
                            Layout.preferredWidth: 42
                        }

                        ColumnLayout {
                            spacing: 1
                            Layout.fillWidth: true

                            Text {
                                text: modelData.label
                                color: bridge.textColor
                                font.family: bridge.fontFamily
                                font.pixelSize: Math.round(11 * bridge.fontScale)
                                Layout.fillWidth: true
                            }

                            Text {
                                text: modelData.detail
                                color: bridge.mutedColor
                                font.family: bridge.fontFamily
                                font.pixelSize: Math.round(10 * bridge.fontScale)
                                wrapMode: Text.Wrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                }
            }
        }
    }
}
