<?php
$data = file_get_contents("http://localhost/NLP_PROJECT/frontend/fetch_news.php");
$news_list = json_decode($data, true);
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>News Summary</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script> <!-- โหลด jQuery -->
</head>
<body>
    <h1>ข่าวทั้งหมด</h1>
    <ul>
        <?php foreach ($news_list as $news): ?>
            <li id="news-<?php echo $news['id']; ?>">
                <h3><?php echo $news['title']; ?></h3>
                <p>ประเภท: <?php echo $news['type']; ?></p>
                <p><a href="<?php echo $news['link']; ?>">อ่านเพิ่มเติม</a></p>

                <!-- ปุ่มสร้าง Word Cloud -->
                <button class="generate-wordcloud" data-id="<?php echo $news['id']; ?>" data-content="<?php echo htmlspecialchars($news['content']); ?>">สร้างภาพ Word Cloud</button>

                <!-- พื้นที่แสดงภาพ Word Cloud -->
                <div class="wordcloud-container">
                    <img id="wordcloud-<?php echo $news['id']; ?>" src="get_image.php?id=<?php echo $news['id']; ?>" width="400">
                </div>
            </li>
        <?php endforeach; ?>
    </ul>

    <script>
    $(document).ready(function () {
        $(".generate-wordcloud").click(function () {
            var newsId = $(this).data("id");
            var content = $(this).data("content");
            var imageElement = $("#wordcloud-" + newsId);

            $.ajax({
                url: "process_news.php",
                type: "POST",
                data: { id: newsId, content: content },
                success: function () {
                    // โหลดภาพใหม่เมื่อเสร็จสิ้น
                    imageElement.attr("src", "get_image.php?id=" + newsId + "&t=" + new Date().getTime());
                },
                error: function () {
                    alert("เกิดข้อผิดพลาดในการสร้าง Word Cloud");
                }
            });
        });
    });
    </script>
</body>
</html>
