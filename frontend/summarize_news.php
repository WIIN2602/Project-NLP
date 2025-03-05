<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "nlp_project";

$conn = new mysqli($servername, $username, $password, $dbname);
$conn->set_charset("utf8");

if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed: " . $conn->connect_error]));
}

$data = json_decode(file_get_contents("php://input"), true);
$news_id = $data['id'];

$sql = "SELECT content FROM news WHERE id=?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $news_id);
$stmt->execute();
$stmt->bind_result($content);
$stmt->fetch();
$stmt->close();

if (!$content) {
    echo json_encode(["error" => "News content not found"]);
    exit;
}

$data = json_encode(["id" => $news_id, "content" => $content]);

$ch = curl_init("http://127.0.0.1:5000/summarize_news");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

$response = curl_exec($ch);
curl_close($ch);

$conn->close();
echo json_encode(["message" => "Summary created for news ID $news_id"]);
?>
