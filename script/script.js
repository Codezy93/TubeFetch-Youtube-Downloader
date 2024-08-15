function trending(){
    const url = 'http://127.0.0.1:5000/trending';
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            const trendingVideos = response.trending;
            const grid = $('.trending-grid');
            trendingVideos.forEach(video => {
                const tile = $('<div></div>').addClass('tile');
                const img = $('<img>').attr('src', video.thumbnailURL);
                const title = $('<p></p>').addClass('trending-video-name').text(video.title);
                const author = $('<p></p>').addClass('trending-video-author').text(video.author);
                const views = $('<p></p>').addClass('trending-video-views').text(video.views);
                const duration = $('<p></p>').addClass('trending-video-duration').text(video.duration);
                tile.append(img, title, author, views, duration);
                tile.on('click', function() {
                    window.location.href = video.url;
                });
                grid.append(tile);
            });
        },
        error: function(error) {
            console.error('Error fetching trending videos:', error);
        }
    });
}

$(document).ready(function() {
    trending();
});
