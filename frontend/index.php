<?php
$data = file_get_contents("http://localhost/NLP_PROJECT/frontend/fetch_news.php");
$news_list = json_decode($data, true);

if (!$news_list) {
    echo "<p style='color: red;'>⚠ ไม่สามารถโหลดข้อมูลข่าวได้ โปรดตรวจสอบ API หรือฐานข้อมูล</p>";
    $news_list = [];
}

// Get unique types from the news list
$news_types = array_unique(array_column($news_list, 'type'));
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>News Summary</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $("#searchInput, #filterType").on("keyup change", function() {
                var value = $("#searchInput").val().toLowerCase();
                var filterType = $("#filterType").val().toLowerCase();
                var hasResults = false;
                
                $(".news-card").each(function() {
                    var title = $(this).find(".news-title").text().toLowerCase();
                    var content = $(this).find(".news-content").text().toLowerCase();
                    var tag = $(this).find(".news-tag").text().toLowerCase();
                    var type = $(this).attr("data-type").toLowerCase();
                    
                    if ((title.includes(value) || content.includes(value) || tag.includes(value)) && (filterType === "all" || type === filterType)) {
                        $(this).show();
                        hasResults = true;
                    } else {
                        $(this).hide();
                    }
                });

                if (!hasResults) {
                    $("#noResults").show();
                } else {
                    $("#noResults").hide();
                }
            });
        });
    </script>
    <style>
        body {
            position: relative;
            width: 1440px;
            height: 1024px;
            overflow-x: scroll;
            background: linear-gradient(180deg, #BCF4DE 51%, #FFB7C3 99.99%);
        }
        h1 {
            text-align: center;
            font-size: 32px;
            margin-top: 20px;
            color: #000;
        }
        .filter-container {
            display: inline-block;
            margin: 20px;
        }
        #filterType {
            width: 150px;
            height: 30px;
            border-radius: 10px;
            padding: 5px;
            font-size: 16px;
        }
        #searchInput {
            display: inline-block;
            width: 400px;
            height: 30px;
            background: #FFB7C3;
            border-radius: 20px;
            padding: 5px;
            font-size: 16px;
        }
        .news-container {
            position: absolute;
            width: 1220px;
            top: 150px;
            left: 110px;
        }
        .news-card {
            background: linear-gradient(180deg, #FCC5C0 0%, #7A0177 100%);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out;
        }
        .news-card:hover {
            transform: scale(1.05);
        }
        .news-title {
            font-family: 'Mitr', sans-serif;
            font-size: 24px;
            color: #000;
        }
        .news-content, .news-tag {
            font-size: 18px;
            color: #000;
        }
        .wordcloud-container img {
            width: 100%;
            border-radius: 10px;
        }
        .no-results {
            text-align: center;
            font-size: 20px;
            color: red;
        }
    </style>
</head>
<body>
    <h1>ข่าวทั้งหมด</h1>
    <div class="filter-container">
        <label for="filterType">ประเภท:</label>
        <select id="filterType">
            <option value="all">ทั้งหมด</option>
            <?php foreach ($news_types as $type): ?>
                <option value="<?php echo htmlspecialchars($type); ?>"><?php echo htmlspecialchars($type); ?></option>
            <?php endforeach; ?>
        </select>
    </div>
    <input type="text" id="searchInput" placeholder="ค้นหาข่าว...">
    <div class="news-container">
        <?php if (empty($news_list)) : ?>
            <div id="noResults" class="news-card no-results">
                <h3>ไม่มีข่าวที่ตรงกับการค้นหา</h3>
                <p>โปรดลองป้อนคำใหม่ที่เกี่ยวข้องกับหัวข้อข่าว เนื้อหา หรือแท็ก</p>
            </div>
        <?php else : ?>
            <?php foreach ($news_list as $news): ?>
                <div class="news-card" data-type="<?php echo htmlspecialchars($news['type']); ?>" id="news-<?php echo $news['id']; ?>">
                    <h3 class="news-title"> <?php echo $news['title']; ?> </h3>
                    <p class="news-content">ประเภท: <?php echo $news['type']; ?></p>
                    <p><strong>คำสำคัญ:</strong> <span class="news-tag"> <?php echo $news['tag']; ?> </span></p>
                    <p><a href="<?php echo $news['link']; ?>">อ่านเพิ่มเติม</a></p>
                    <div class="wordcloud-container">
                        <img src="get_image.php?id=<?php echo $news['id']; ?>" alt="Word Cloud">
                    </div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</body>
</html>
