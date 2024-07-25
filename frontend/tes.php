<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KNN Sentiment Analysis</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <div class="container">
        <h1>KNN Sentiment Analysis</h1>
        <form id="textForm">
            <textarea id="inputText" rows="4" placeholder="Enter text here..."></textarea>
            <button type="submit">Analyze Sentiment</button>
        </form>
        <div id="result">
            <h2>Result</h2>
            <p>Preprocessing Text: <span id="textpre"></span></p>
            <p>Sentiment: <strong> <span id="sentiment"></span></strong></p>
            <h3>Top 3 Similar Texts</h3>
            <ul id="similarTexts"></ul>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
    $(document).ready(function() {
        $('#textForm').on('submit', function(event) {
            event.preventDefault();
            var inputText = $('#inputText').val();
            if (inputText.trim() === "") {
                alert("Please enter some text.");
                return;
            }

            $.ajax({
                url: 'http://127.0.0.1:5000/knn',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    text: inputText
                }),
                success: function(response) {
                    $('#textpre').text(response.preprocess_text);
                    $('#sentiment').text(response.sentiment);
                    var similarTexts = $('#similarTexts');
                    similarTexts.empty();
                    response.results.forEach(function(result) {
                        similarTexts.append('<li>Rank: ' + result.rank +
                            ' - Similarity: ' + result.similarity.toFixed(2) +
                            ' - Text: ' + result.text + '</li>');
                    });
                },
                error: function(xhr) {
                    alert("Error: " + xhr.responseJSON.error);
                }
            });
        });
    });
    </script>
</body>

</html>