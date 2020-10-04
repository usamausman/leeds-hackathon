<?php
$servername = "localhost:3306";
$username = "phpmyadmin";
$password = "root";
$database = "homeless";

$conn = mysqli_connect($servername, $username, $password, $database);
$sql = "SELECT * FROM coreData";
$result = $conn->query($sql);

if ($result->num_rows > 0){
    while ($row = $result->fetch_assoc()){

        if ($row["Error"] != NULL){
            $a = $row["State"] . $row["Error"];
        }
        else {
            $a = $row["State"];
        }

        header('Content-Type: text/event-stream');
        header('Cache-Control: no-cache');

        $time = date('r');
        echo "data:$a\n\n";

        flush();
    }
}

$conn->close();

?>
