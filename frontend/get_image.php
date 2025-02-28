<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "news_db";

$conn = new mysqli($servername, $username, $password, $dbname);
$conn->set_charset("utf8");

$id = $_GET['id'];
$sql = "SELECT image FROM news WHERE id=?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $id);
$stmt->execute();
$stmt->bind_result($image);
$stmt->fetch();
$stmt->close();
$conn->close();

header("Content-Type: image/png");
echo $image;
?>
