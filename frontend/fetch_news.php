<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "nlp_project";

// เชื่อมต่อ MySQL
$conn = new mysqli($servername, $username, $password, $dbname);
$conn->set_charset("utf8");

// ตรวจสอบการเชื่อมต่อ
if ($conn->connect_error) {
    die(json_encode(["error" => "เชื่อมต่อฐานข้อมูลไม่สำเร็จ: " . $conn->connect_error]));
}

// คิวรีข้อมูลข่าว
$sql = "SELECT id, title, type, tag, date, content, link FROM news";
$result = $conn->query($sql);

$news = [];
while ($row = $result->fetch_assoc()) {
    $news[] = $row;
}

// ถ้าไม่มีข่าวให้แจ้งเตือน
if (empty($news)) {
    echo json_encode(["error" => "ไม่พบข้อมูลข่าวในฐานข้อมูล"]);
} else {
    header('Content-Type: application/json');
    echo json_encode($news);
}

$conn->close();
?>
