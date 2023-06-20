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
      document.getElementById("ls-movie-title").innerHTML = responseData["Title"]
      document.getElementById("poster").innerHTML = `<img src="${responseData['Poster']}" alt="movie title"/>`
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error('Error:', error);
    });
}