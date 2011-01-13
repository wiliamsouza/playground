import QtQuick 1.0

ListView {
    id: unit_list
    width: 250
    height: 480
    model: unit_list_model
    delegate: Component {
        Rectangle {
            width: unit_list.width
            height: 50
            gradient : ((index % 2 == 0)? grad : grad2)
            Row {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 4
                children: [
                    Image {
                        id: icon
                        width: 16
                        height: 16
                        source: "icons/green.png"
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.leftMargin: 4
                    },
                    Column {
                        spacing: 2
                        anchors.verticalCenter: parent.verticalCenter
                        children: [
                            Text {
                                id: title
                                elide: Text.ElideRight
                                text: model.unit.id
                                color: "#383535"
                                font.bold: true
                                anchors.left: parent.left
                                anchors.leftMargin: 4
                            },
                            Text {
                                id: subtitle
                                elide: Text.ElideRight
                                text: model.unit.description
                                color: "#383535"
                                anchors.left: parent.left
                                anchors.leftMargin: 4
                            }
                        ]
                    }
                ]                
            }
            MouseArea {
                anchors.fill: parent
                onClicked: { unit_controller.unit_selected(model.unit) }
            }
        }
    }

        Gradient {
            id: grad
            GradientStop {
                position: 0.38
                color: "#85d1f9"
            }

            GradientStop {
                position: 1
                color: "#3881a8"
            }
        }

        Gradient {
            id: grad2
            GradientStop {
                position: 0.38
                color: "white"
            }

            GradientStop {
                position: 1
                color: "white"
            }
        }


        states: State {
            name: "ShowBars"
            when: unit_list.movingVertically
            PropertyChanges { target: verticalScrollBar; opacity: 1 }
        }

        ScrollBar {
            id: verticalScrollBar
            width: 12; height: unit_list.height-12
            anchors.right: unit_list.right
            opacity: 0
            orientation: Qt.Vertical
            position: unit_list.visibleArea.yPosition
            pageSize: unit_list.visibleArea.heightRatio
        }

}