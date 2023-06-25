function showIfMovie(){
    var urlParams = new URLSearchParams(window.location.search);
    var movieName = urlParams.get('movie_name');
    console.log(movieName);
    if(movieName){
        document.getElementById("movieSearch").value = movieName;
        getValueFromMovieSearch();
    }
}

function getValueFromMovieSearch(){
    var movieTitle = document.getElementById("movieSearch").value;
    console.log(movieTitle);

    const data = { dataFromJS: movieTitle };

    fetch('/receive_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      // Handle the response from Flask server
      console.log(responseData);
      document.getElementById("ls-found").style.display = "block";
      document.getElementById("ls-not-found").style.display = "none";

      document.getElementById("Title").innerHTML = responseData["Title"]
      document.getElementById("Poster").innerHTML = `<img src="${responseData['Poster']}" alt="movie title"/>`
      document.getElementById("Year").innerHTML = responseData["Year"]
      document.getElementById("Runtime").innerHTML = responseData["Runtime"]
      document.getElementById("Genre").innerHTML = responseData["Genre"]
      document.getElementById("Director").innerHTML = responseData["Director"]
      document.getElementById("Actors").innerHTML = responseData["Actors"]
      document.getElementById("Country").innerHTML = responseData["Country"]
      document.getElementById("imdbRating").innerHTML = responseData["imdbRating"]
      document.getElementById("Plot").innerHTML = responseData["Plot"]

      var links = responseData["FreeLinks"].split(",");
      var content = ""
      for (let link of links) {
        if(link.length !== 0){
              content += `
                <div class="col-12 col-md-12">
                    <a href="${link}" target="_blank" class="ls-free-link">${link}</a>
                </div>
              `
          }
      }

      document.getElementById("FreeLinks").innerHTML = content;

    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
      document.getElementById("ls-not-found").style.display = "block";
      document.getElementById("ls-found").style.display = "none";
    });
}

function addMovieToUser(){
    var movieTitle = document.getElementById("Title").innerText;
    console.log(movieTitle);

    const data = { dataFromJS: movieTitle };

    fetch('/add_movie_to_user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      console.log(responseData);
      // flash

    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
      // flash
    });
}

function addLink(){
    var freeLink = document.getElementById("freeLink").value;
    var movieName = document.getElementById("Title").innerText;

    console.log(freeLink);
    console.log(movieName);

    const data = { dataFromJS: {"freeLink": freeLink, "movieName": movieName}};

    fetch('/add_link', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      // Handle the response from Flask server
      console.log(responseData);
      window.location.href = "/movie?movie_name=" + movieName;
      //document.getElementById("movieSearch").value = movieName;
      //getValueFromMovieSearch();
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);

    });
}