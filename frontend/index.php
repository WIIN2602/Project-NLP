<?php
$news_list = []; // No initial data from MySQL
?>

<!DOCTYPE html>
<html lang="th">

<head>
    <meta charset="UTF-8">
    <title>News Summary</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <script>
        $(document).ready(function () {
            // Handle Scrape Button Click
            $("#scrapeButton").click(function () {
                var selectedType = $("#filterType").val();
                var selectedPublisher = $("#filterPublisher").val();
                var selectedYear = $("#filterYear").val();

                $("#noResults").html("<h3>⏳ กำลังดึงข้อมูลข่าว...</h3>").css("color", "blue").show();
                
                setTimeout(function () {
                    $(".news-container").empty();
                    startScraping(selectedType, selectedPublisher, selectedYear);
                }, 5000);
            });

            function startScraping(type, publisher, year) {
                $.ajax({
                    url: "http://127.0.0.1:5000/fetch_news",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({
                        type: type,
                        publisher: publisher,
                        year: year
                    }),
                    success: function (response) {
                        console.log("Scraped Data:", response);

                        if (response.news.length > 0) {
                            $("#noResults").html("<h3 style='color:green;'>✔️ Scraping complete</h3>").show();
                            displayNews(response.news);
                        } else {
                            $("#noResults").html("<h3 style='color:red;'>❌ ไม่มีข่าวที่ตรงกับการค้นหา</h3>").show();
                        }
                    },
                    error: function (xhr, status, error) {
                        console.log("AJAX Error:", xhr, status, error);
                        let errorMessage = xhr.responseText ? xhr.responseText : error ? error : "Unknown error";

                        $("#noResults").html(
                            "<h3 style='color:red;'>❌ ดึงข้อมูลข่าวไม่สำเร็จ</h3>" +
                            "<p><strong>Error:</strong> " + errorMessage + "</p>"
                        ).show();
                    }
                });
            }

            function displayNews(newsList) {
                $(".news-container").empty();

                newsList.forEach(news => {
                    var newsCard = `
                        <div class="news-card" data-id="${news.id}" data-type="${news.type}" data-publisher="${news.publisher}" data-year="${news.date ? new Date(news.date).getFullYear() : 'No data'}">
                            <h3 class="news-title">${news.title}</h3>
                            <p class="news-content" style="display:none;">${news.content}</p> <!-- Hidden Content -->
                            <p>
                                ประเภท: ${news.type} | ผู้เผยแพร่: ${news.publisher} | วันที่: ${news.date || 'No data'}
                            </p>
                            <p><a href="${news.link}" target="_blank">อ่านเพิ่มเติม</a></p>
                            <button class="btn" onclick="processNews('${news.id}', this)">Generate Word Cloud</button>
                            <button class="btn" onclick="extractKeywords('${news.id}', this)">Extract Keywords</button>
                            <button class="btn" onclick="summarizeNews('${news.id}', this)">Summarize News</button>
                            <div class="summary-container">
                                <strong>ไฮไลท์ในข่าว:</strong>
                                <button class="copy-btn" onclick="copySummary(this)">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <p id="summary-${news.id}">${news.summary || "<span style='color: gray;'>ยังไม่มีการสรุป</span>"}</p>
                            </div>
                            <div class="tag-container">
                                <strong>คำปรากฎในข่าวเยอะที่สุด: </strong>
                                <span class="news-tag" id="keywords-${news.id}">${news.tag || "ยังไม่มีการวิเคราะห์"}</span>
                            </div>
                            <div class="wordcloud-container">
                                <img id="wordcloud-${news.id}" src="" alt="Word Cloud">
                            </div>
                        </div>
                    `;
                    $(".news-container").append(newsCard);
                });
            }
        });

        // Fetch news content dynamically
        function getNewsContent(newsId) {
            return $(".news-card[data-id='" + newsId + "'] .news-content").text();
        }

        // Generate Word Cloud
        function processNews(newsId, button) {
            $(button).text("⌛ Generating...").prop("disabled", true);
            
            let content = getNewsContent(newsId); // Fetch the content dynamically

            $.ajax({
                url: "http://127.0.0.1:5000/process_news",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ id: newsId, content: content }),
                success: function (response) {
                    if (response.wordcloud) {
                        $("#wordcloud-" + newsId).attr("src", "data:image/png;base64," + response.wordcloud);
                    }
                    $(button).text("✔️ Done").prop("disabled", false);
                },
                error: function () {
                    alert("❌ Failed to generate Word Cloud");
                    $(button).text("Generate Word Cloud").prop("disabled", false);
                }
            });
        }

        // Extract Keywords
        function extractKeywords(newsId, button) {
            $(button).text("⌛ Extracting...").prop("disabled", true);

            let content = getNewsContent(newsId);

            $.ajax({
                url: "http://127.0.0.1:5000/extract_keywords",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ id: newsId, content: content }),
                success: function (response) {
                    if (response.keywords) {
                        $("#keywords-" + newsId).text(response.keywords.join(", "));
                    }
                    $(button).text("✔️ Done").prop("disabled", false);
                },
                error: function () {
                    alert("❌ Failed to extract keywords");
                    $(button).text("Extract Keywords").prop("disabled", false);
                }
            });
        }

        // Summarize News
        function summarizeNews(newsId, button) {
            $(button).text("⌛ Summarizing...").prop("disabled", true);

            let content = getNewsContent(newsId);

            $.ajax({
                url: "http://127.0.0.1:5000/summarize_news",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ id: newsId, content: content }),
                success: function (response) {
                    if (response.summary) {
                        $("#summary-" + newsId).text(response.summary);
                    }
                    $(button).text("✔️ Done").prop("disabled", false);
                },
                error: function () {
                    alert("❌ Failed to summarize news");
                    $(button).text("Summarize News").prop("disabled", false);
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
            background-color: white;
            font-family: 'Bai Jamjuree', sans-serif;
            color: #333333;
        }

        h1 {
            text-align: center;
            font-size: 36px;
            margin-top: 20px;
            color: #00BFFF;
        }

        .filter-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            text-align: center;
        }

        select, input {
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            border: 2px solid #00BFFF;
            background: #E0FFFF;
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
            background: linear-gradient(180deg, #E0FFFF 0%, #00BFFF 100%);
            border-radius: 20px;
            padding: 24px 16px;
            margin: 15px 0;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out;
        }

        .news-card:hover {
            transform: scale(1.05);
        }

        .no-results {
            text-align: center;
            font-size: 20px;
            color: red;
            display: none;
        }

        .btn, #scrapeButton {
            display: inline-block;
            padding: 10px 15px;
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #00BFFF;
            border-radius: 10px;
            background: #E0FFFF;
            color: #000;
            cursor: pointer;
            margin: 5px;
            transition: background 0.3s, transform 0.2s;
        }

        .btn:hover, #scrapeButton:hover {
            background: #00BFFF;
            color: white;
            transform: scale(1.05);
        }
        .wordcloud-container img {
            max-width: 100%;  /* Ensure it does not overflow its container */
            height: auto;      /* Maintain aspect ratio */
            display: block;    /* Ensure proper alignment */
            margin: 10px auto; /* Center the image */
        }

    </style>
</head>

<body>
    <h1>📰 ข่าวทั้งหมด</h1>
    <div class="filter-container">
        <label>ผู้เผยแพร่:</label>
        <select id="filterPublisher">
            <option value="thestandard">The Standard</option>
            <option value="matichon">Matichon</option>
            <option value="tna">TNA</option>
        </select>
        <label>ประเภท:</label>
        <select id="filterType">
            <option value="entertainment">บันเทิง</option>
            <option value="politics">การเมือง</option>
            <option value="sport">กีฬา</option>
            <option value="foreign">ต่างประเทศ</option>
        </select>
        <label>ปี:</label>
        <select id="filterYear">
            <option value="2025">2025</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
        </select>
        <button id="scrapeButton">ดึงข้อมูล</button>
    </div>
    <div class="news-container">
        <div id="noResults" class="no-results"></div>
    </div>
</body>
</html>
