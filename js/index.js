var form = document.getElementById('upload_form');
var fileSelect = document.getElementById('programs_file');
var uploadButton = document.getElementById('submit_form_btn');

var sl_agitated_calm = document.getElementById('sl_agitated_calm');
var sl_happy_sad = document.getElementById('sl_happy_sad');
var sl_tired_awake = document.getElementById('sl_tired_awake');
var sl_scared_fearless = document.getElementById('sl_scared_fearless');

function get_recommendations(){
  var moods = [];
  if (sl_agitated_calm.value > 50) {
      moods.push('Calm')
  } else if(sl_agitated_calm.value < 50) {
      moods.push('Agitated')
  }

  if (sl_happy_sad.value > 50) {
      moods.push('Sad')
  } else if(sl_happy_sad.value < 50) {
      moods.push('Happy')
  }

  if (sl_tired_awake.value > 50) {
      moods.push('Wide Awake')
  } else if(sl_tired_awake.value < 50) {
      moods.push('Tired')
  }

  if (sl_scared_fearless.value > 50) {
      moods.push('Fearless')
  } else if(sl_scared_fearless.value < 50) {
      moods.push('Scared')
  }
    // Set up the request.
    var xhr = new XMLHttpRequest();

    // Open the connection.
    xhr.open('POST', '/recommendations', true);

    //Send the proper header information along with the request
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    // Set up a handler for when the request finishes.
    xhr.onload = function () {
      if (xhr.status === 200) {
        // CHANGE PICTURES
        var programmes = JSON.parse(xhr.response);
        console.log(programmes);
        for(i in programmes) {
          console.log(programmes[i][0]);
          console.log(programmes[i][1]);
          var image = document.getElementById('programme-image-' + i);
          var title = document.getElementById('programme-text-' + i);
          image.src = programmes[i][1];
          title.innerHTML = programmes[i][0]
        }
      } else {
        alert('An error occurred!');
      }
    };

    // Send the Data.
    xhr.send('moods=' + moods);
};

form.onsubmit = function(event) {
  console.log("Here we are");
  event.preventDefault();

  // Update button text.
  uploadButton.value = 'Uploading...';


    // Get the selected files from the input.
    var files = fileSelect.files;

    // Create a new FormData object.
    var formData = new FormData();

    // Loop through each of the selected files.
    for (var i = 0; i < files.length; i++) {
      var file = files[i];

      // Add the file to the request.
      formData.append('xml[]', file, file.name);
    }

    // Set up the request.
    var xhr = new XMLHttpRequest();

    // Open the connection.
    xhr.open('POST', '/upload', true);

    // Set up a handler for when the request finishes.
    xhr.onload = function () {
      if (xhr.status === 200) {
        // File(s) uploaded.
        uploadButton.value = 'Upload';
      } else {
        alert('An error occurred!');
      }
    };

    // Send the Data.
    xhr.send(formData);
    console.log('Fiished')
};