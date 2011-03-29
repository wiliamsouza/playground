import QtQuick 1.0

Rectangle {
    width: 240
    height: 320

    ListView {
        anchors.fill: parent
        model: groupListModel
        delegate: Text {
            text: modelData.groupname
        }
    }
}
