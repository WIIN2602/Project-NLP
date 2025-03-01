<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "nlp_project";

$conn = new mysqli($servername, $username, $password, $dbname);
$conn->set_charset("utf8");

if ($conn->connect_error) {
    die(json_encode(["error" => "เชื่อมต่อฐานข้อมูลไม่สำเร็จ: " . $conn->connect_error]));
}

// Fetch all news from DB
$sql = "SELECT id, content FROM news";
$result = $conn->query($sql);
$news_list = [];

while ($row = $result->fetch_assoc()) {
    $news_list[] = $row;
}

foreach ($news_list as $news) {
    $news_id = $news['id'];
    $content = $news['content'];

    $data = json_encode(["id" => $news_id, "content" => $content]);

    $ch = curl_init("http://127.0.0.1:5000/process_news");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $response = curl_exec($ch);
    curl_close($ch);
}

$conn->close();
echo json_encode(["message" => "Processed all news successfully!"]);
?>
