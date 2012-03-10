import QtQuick 1.1
import com.nokia.meego 1.0

Item {
    id : icgb
    property real margin : 0
    property real iconSize : 100
    property alias iconName : themedIcon.iconName
    property alias color : background.color
    property alias sensitive : mouseArea.enabled
    property string text : ""
    signal clicked

    scale : mouseArea.pressed ? 0.9 : 1.0
    //transform: Scale { origin.x: 25; origin.y: 25; xScale: 3}

    width : iconSize
    height : iconSize
    // background
    Rectangle {
        id : background
        anchors.horizontalCenter : icgb.horizontalCenter
        anchors.margins : icgb.margin/2.0
        width : icgb.iconSize-icgb.margin/2.0
        height : icgb.iconSize-icgb.margin/2.0
        // TODO: get color from theme
        //color : mouseArea.pressed ? "black" : "#92aaf3"
        color : "#92aaf3"
        radius : 10
        smooth : true

        // icon
        TIcon {
            id: themedIcon
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.top : parent.top
            anchors.bottom : iconLabel.top
            anchors.right : parent.right
            anchors.left : parent.left
            iconName : icon
            anchors.margins : icgb.margin
            width : parent.width-icgb.margin
            height : parent.height-icgb.margin
        }
        // caption
        Label {
            id : iconLabel
            text : icgb.text
            font.pixelSize : rWin.inPortrait ? 42 : 36
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.bottom : parent.bottom
            anchors.bottomMargin : icgb.margin/1.5
        }
    }
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: icgb.clicked()
    }
}