function load() {

    listModel.clear();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://api.foursquare.com/v2/users/leaderboard?oauth_token=" + access_token, true);
    xhr.onreadystatechange = function()
    {
        if ( xhr.readyState == xhr.DONE)
        {
            if ( xhr.status == 200)
            {
                var jsonObject = eval('(' + xhr.responseText + ')');
                loaded(jsonObject);
            }
        }
    }
    xhr.send();
}

function loaded(jsonObject) {
    for (var index in jsonObject.response.leaderboard.items){
        listModel.append({
                         "id": jsonObject.response.leaderboard.items[index].user["id"],
                         "firstName": jsonObject.response.leaderboard.items[index].user["firstName"],
                         "lastName": jsonObject.response.leaderboard.items[index].user["lastName"],
                         "photo": jsonObject.response.leaderboard.items[index].user["photo"],
                         "gender": jsonObject.response.leaderboard.items[index].user["gender"],
                         "homeCity": jsonObject.response.leaderboard.items[index].user["homeCity"],
                         "relationship": jsonObject.response.leaderboard.items[index].user["relationship"],
                          });
    }
}

