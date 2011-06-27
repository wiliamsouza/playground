function urlChanged(url) {
    var mUrl = url.toString();
    if (mUrl.indexOf("https://foursquare.com/img/categories/travel/busstation.png#") > -1) {
        console.log(mUrl.substring(mUrl.indexOf('=') + 1));
        return mUrl.substring(mUrl.indexOf('=') + 1);
    } else {
        return "";
    }
}
