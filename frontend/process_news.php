<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $news_id = $_POST['id'];
    $content = $_POST['content'];

    $data = json_encode(["id" => $news_id, "content" => $content]);

    $ch = curl_init("http://127.0.0.1:5000/process_news");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $response = curl_exec($ch);
    curl_close($ch);

    echo $response;
}
?>
