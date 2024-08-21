console.log("script.js loaded");

function getPrediction() {
    const pred = document.getElementById("pred").value;
    if (!country1 || !country2) {
        alert("Please select two countries on the map.");
        return;
    }
    console.log("calls getPrediction()"+ country1 + country2 + pred)
    apiurl = "/connector/get_prediction/" + country1 + "/" + country2 + "/" + pred
    fetch(apiurl)
        .then(response => response.json())
        .then(data => {
            let plot_url = data.plot_url;
            // If the plot is returned, display it
            if (data.plot_url) {
                console.log("Received data:", data);
                const imgElement = document.getElementById('pred_img');
                imgElement.src = 'data:image/png;base64,' + data.plot_url;
                imgElement.style.display = 'block'; // Make the image visible
            } else {
                alert('No plot was generated');
            }
        })
        .catch(error => {
            console.error('Error fetching prediction:', error);
        });
}

// Function to handle submit action
function cases() {
    const param2 = document.getElementById('param2').value;

    if (!country1 || !country2) {
        alert("Please select two countries on the map.");
        return;
    }
    console.log("calls cases()"+ country1 + country2 + param2)
    method = "connector"
    // Example logic to handle data submission, API calls, etc.
    apiurl = "/" + method + "/cases/" + country1 + "/" + country2 + "/" + param2

    document.getElementById("output").innerHTML = "Getting Data";
    fetch(apiurl)
        // .then(response => response.json())
        // .then(data => document.getElementById("output").innerHTML = "<pre>" + JSON.stringify(data, null, "  ") + "</pre>")
        // .catch(error => document.getElementById("output").innerHTML = "There was an error: " + error)
        
        .then(response => response.json())
        .then(data => {
            // If the plot is returned, display it
            if (data.plot) {
                console.log(data)
                const imgElement = document.getElementById('plot');
                imgElement.src = 'data:image/png;base64,' + data.plot;
                imgElement.style.display = 'block'; // Make the image visible
            } else {
                alert('No plot was generated');
            }
        });        
}

function addComment() {
    const comment = document.getElementById('comment').value;

    if (!country1 || !country2) {
        alert("Please select two countries on the map.");
        return;
    }

    if (!comment) {
        alert("Please enter a comment before submitting.");
        return;
    }

    const data = {
        user_id: "user123",  // Replace with dynamic user ID if available
        country1: country1,
        country2: country2,
        param2: document.getElementById('param2').value,
        comment: comment
    };

    fetch('connector/add_comment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('comment').value = '';
    })
    .catch(error => console.error('Error:', error));
}

function getComments(){
    fetch('connector/get_comments')
    .then(response => response.json())
    .then(data => {
        let output = "";
        data.forEach(comment => {
            output += `
                <div class="comment-block">
                    <p><strong>Country 1:</strong> ${comment.country1}</p>
                    <p><strong>Country 2:</strong> ${comment.country2}</p>
                    <p><strong>Parameter:</strong> ${comment.param2}</p>
                    <p><strong>Comment:</strong> ${comment.comment}</p>
                    <p><strong>Timestamp:</strong> ${new Date(comment.timestamp).toLocaleString()}</p>
                </div>
            `;
        });
        document.getElementById("output").innerHTML = output;
    })
    .catch(error => document.getElementById("output").innerHTML = "There was an error: " + error);

}

function clearSelection() {
    country1 = null;
    country2 = null;
    document.getElementById('country1').value = '';
    document.getElementById('country2').value = '';
    document.getElementById('plot').style.display = 'none';
    document.getElementById('pred_img').style.display = 'none';
    console.log("Selection and graph cleared");
}