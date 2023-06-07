document.addEventListener('DOMContentLoaded', function() {
    // Replace 'YOUR_API_KEY' with your actual News API key
    var apiKey = 'YOUR_API_KEY';
    
    // Fetch news data from the News API
    function fetchNews() {
      var url = '0efc5b349dbf4d67aba7e45d8a7dd58e' +
        'q=agriculture advancements&' +
        'language=en&' +
        'apiKey=' + apiKey;
  
      fetch(url)
        .then(function(response) {
          return response.json();
        })
        .then(function(data) {
          if (data.status === 'ok') {
            displayNews(data.articles);
          } else {
            console.error('Failed to fetch news:', data.message);
          }
        })
        .catch(function(error) {
          console.error('Error fetching news:', error);
        });
    }
  
    // Display news data on the webpage
    function displayNews(articles) {
      var newsList = document.getElementById('news-list');
      newsList.innerHTML = '';
  
      articles.forEach(function(article) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        link.href = article.url;
        link.target = '_blank';
        link.textContent = article.title;
        li.appendChild(link);
        newsList.appendChild(li);
      });
    }
  
    fetchNews();
  
    setInterval(fetchNews, 60000); // Fetch news every minute
  });