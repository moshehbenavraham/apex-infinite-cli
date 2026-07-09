import QtQuick

Item {
    id: field

    property var bridge
    property real charge: 0.0

    visible: bridge && bridge.glowEnabled

    function sweep(strength) {
        charge = Math.min(1.0, strength)
        drain.restart()
    }

    function drainNow() {
        drain.stop()
        charge = 0.0
    }

    NumberAnimation {
        id: drain
        target: field
        property: "charge"
        to: 0.0
        duration: 1400
        easing.type: Easing.OutQuad
    }

    Rectangle {
        anchors.fill: parent
        color: bridge ? bridge.accentColor : "#6ee7a8"
        opacity: bridge
            ? (0.015 + bridge.effectOpacity * 0.05) + charge * 0.10
            : 0.0
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: bridge
                    ? Qt.alpha(bridge.accentColor, 0.04 + field.charge * 0.08)
                    : "transparent"
            }
            GradientStop { position: 0.25; color: "transparent" }
            GradientStop { position: 0.75; color: "transparent" }
            GradientStop {
                position: 1.0
                color: bridge
                    ? Qt.alpha(bridge.accentColor, 0.05 + field.charge * 0.08)
                    : "transparent"
            }
        }
    }
}
