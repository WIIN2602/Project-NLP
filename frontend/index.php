<?php
$data = file_get_contents("http://localhost/NLP_PROJECT/frontend/fetch_news.php");
$news_list = json_decode($data, true);

if (!$news_list) {
    echo "<p style='color: red;'>⚠ ไม่สามารถโหลดข้อมูลข่าวได้ โปรดตรวจสอบ API หรือฐานข้อมูล</p>";
    $news_list = [];
}

// Get unique types, publishers, and years
$news_types = array_unique(array_column($news_list, 'type'));
$publishers = array_unique(array_column($news_list, 'publisher'));
$years = array_unique(array_map(function ($news) {
    return !empty($news['date']) ? date("Y", strtotime($news['date'])) : "No data";
}, $news_list));
sort($years); // Sort years in ascending order
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>News Summary</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            function filterNews() {
                var searchText = $("#searchInput").val().toLowerCase();
                var selectedType = $("#filterType").val().toLowerCase();
                var selectedPublisher = $("#filterPublisher").val().toLowerCase();
                var selectedYear = $("#filterYear").val().toLowerCase();
                var hasResults = false;

                $(".news-card").each(function() {
                    var newsType = $(this).attr("data-type").toLowerCase();
                    var newsPublisher = $(this).attr("data-publisher").toLowerCase();
                    var newsYear = $(this).attr("data-year").toLowerCase();
                    var newsTitle = $(this).find(".news-title").text().toLowerCase();
                    var newsContent = $(this).find(".news-content").text().toLowerCase();
                    var newsTags = $(this).find(".news-tag").text().toLowerCase();

                    var matchesType = (selectedType === "all" || newsType === selectedType);
                    var matchesPublisher = (selectedPublisher === "all" || newsPublisher === selectedPublisher);
                    var matchesYear = (selectedYear === "all" || newsYear === selectedYear);
                    var matchesSearch = (searchText === "" || newsTitle.includes(searchText) || newsContent.includes(searchText) || newsTags.includes(searchText));

                    if (matchesType && matchesPublisher && matchesYear && matchesSearch) {
                        $(this).show();
                        hasResults = true;
                    } else {
                        $(this).hide();
                    }
                });

                $("#noResults").toggle(!hasResults);
            }

            $("#filterType, #filterPublisher, #filterYear, #searchInput").on("change keyup", filterNews);
        });

        function processNews(newsId) {
            $.ajax({
                url: "process_news.php",
                type: "POST",
                data: JSON.stringify({ id: newsId }),
                contentType: "application/json",
                success: function() {
                    location.reload();  // Reload the page to show the updated word cloud
                },
                error: function(xhr) {
                    alert("Error processing news: " + xhr.responseText);
                }
            });
        }

        function extractKeywords(newsId) {
            $.ajax({
                url: "extract_keywords.php",
                type: "POST",
                data: JSON.stringify({ id: newsId }),
                contentType: "application/json",
                success: function() {
                    location.reload();  // Reload to show updated keywords
                },
                error: function(xhr) {
                    alert("Error extracting keywords: " + xhr.responseText);
                }
            });
        }

        function summarizeNews(newsId) {
            $.ajax({
                url: "summarize_news.php",
                type: "POST",
                data: JSON.stringify({ id: newsId }),
                contentType: "application/json",
                success: function() {
                    location.reload();  // Reload to show updated summary
                },
                error: function(xhr) {
                    alert("Error summarizing news: " + xhr.responseText);
                }
            });
        }
    </script>

    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(180deg, #BCF4DE 51%, #FFB7C3 99.99%);
        }

        h1 {
            text-align: center;
            font-size: 32px;
            margin-top: 20px;
            color: #000;
        }

        /* 🔹 Filter Container & Inputs Styled Same as Buttons */
        .filter-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        select, input {
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            border: 2px solid #7A0177;
            background: #FCC5C0;
            color: #000;
            font-weight: bold;
            text-align: center;
        }

        #searchInput {
            width: 300px;
        }

        .news-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 90%;
            max-width: 1220px;
        }

        .news-card {
            background: linear-gradient(180deg, #FCC5C0 0%, #7A0177 100%);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out;
        }

        .news-card:hover {
            transform: scale(1.05);
        }
        
        /* 🔹 "อ่านเพิ่มเติม" Link Styling */
        .news-card p a {
            display: inline-block;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background: #7A0177;
            padding: 10px 15px;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        /* 🔹 Hover Effect */
        .news-card p a:hover {
            background: #FCC5C0;
            color: black;
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .news-title {
            font-size: 24px;
            color: #000;
            text-align: center;
        }

        .news-content, .news-tag {
            font-size: 18px;
            color: #000;
            text-align: left;
        }

        .wordcloud-container {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }

        .wordcloud-container img {
            width: 100%;
            max-width: 400px;
            border-radius: 10px;
        }

        .summary-container {
            text-align: left;
            margin-top: 10px;
            background: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
        }

        /* 🔹 Buttons inside Cards Styled Same as Filter Inputs */
        .news-card button {
            display: inline-block;
            padding: 10px 15px;
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #7A0177;
            border-radius: 10px;
            background: #FCC5C0;
            color: #000;
            cursor: pointer;
            margin: 5px;
            transition: background 0.3s, transform 0.2s;
        }

        .news-card button:hover {
            background: #7A0177;
            color: white;
            transform: scale(1.05);
        }

        .no-results {
            text-align: center;
            font-size: 20px;
            color: red;
            display: none;
        }

        .tag-container {
            text-align: left;
            margin-top: 10px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-wrap: wrap;
            justify-content: left;
            gap: 8px;
        }
        
        /* 🔹 Filter Dropdown Styling */
        #filterType {
            padding: 10px 15px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            border: 2px solid #7A0177;
            background: #FCC5C0;
            color: black;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        /* 🔹 Hover & Focus Effect */
        #filterType:hover, #filterType:focus {
            background: #7A0177;
            color: white;
            border-color: #FCC5C0;
            outline: none;
        }

        /* 🔹 Dropdown Options Styling */
        #filterType option {
            background: white;
            color: black;
            font-weight: bold;
        }

        /* 🔹 Option Hover Effect (for some browsers) */
        #filterType option:hover {
            background: #FCC5C0;
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

        <label for="filterPublisher">ผู้เผยแพร่:</label>
        <select id="filterPublisher">
            <option value="all">ทั้งหมด</option>
            <?php foreach ($publishers as $publisher): ?>
                <option value="<?php echo htmlspecialchars($publisher); ?>"><?php echo htmlspecialchars($publisher); ?></option>
            <?php endforeach; ?>
        </select>

        <label for="filterYear">ปี:</label>
        <select id="filterYear">
            <option value="all">ทั้งหมด</option>
            <?php foreach ($years as $year): ?>
                <option value="<?php echo htmlspecialchars($year); ?>"><?php echo htmlspecialchars($year); ?></option>
            <?php endforeach; ?>
        </select>

        <input type="text" id="searchInput" placeholder="ค้นหาข่าว...">
    </div>

    <div class="news-container">
        <div id="noResults" class="no-results">
            <h3>ไม่มีข่าวที่ตรงกับการค้นหา</h3>
            <p>โปรดลองป้อนคำใหม่ที่เกี่ยวข้องกับหัวข้อข่าว เนื้อหา หรือแท็ก</p>
        </div>

        <?php foreach ($news_list as $news): ?>


            <div class="news-card" data-type="<?php echo htmlspecialchars($news['type']); ?>" data-publisher="<?php echo htmlspecialchars($news['publisher'] ?? 'No data'); ?>" data-year="<?php echo !empty($news['date']) ? date("Y", strtotime($news['date'])) : 'No data'; ?>" id="news-<?php echo $news['id']; ?>">
                <h3 class="news-title"><?php echo $news['title']; ?></h3>
                <p class="news-content">
                    ประเภท: <?php echo $news['type']; ?> | ผู้เผยแพร่: <?php echo $news['publisher'] ?? 'No data'; ?> | วันที่: <?php echo !empty($news['date']) ? $news['date'] : 'No data'; ?></span>
                </p>
                <p><a href="<?php echo $news['link']; ?>">อ่านเพิ่มเติม</a></p>


                <button onclick="processNews(<?php echo $news['id']; ?>)">Generate Word Cloud</button>
                <button onclick="extractKeywords(<?php echo $news['id']; ?>)">Extract Keywords</button>
                <button onclick="summarizeNews(<?php echo $news['id']; ?>)">Summarize News</button>

                <div class="summary-container">
                    <strong>ไฮไลท์ในข่าว:</strong>
                    <p><?php echo !empty($news['summary']) ? htmlspecialchars($news['summary']) : "<span style='color: gray;'>ยังไม่มีการสรุป</span>"; ?></p>
                </div>

                <div class="tag-container">
                    <strong>คำปรากฎในข่าวเยอะที่สุด: </strong>
                    <span class="news-tag"><?php echo htmlspecialchars($news['tag'] ?? 'ยังไม่มีการวิเคราะห์'); ?></span>
                </div>

                <div class="wordcloud-container">
                    <img id="news-img-<?php echo $news['id']; ?>" src="get_image.php?id=<?php echo $news['id']; ?>" alt="Word Cloud">
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</body>
</html>
