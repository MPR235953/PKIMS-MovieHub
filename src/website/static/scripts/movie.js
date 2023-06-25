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