import Qt 4.7

ListView {
    id: pythonList
    width: 400
    height: 200

    model: pythonListModel

    delegate: Component {
        Rectangle {
            width: pythonList.width
            height: 40
            color: ((index % 2 == 0)?"#222":"#111")

            Item {
                width: 400; height: 40

                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.thing.name
                        color: "white"
                        font.bold: true
                        anchors.leftMargin: 10
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                    }
                    Text {
                        id: subtitle
                        elide: Text.ElideRight
                        text: model.thing.description
                        color: "red"
                        anchors.leftMargin: 10
                        anchors.topMargin: 25
                        anchors.fill: parent
                        verticalAlignment: Text.AlignBottom
                    }
                
            }



            MouseArea {
                anchors.fill: parent
                onClicked: { controller.thingSelected(model.thing) }
            }
        }
    }
}