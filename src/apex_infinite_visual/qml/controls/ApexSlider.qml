import QtQuick
import QtQuick.Controls

Slider {
    id: control

    property var bridge

    implicitHeight: 24

    background: Rectangle {
        x: control.leftPadding
        y: control.topPadding + control.availableHeight / 2 - height / 2
        width: control.availableWidth
        height: 4
        radius: 2
        color: bridge.cellColor
        border.color: bridge.borderColor
        border.width: 1

        Rectangle {
            width: control.visualPosition * parent.width
            height: parent.height
            radius: 2
            color: bridge.accentColor
            opacity: 0.8
        }
    }

    handle: Rectangle {
        x: control.leftPadding + control.visualPosition
            * (control.availableWidth - width)
        y: control.topPadding + control.availableHeight / 2 - height / 2
        width: 14
        height: 14
        radius: 7
        color: bridge.backgroundColor
        border.color: bridge.accentColor
        border.width: 2
    }
}
