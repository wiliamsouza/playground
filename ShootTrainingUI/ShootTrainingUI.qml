import QtQuick 1.0
import QtMultimediaKit 1.1

Rectangle {
    id : cameraUI
    width: 360
    height: 360
    state: "PhotoCapture"

    states: [
        State {
            name: "PhotoCapture"
            StateChangeScript {
                script: {
                    camera.visible = true
                    camera.focus = true
                    //stillControls.visible = true
                    photoPreview.visible = false
                }
            }
        },
        State {
            name: "PhotoPreview"
            StateChangeScript {
                script: {
                    camera.visible = false
                    //stillControls.visible = false
                    photoPreview.visible = true
                    photoPreview.focus = true
                }
            }
        }
    ]

    Item {
        id: photoPreview
        property alias source : preview.source
        signal closed

        Image {
            id: preview
            anchors.fill : parent
            fillMode: Image.PreserveAspectFit
            smooth: true
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                parent.closed();
            }
        }
    }

    Camera {
        id: camera
        width: 360
        height: 300
        focus : visible

        flashMode: Camera.FlashRedEyeReduction
        whiteBalanceMode:  Camera.WhiteBalanceFlash
        exposureCompensation: -1.0

        onImageCaptured : {
            photoPreview.source = preview
            cameraUI.state = "PhotoPreview"
        }
    }

    Rectangle {
        id: take
        height: 30
        width: 100
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        color: "black"

        Text {
            id: takephoto
            anchors.centerIn: parent
            color: "white"
            text: "Take a Photo"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                camera.captureImage()
                console.log("taking a pic")
            }
        }
    }
}
