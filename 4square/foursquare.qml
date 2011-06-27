import QtQuick 1.0
import QtWebKit 1.0

import "oauth.js" as OAuth
import "parser.js" as JS

Rectangle {
    id: window
    width: 640
    height: 360
    color: "gray"

    property string access_token: ""
    Component.onCompleted: JS.load()

    Text {
        id: token
        text: access_token
    }

    ListModel {  id:listModel }

    ListView {
        id:view
        anchors.fill:parent
        model : listModel
        delegate: Rectangle {
            width:parent.width
            height:80
            Row {
                spacing: 12
                Image {
                    source: photo
                    width: 80
                    height: 80
                }
                Text {
                    text: firstName
                }
                Text {
                    text: lastName
                }
                Text {
                    text: gender
                }
                Text {
                    text: homeCity
                }
                Text {
                    text: relationship
                }
            }
        }
    }

    Flickable {
        visible: false
        anchors.fill: parent
        contentWidth: loginView.width
        contentHeight: loginView.height

        WebView {
            id: loginView
            settings.javascriptEnabled: true
            url: "https://foursquare.com/oauth2/authenticate"+
                 "?display=touch"+
                 "&client_id=<YOUR_CLIENT_ID_HERE>"+
                 "&response_type=token"+
                 "&redirect_uri=https://foursquare.com/img/categories/travel/busstation.png"
            onUrlChanged: {
                if (OAuth.urlChanged(url) !== "")
                    window.access_token = OAuth.urlChanged(url)
            }
        }
    }

}
