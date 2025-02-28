<?php
$data = file_get_contents("http://localhost/NLP_PROJECT/frontend/fetch_news.php");
$news_list = json_decode($data, true);
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>News Summary</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="styles.css"> <!-- Linking external CSS file -->
</head>
<body>
    <div class="container">
        <h1>ข่าวทั้งหมด</h1>
        <ul class="news-list">
            <?php foreach ($news_list as $news): ?>
                <li class="news-item" id="news-<?php echo $news['id']; ?>">
                    <h3><?php echo $news['title']; ?></h3>
                    <p class="news-type">ประเภท: <?php echo $news['type']; ?></p>
                    <p><strong>คำสำคัญ:</strong> <span class="tag"><?php echo $news['tag']; ?></span></p>
                    <p><a class="read-more" href="<?php echo $news['link']; ?>">อ่านเพิ่มเติม</a></p>
                    <div class="wordcloud-container">
                        <img class="wordcloud" id="wordcloud-<?php echo $news['id']; ?>" src="get_image.php?id=<?php echo $news['id']; ?>" width="400">
                    </div>
                </li>
            <?php endforeach; ?>
        </ul>
    </div>
</body>
</html>
