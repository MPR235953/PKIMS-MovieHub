function removeMovieFromUser(movie_name){
    const data = { dataFromJS: movie_name };

    fetch('/remove_movie_from_user', {
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

function onPosterClick(movie_name){
    window.location.href = "/movie?movie_name=" + movie_name;
}